from collections import defaultdict
import copy
from functools import partial
import inspect
from itertools import chain
import logging
import operator
import os
from pathlib import Path
from time import time
import typing
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

from torch._subclasses import FakeTensorMode
from torch.fx.passes.shape_prop import ShapeProp
from torch.fx.passes.split_module import split_module

if typing.TYPE_CHECKING:
    from furiosa_llm.models import ModelMetadata

import furiosa_llm_models
from furiosa_torch_ext.torch_ext import eliminate_dead_code
from more_itertools import zip_equal
import torch
from torch._dispatch.python import enable_python_dispatcher
from torch._dynamo.source import GetItemSource, LocalSource
from torch._guards import Source
from torch._subclasses.fake_tensor import FakeTensor
import torch.fx
from torch.fx import Graph, GraphModule, Node, map_arg
from torch.fx.experimental.proxy_tensor import make_fx
from torch.fx.node import has_side_effect
from torch.overrides import TorchFunctionMode
from torch.utils._pytree import tree_flatten, tree_map_only

from furiosa_llm.models.metadata import DecomposedLayerNorm
from furiosa_llm.models.quant import QuantCausalLM
from furiosa_llm.parallelize.export.graphmodule import load_gm, save_gm
from furiosa_llm.parallelize.export.tensor import ParamfileFormat, ParamFileInfo, save_model
from furiosa_llm.parallelize.hash import get_env_independent_hash, hash_example_inputs, hash_model
from furiosa_llm.parallelize.model_creation_info import ModelCreationInfo
from furiosa_llm.parallelize.node_meta import (
    add_tensor_meta,
    fill_tensor_meta_from_val_meta,
    get_original_name,
    has_original_name,
)
from furiosa_llm.parallelize.original_node_mapper import add_original_name_info, add_qparam_info
from furiosa_llm.parallelize.utils import (
    flatten_input_tensors,
    get_cache_path_if_exists,
    get_fake_mode,
    get_normalized_torch_op_node_args,
    get_original_model_type,
    get_output_names,
    get_tensor_from_node,
    is_typecast_node,
    recursive_getattr,
)

# Model tracer version
TRACER_VERSION = "0.2.0"
GRAPHMODULE_SERILAIZER_VERSION = "0.3.0"
logger = logging.getLogger(__file__)


class FakeCopyModeWithMapping(TorchFunctionMode):
    """When `self.fake_to_real` is False, this converts all real tensors in objects to fake ones, maintaining a mapping from fake tensor to real tensor.
    Otherwise, this converts all fake tensors in objects to original real ones using previously saved mapping.
    """

    def __init__(self, fake_mode):
        self.fake_mode = fake_mode
        self.fake_tensor_to_real = {}
        self.fake_to_real = False

    def set_fake_to_real(self, val: bool) -> None:
        self.fake_to_real = val

    def _handle_tensor(self, input_tensor: torch.Tensor) -> torch.Tensor:
        if self.fake_to_real:
            if isinstance(input_tensor, FakeTensor):
                # Convert fake tensor to its original real tensor.
                new_tensor = self.fake_tensor_to_real[input_tensor]
            else:
                # This tensor is real tensor which does not exist before tracing, but created dynamicall.
                # Just return this as it is.
                new_tensor = input_tensor
        else:
            if isinstance(input_tensor, FakeTensor):
                # This tensor is originally fake tensor.
                new_tensor = input_tensor
                self.fake_tensor_to_real[input_tensor] = input_tensor
            else:
                # Create fake tensor from real tensor.
                new_tensor = self.fake_mode.from_tensor(input_tensor, static_shapes=True)
            self.fake_tensor_to_real[new_tensor] = input_tensor
        return new_tensor

    def __torch_function__(self, func, types, args=(), kwargs=None):
        kwargs = kwargs if kwargs else {}

        # clone will get called in Parameter deepcopy
        if func == torch._C._TensorBase.clone:
            to_be_cloned = args[0]
            new_tensor = self._handle_tensor(to_be_cloned)
            return new_tensor
        elif func == torch.Tensor.__deepcopy__:
            assert len(args) == 2 and len(kwargs) == 0
            tensor, memo = args

            if id(tensor) in memo:
                return memo[id(tensor)]

            out = self._handle_tensor(tensor)
            memo[id(tensor)] = out
            return out
        else:
            with torch._C.DisableTorchFunctionSubclass():
                return func(*args, **kwargs)


def _remove_duplicate_typecasts(graph: Graph) -> None:
    for node in graph.nodes:
        if not is_typecast_node(node):
            continue

        dtype = node.meta["tensor_meta"].dtype

        to_searches = list(node.users)

        while to_searches:
            child = to_searches.pop()
            if not is_typecast_node(child) or child.meta["tensor_meta"].dtype != dtype:
                continue
            to_searches.extend(child.users)
            child.replace_all_uses_with(node)
            graph.erase_node(child)


def _merge_duplicate_descendants(node: Node, gm: GraphModule) -> None:
    cur = node

    while True:
        children = tuple(cur.users.keys())
        if len(children) == 0:
            return
        elif len(children) == 1:
            cur = children[0]
            continue
        else:
            first_child = children[0]
            if not all(
                first_child.args == child.args and first_child.kwargs == child.kwargs
                for child in children[1:]
            ):
                # Children are not identical. Just stop here.
                return

            # All children are identical. Remove duplicates and leave just one of them.
            representative_child = children[0]

            for duplicate_child in children[1:]:
                duplicate_child.replace_all_uses_with(representative_child)
                gm.graph.erase_node(duplicate_child)
            cur = representative_child


# FIXME: this function is highly coupled with mlperf submission slice model.
def _make_quantized_gptj_mlperf_slice_prefill_model_slicable(
    gm: GraphModule,
) -> None:
    targets = [
        node
        for node in gm.graph.nodes
        if node.op == "placeholder"
        and get_original_name(node) in ("position_ids", "new_key_location", "new_value_location")
    ]

    # position_ids: placeholder - unsqueeze - repeat - gather
    # new_key_location, new_value_location: placeholder - reshape - squeeze - index_put
    for target in targets:
        _merge_duplicate_descendants(target, gm)


def _remove_unnecessary_larger_typecast_before_index(graph: Graph) -> None:
    for node in graph.nodes:
        if node.op != "call_function" or node.target != torch.ops.aten.index.Tensor:
            continue
        indices = node.args[1]
        if len(indices) != 1:
            raise NotImplementedError("We only consider index ops with single index tensor now.")
        index = indices[0]
        if is_typecast_node(index) and index.meta["tensor_meta"].dtype == torch.int64:
            assert len(index.all_input_nodes) == 1
            node_before_conversion = index.all_input_nodes[0]
            dtype_before_cast = node_before_conversion.meta["tensor_meta"].dtype
            if (
                not dtype_before_cast.is_floating_point
                and torch.iinfo(dtype_before_cast).bits < torch.iinfo(torch.int64).bits
            ):
                index.replace_all_uses_with(node_before_conversion)
                graph.erase_node(index)


def _check_all_index_ops_i32_index(graph: Graph) -> None:
    for node in graph.nodes:
        if not (
            node.op == "call_function"
            and node.target in (torch.ops.aten.index.Tensor, torch.ops.aten.index_put_.default)
        ):
            continue
        indices = node.kwargs.get("indices") or node.args[1]

        if len(indices) != 1:
            raise NotImplementedError("We only consider index ops with single index tensor now.")
        index = indices[0]

        if index.meta["tensor_meta"].dtype != torch.int32:
            raise ValueError("We only consider index ops with i32 index tensor now.")


def decompose_layernorm(gm: GraphModule):
    fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

    for node in gm.graph.nodes:
        if not (
            node.op == "call_function"
            and node.target
            in (
                torch.ops.aten.native_layer_norm.default,
                torch.ops.aten.layer_norm.default,
            )
        ):
            continue
        node_args, node_kwargs = get_normalized_torch_op_node_args(node)
        node.args = node_args
        node.kwargs = node_kwargs

        # input, normalized_shape, weight , bias, eps when ``torch.ops.aten.native_layer_norm.default``.
        # input, normalized_shape, weight(optional) = 0, bias (optional) = 0, eps (optional) = 1e-5, cudnn_enable (optional) when ``torch.ops.aten.layer_norm.default``.
        # TODO: add support for cases when weight and bias are not given.
        if len(node.args) < 4:
            raise NotImplementedError("We only support layer_norms with weight and bias now.")

        input_, normalized_shape = node.args[:2]
        eps = node.args[4] if len(node.args) > 4 else 1e-5

        sub_gm, _ = torch._dynamo.export(
            DecomposedLayerNorm(normalized_shape, eps=eps),
            aten_graph=True,
            tracing_mode="static",
        )(get_tensor_from_node(input_, fake_mode=fake_mode))

        # To make all get_attr nodes as placeholders.
        splitted = split_module(sub_gm, None, lambda x: 0)
        sub_gm = splitted.submod_0

        subg_placeholders = tuple(node for node in sub_gm.graph.nodes if node.op == "placeholder")
        input_nodes = tuple(arg for arg in node.args if isinstance(arg, Node))

        # fill tensor meta info for nodes in layernorm subgraph.
        ShapeProp(sub_gm).propagate(
            *map(partial(get_tensor_from_node, fake_mode=fake_mode, gm=gm), input_nodes)
        )

        assert len(subg_placeholders) == len(
            input_nodes
        ), f"{len(subg_placeholders)}, {len(input_nodes)}"

        replace_map = {
            subg_placeholder: input_node
            for subg_placeholder, input_node in zip(subg_placeholders, input_nodes)
        }

        with gm.graph.inserting_before(node):
            output_node = gm.graph.graph_copy(sub_gm.graph, replace_map)

        to_be_replaced = []

        if node.target == torch.ops.aten.native_layer_norm.default:
            # aten.native_layer_norm.default produces a tuple of tensors with length 3.
            for user in node.users:
                if (
                    user.op == "call_function"
                    and user.target == operator.getitem
                    and user.args[1] == 0
                ):
                    to_be_replaced.append(user)
                else:
                    if user.users:
                        # Do we need to support this case?
                        raise NotImplementedError(
                            "Pattern using last two output tensors of aten.native_layer_norm cannot be handled now."
                        )
        else:
            # aten.layer_norm.default produces a single tensor
            assert node.target == torch.ops.aten.layer_norm.default
            to_be_replaced.append(node)

        assert isinstance(output_node, Node)

        for original in to_be_replaced:
            original.replace_all_uses_with(output_node)

    eliminate_dead_code(gm.graph)

    gm.recompile()


def decompose_linear(gm: GraphModule) -> None:
    for node in tuple(gm.graph.nodes):
        if not (node.op == "call_function" and node.target == torch.ops.aten.linear.default):
            continue
        with gm.graph.inserting_before(node):
            transpose_node = gm.graph.call_function(torch.ops.aten.t.default, (node.args[1],))
            add_tensor_meta(transpose_node)

            replacement = gm.graph.call_function(
                torch.ops.aten.matmul.default, (node.args[0], transpose_node)
            )
            add_tensor_meta(replacement)

            if len(node.args) == 3:
                replacement = gm.graph.call_function(
                    torch.ops.aten.add.default, (replacement, node.args[2])
                )
                add_tensor_meta(replacement)
        node.replace_all_uses_with(replacement)
        gm.graph.erase_node(node)
    gm.recompile()


# FIXME: remove `is_quantized_gptj_mlperf_slice_prefill_model` after mlperf.
def _preprocess_gm_for_model_rewrite(
    gm: GraphModule,
    do_decomposition: bool = False,
    is_quantized_gptj_mlperf_slice_prefill_model: bool = False,
    check_for_compilability: bool = True,
) -> None:
    if do_decomposition:
        decompose_linear(gm)
        decompose_layernorm(gm)
    _remove_duplicate_typecasts(gm.graph)
    _remove_unnecessary_larger_typecast_before_index(gm.graph)

    # This is needed for making model slicable by block slicer.
    if is_quantized_gptj_mlperf_slice_prefill_model:
        _make_quantized_gptj_mlperf_slice_prefill_model_slicable(gm)

    if check_for_compilability:
        _check_all_index_ops_i32_index(gm.graph)


def _get_name_from_source(source) -> str:
    if isinstance(source, LocalSource):
        return source.local_name
    elif isinstance(source, GetItemSource):
        return f"{_get_name_from_source(source.base)}_{source.index}"
    else:
        raise NotImplementedError


def _flatten_placeholder_nodes(gm: GraphModule, example_kwargs: Mapping[str, Any]) -> None:
    placeholder_nodes_to_remove = []

    placeholder_nodes = [node for node in gm.graph.nodes if node.op == "placeholder"]

    # Add example value information to placeholder nodes.
    for placeholder_node in placeholder_nodes:
        example_val = example_kwargs[placeholder_node.name]
        placeholder_node.meta["val"] = example_val

    # Make inputs whose type is nested type of tensor to single tensors
    for placeholder_node in placeholder_nodes:
        placeholder_node._dynamo_source = LocalSource(placeholder_node.name)
        example_val = example_kwargs[placeholder_node.name]

        # For inputs with simple type (not list, tuple, ..), we don't need to do anything.
        if isinstance(example_val, (torch.Tensor, float, int, str)):
            placeholder_node.type = type(example_val)
            continue

        nodes_to_search: List[Tuple[Node, Optional[Source]]] = [(placeholder_node, None)]
        new_input_point_nodes_per_source_info: MutableMapping[Source, List[Node]] = defaultdict(
            list
        )

        # BFS while reaching simple tensor node.
        while nodes_to_search:
            node, prev_source_info = nodes_to_search.pop()
            assert isinstance(node, Node)

            if node.op == "placeholder":
                new_source_info: Source = LocalSource(placeholder_node.name)
                val = example_kwargs[placeholder_node.name]
            else:
                assert isinstance(prev_source_info, Source)
                args = map_arg(node.args, lambda n: n.meta["val"])
                kwargs = map_arg(node.kwargs, lambda n: n.meta["val"])
                val = node.target(*args, **kwargs)

                if node.op == "call_function" and node.target == operator.getitem:
                    # Update source info from previous one.
                    new_source_info = GetItemSource(prev_source_info, node.args[1])
                else:
                    assert node.op == "call_function" and isinstance(
                        node.target, torch._ops.OpOverload
                    )
                    continue

            node.meta["val"] = val

            if isinstance(val, (torch.Tensor, int, float)):
                # If current node's value type is tensor, don't search further for this node.
                # This node will become one of inputs (placeholders) of new GraphModule.
                new_input_point_nodes_per_source_info[new_source_info].append(node)
                continue

            # The node value is not tensor. Search further its children.
            for user in node.users:
                nodes_to_search.append((user, new_source_info))

        # Now we got all nodes to be replaced with new input nodes (input point nodes).
        for new_source_info, new_input_nodes in new_input_point_nodes_per_source_info.items():
            # Create new placeholder node that corresponds to `new_source_info`.
            with gm.graph.inserting_after(placeholder_node):
                new_placeholer_node = gm.graph.placeholder(_get_name_from_source(new_source_info))
            new_placeholer_node._dynamo_source = new_source_info
            new_placeholer_node.type = torch.Tensor
            new_placeholer_node.meta["val"] = new_input_nodes[0].meta["val"]

            # Replace existing input point nodes with new placeholder node.
            # Replaced nodes will be removed later through dead code elimination.
            for new_input_node in new_input_nodes:
                new_input_node.replace_all_uses_with(new_placeholer_node)
        placeholder_nodes_to_remove.append(placeholder_node)

    # We don't want setitem nodes to be eliminated by DCE.
    has_side_effect(operator.setitem)
    eliminate_dead_code(gm.graph)

    for placeholder_node in placeholder_nodes_to_remove:
        gm.graph.erase_node(placeholder_node)

    gm.recompile()


def get_param_file_with_cache(model: ModelCreationInfo, cache_dir: os.PathLike) -> Path:
    # Find if cached param file exists.
    model_hash = hash_model(
        model.metadata.get_optimized_cls(),
        model.metadata.config,
        model.metadata.quantization_config,
        model.get_qparam_qformat_path(),
        model.metadata.pretrained_id,
        model.seed,
        model.random_weight_model,
    )

    os.makedirs(cache_dir, exist_ok=True)

    cached_path = get_cache_path_if_exists(model_hash, "safetensors", cache_dir)
    if cached_path is None:
        # No cached param file exists. Model instantitation is unavoidable.
        logger.info(f"Failed to get parameter file from cache for model {model.metadata}")
        param_file_path = Path(cache_dir) / f"params-{model_hash}.safetensors"
        save_model(model.instantiate_model(), param_file_path, "safetensors")
        return param_file_path
    else:
        # Cached param file exists. Return it.
        logger.info(f"Found parameter file from cache for model {model.metadata}")
        return cached_path


def graph_with_interpreter(*args, gm: GraphModule):
    with torch.fx.traceback.preserve_node_meta():
        return torch.fx.Interpreter(gm).run(*args)


def get_aten_gm_from_symbolic_traced_gm(
    gm: GraphModule, example_kwargs: Mapping[str, Any]
) -> GraphModule:
    """Get ATen IR level fx graph from symbolic traced GraphModule (with torch.fx.symbolic_trace).

    Main difference from just calling `make_fx` is that this function generates exactlys same fx graph as calling both `torch._dynamo.export` and `make_fx` to the graph.
    For this, it flattens input/outputs of the graph and adds source information to flattened placeholder nodes.

    """

    # We don't want to affect original gm but share parameter/buffers.
    gm = GraphModule(gm, copy.deepcopy(gm.graph))

    # Flatten input (placeholder noodes) of the graph.
    _flatten_placeholder_nodes(gm, example_kwargs)

    # Lower the graph to ATen IR level.
    flattened_input = flatten_input_tensors(gm, example_kwargs)
    new_gm = trace_model(gm, flattened_input, {}, True, True, torch_ir_gm=gm)

    # Copy source info from original graph to lowered graph.
    for torch_ir_gm_ph, aten_gm_ph in zip(gm.graph.nodes, new_gm.graph.nodes):
        if torch_ir_gm_ph.op != "placeholder":
            assert aten_gm_ph.op != "placeholder"
            break
        if hasattr(torch_ir_gm_ph, "_dynamo_source"):
            aten_gm_ph._dynamo_source = torch_ir_gm_ph._dynamo_source

    # Flatten output
    # TODO: Do we need to add info about where each output comes from?
    output_node = next(iter(reversed(new_gm.graph.nodes)))
    assert output_node.op == "output"
    assert len(output_node.args) == 1
    output_node.args = (tree_flatten(output_node.args)[0],)

    # After make_fx, non-tensor placeholders becomes dead nodes but exist. They cannot be removed by `eliminate_dead_code`,
    # so remove them separately.
    for input_element, placeholder_node in zip(flattened_input, new_gm.graph.nodes):
        assert placeholder_node.op == "placeholder"
        if not isinstance(input_element, torch.Tensor):
            new_gm.graph.erase_node(placeholder_node)

    new_gm.recompile()

    return new_gm


def _get_input_layout(t) -> List[Tuple[str, Any]]:
    if isinstance(t, torch.Tensor):
        return [("", "Tensor")]
    elif isinstance(t, (tuple, list)):
        return [
            (f"[{i}]{input_name}", final_elem)
            for i, elem in enumerate(t)
            for input_name, final_elem in _get_input_layout(elem)
        ]
    elif isinstance(t, dict):
        return [
            (f"[{k}]{input_name}", final_elem)
            for k, v in t.items()
            for input_name, final_elem in _get_input_layout(v)
        ]
    elif isinstance(t, (str, int, float)):
        return [("", t)]
    else:
        raise ValueError(f"Unsupported type: {type(t)}")


def trace_model(
    model: torch.nn.Module,
    example_args: Sequence[Any],
    example_kwargs: Mapping[str, Any],
    aten_graph: bool,
    pre_dispatch: bool,
    torch_ir_gm: Optional[GraphModule] = None,
) -> GraphModule:
    flattened_inputs = tree_flatten((example_args, example_kwargs))[0]
    fake_mode = get_fake_mode(chain(model.parameters(), model.buffers(), flattened_inputs))

    # Always trace with fake inputs to avoid real computation.
    fake_args = tree_map_only(torch.Tensor, lambda t: fake_mode.from_tensor(t), example_args)
    fake_kwargs = tree_map_only(torch.Tensor, lambda t: fake_mode.from_tensor(t), example_kwargs)

    if pre_dispatch and not aten_graph:
        raise ValueError("`pre_dispatch` can be True only if `aten_graph` is True.")

    # Why is this needed? Somehow models might contain fake tensors
    # whose fake mode's `allows_non_fake_inputs` value is false.
    # In this case, this might cause problem during `make_fx` if there's
    # operator that creates tensor dynamically during executiion (e.g., torch.arange, torch.zeros)
    # because these dynamically created tensors are real tensors and operation between fake and real
    # tensors are not allowed if `allows_non_fake_inputs` is false.
    original_allow_non_fake_inputs = fake_mode.allow_non_fake_inputs
    fake_mode.allow_non_fake_inputs = True

    try:
        # If torch-IR level GraphModule is given, we don't need to run torch dynamo tracer again.
        if torch_ir_gm and aten_graph:
            assert not fake_kwargs

            # TODO: avoid calling `make_fx` and use torch.export.export instead.
            with enable_python_dispatcher():
                gm = make_fx(
                    partial(graph_with_interpreter, gm=torch_ir_gm),
                    pre_dispatch=pre_dispatch,
                    record_module_stack=True,
                )(*fake_args)

            # This is a workaround to make graphmodule serializable by torch graphmodule serializer.
            for node in gm.graph.nodes:
                if "nn_module_stack" not in node.meta:
                    continue
                for k, v in node.meta["nn_module_stack"].items():
                    node.meta["nn_module_stack"][k] = (v[0], f"{v[1].__module__}.{v[1].__name__}")

            # If `torch_ir_gm` was traced with dynamic shape, unused symbolic ops might remain after make_fx.
            # TODO: There might be other kinds of symbolic ops for other models.
            for node in gm.graph.nodes:
                if node.target == torch.ops.aten.sym_size:
                    assert not node.users
                    gm.graph.erase_node(node)
        else:
            torch._dynamo.reset()

            gm = torch._dynamo.export(
                model,
                aten_graph=aten_graph,
                tracing_mode="static",
                same_signature=False,
                pre_dispatch=pre_dispatch,
            )(*fake_args, **fake_kwargs)[0]

        return gm
    finally:
        fake_mode.allow_non_fake_inputs = original_allow_non_fake_inputs


def _get_aten_gm(
    fake_model: torch.nn.Module,
    example_args: Sequence,
    example_kwargs: Mapping,
) -> Tuple[GraphModule, GraphModule]:
    if isinstance(fake_model, GraphModule):
        # If the model is already GraphModule, assume it's in torch_ir level.
        # This pass exists for the case when calling this function inside torch.compile backend.
        aten_gm = trace_model(
            fake_model,
            example_args,
            example_kwargs,
            aten_graph=True,
            pre_dispatch=False,
            torch_ir_gm=fake_model,
        )

        return fake_model, aten_gm

    if isinstance(fake_model, QuantCausalLM):
        if example_args:
            raise NotImplementedError("We don't support fast tracing with example args.")

        # If the model is quantized, torch dynamo tracing is not needed. All we need is just `make_fx`.
        # First convert all positional arguments to keyword arguments.
        example_kwargs_copy = dict(example_kwargs)
        for arg_name, arg in zip(inspect.signature(fake_model).parameters.keys(), example_args):
            example_kwargs_copy[arg_name] = arg

        # Get actual graph module to be run
        is_prefill = fake_model._is_prefill(example_kwargs_copy)
        actual_gm = fake_model.prefill_model if is_prefill else fake_model.decode_model

        logger.info("Generating ATen graph from quantized model with fast tracing.")
        start = time()
        aten_gm = get_aten_gm_from_symbolic_traced_gm(actual_gm, example_kwargs_copy)

        logger.info(f"ATen graph generation and postprocess took {time() - start:.2f} seconds.")
        return aten_gm, aten_gm

    # Trace with ``aten_graph=False`` to find out input tensor order in traced FX graph.
    # Because input name information only remain when ``aten_graph=False``.
    torch_ir_gm = trace_model(fake_model, example_args, example_kwargs, False, False)

    # Flatten nested type inputs into tuple of tensors.
    # This matching process is not stable. Might work wrong for some inputs.
    # TODO: make this more robust.
    if example_args and example_kwargs:
        raise NotImplementedError("We do not support cases that both args and kwargs exist.")
    inputs = example_args or example_kwargs
    flattened_input = flatten_input_tensors(torch_ir_gm, inputs)

    # If model is Quantized model, trace with pre_dispatch=True. With this,
    # CompositeImplicitAutograd decomposition doesn't occur, and it's the right level
    # that MPPP config is bound to. For example, with CompositeImplicitAutograd decomposition,
    # matmul can be decomposed into bmm or mm with multiple view ops, which makes valid MPPP config
    # fails to propagate because of those flattening view ops.
    #
    # For more details about how matmul op is decomposed by CompositeImplicitAutograd,
    # refer to https://github.com/pytorch/pytorch/blob/6b1f13ea2f3b1bcd575620eecd7d84a4d2e3eb76/torch/_decomp/decompositions.py#L4166
    #
    # TODO: remove this and always trace with `pre_dispatch=True` .
    # For this, mppp configs should be rewritten.
    pre_dispatch = isinstance(fake_model, QuantCausalLM)

    # Get ATen level GraphModule
    aten_gm = trace_model(
        fake_model, flattened_input, {}, True, pre_dispatch, torch_ir_gm=torch_ir_gm
    )

    return torch_ir_gm, aten_gm


def _get_aten_graph_with_original_names(
    model: torch.nn.Module,
    example_args: Sequence,
    example_kwargs: Mapping,
    input_names: Optional[Sequence[str]] = None,
    output_names: Optional[Sequence[str]] = None,
) -> Tuple[GraphModule, GraphModule]:
    # Copy model to fake model to avoid any real computation or clone.
    flattened_args = tree_flatten(example_args)[0]
    flattened_kwargs = tree_flatten(example_kwargs)[0]
    fake_mode = get_fake_mode(
        chain(model.parameters(), model.buffers(), flattened_args, flattened_kwargs)
    )
    fake_mapping_mode = FakeCopyModeWithMapping(fake_mode)

    # `FakeCopyModeWithMapping` has a mapping from fake tensor to real tensor.
    with fake_mapping_mode:
        fake_model = copy.deepcopy(model)

    # # `Node._dynamo_source fields are not copied with deepcopy.copy. Copy them manually.`
    if isinstance(fake_model, GraphModule):
        for ph1, ph2 in zip(model.graph.nodes, fake_model.graph.nodes):
            assert ph1.op == ph2.op
            if ph1.op != "placeholder":
                break
            if dynamo_source_info := getattr(ph1, "_dynamo_source"):
                setattr(ph2, "_dynamo_source", dynamo_source_info)

    gm_with_dynamo_source_info, aten_gm = _get_aten_gm(
        fake_model,
        example_args,
        example_kwargs,
    )

    # Remove aten.sym_size nodes that are created due to dynamic shape tracing.
    for node in aten_gm.graph.nodes:
        if node.op == torch.ops.aten.sym_size:
            assert not node.users
            aten_gm.graph.erase_node(node)

    add_original_name_info(
        fake_model, gm_with_dynamo_source_info, aten_gm, input_names, output_names
    )
    add_qparam_info(fake_model, aten_gm)

    model_parameters = dict(model.named_parameters())
    model_buffers = dict(model.named_buffers())

    # Replace fake tensor constants which have original names and are original model's buffer or parameter with real ones.
    # This is needed because some constant fake tensors are cloned during tracing, which makes `FakeCopyModeWithMapping` impossible to match them.
    for node in aten_gm.graph.nodes:
        if node.op == "get_attr":
            target = recursive_getattr(aten_gm, node.target)
            if isinstance(target, FakeTensor):
                if not has_original_name(node):
                    continue
                original_name = get_original_name(node)
                original_tensor_constant: Union[torch.Tensor, torch.nn.Parameter]
                if original_name in model_parameters:
                    original_tensor_constant = model.get_parameter(get_original_name(node))
                elif original_name in model_buffers:
                    original_tensor_constant = model.get_buffer(get_original_name(node))
                else:
                    continue
                assert (
                    target.shape == original_tensor_constant.shape
                    and target.dtype == original_tensor_constant.dtype
                    and target.device == original_tensor_constant.device
                )

                target_path = node.target.rsplit(".", 1)

                if len(target_path) == 1:
                    setattr(aten_gm, node.target, original_tensor_constant)
                else:
                    setattr(
                        aten_gm.get_submodule(target_path[0]),
                        target_path[1],
                        original_tensor_constant,
                    )

    # Replace remaining fake tensor constants with real ones.
    fake_mapping_mode.set_fake_to_real(True)
    with fake_mapping_mode:
        aten_gm = copy.deepcopy(aten_gm)

    del fake_mapping_mode

    # Fill "tensor_meta" metadata from "example_value" metadata.
    # The result is same as calling ShapeProp, but more efficient.
    fill_tensor_meta_from_val_meta(aten_gm)

    return gm_with_dynamo_source_info, aten_gm


def get_aten_graph_with_original_names(
    model: Union[torch.nn.Module, ModelCreationInfo],
    example_args: Sequence,
    example_kwargs: Mapping,
    input_names: Optional[Sequence[str]] = None,
    output_names: Optional[Sequence[str]] = None,
    do_decompositions_for_model_rewrite: bool = False,
    cache_dir: Optional[os.PathLike] = None,
    param_file_info: Optional[ParamFileInfo] = None,
) -> Tuple[GraphModule, Tuple[torch.Tensor, ...]]:
    """Get ATen IR level fx graph from model whose nodes have original names.

    Returns:
        Tuple[GraphModule, Tuple[torch.Tensor, ...]]:
            ATen IR level fx graph and input that can be used to run returned GraphModule,
            made by flattening `example_args` and `example_kwargs`.
    """

    # Support GraphModule caching for only ModelMetadata model
    # TODO: add support for normal nn.Module model.
    do_cache = (
        cache_dir is not None and isinstance(model, ModelCreationInfo) and model.is_hashable()
    )
    if isinstance(model, ModelCreationInfo):
        original_type = model.metadata.get_optimized_cls()
        is_quantized = model.metadata.is_quantized
    else:
        original_type = get_original_model_type(model)
        is_quantized = isinstance(model, QuantCausalLM)

    # FIXME: This is hard binded to gptj mlperf slice model.
    is_quantized_gptj_mlperf_slice_prefill_model = (
        original_type is furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM
        and "causal_mask" in example_kwargs
        and is_quantized
    )

    if do_cache:
        assert cache_dir is not None
        gm_path = Path(cache_dir) / "graphmodules"
        gm_path.mkdir(parents=True, exist_ok=True)

        qformat_qparam_path = model.get_qparam_qformat_path()
        pretrained_id = model.metadata.pretrained_id
        model_config = model.metadata.config

        model_hash = hash_model(
            original_type,
            model_config,
            model.metadata.quantization_config,
            qformat_qparam_path,
            pretrained_id,
            model.seed,
            model.random_weight_model,
        )

        hash_val = get_env_independent_hash(
            (
                # We want to consider cpu and cuda version as same.
                # e.g., "2.4.1+cu121" and "2.4.1+cpu".
                torch.__version__.rsplit("+")[0],
                TRACER_VERSION,
                GRAPHMODULE_SERILAIZER_VERSION,
                model_hash,
                hash_example_inputs(example_args, example_kwargs),
            )
        )

        quantized_prefix = "Quantized_" if model.metadata.is_quantized else ""
        model_name = f"{quantized_prefix}{original_type.__module__}.{original_type.__name__}"

        cached_gm_file_path = get_cache_path_if_exists(hash_val, "fx", gm_path)

        if cached_gm_file_path:
            # Cached GraphModule exists. Load and return it.
            logger.info("use cached GraphModule")
            cached_gm = load_gm(cached_gm_file_path, fill_tensor_meta=True)
            # Flatten nested type inputs into tuple of tensors.
            # This matching process is not stable. Might work wrong for some inputs.
            # TODO: make this more robust.
            if example_args and example_kwargs:
                raise NotImplementedError(
                    "We do not support cases that both args and kwargs exist."
                )
            inputs = example_args or example_kwargs
            flattened_input = flatten_input_tensors(cached_gm, inputs)
            _preprocess_gm_for_model_rewrite(
                cached_gm,
                do_decompositions_for_model_rewrite,
                is_quantized_gptj_mlperf_slice_prefill_model=is_quantized_gptj_mlperf_slice_prefill_model,
            )
            return cached_gm, flattened_input

    # In most cases, output names in FX graph is not meaningful. Therefore, use predefined output names for each model.
    if output_names is None:
        try:
            if isinstance(model, ModelCreationInfo):
                cur_model: Union[torch.nn.Module, ModelMetadata] = model.metadata
            else:
                cur_model = model
            output_names = get_output_names(cur_model)
        except Exception:
            logger.warning(
                "Output tensor names will be obtained from FX graph. This might not be correct."
            )

    # Instantiate model if it's `ModelCreationInfo` and cache does not exist.
    if isinstance(model, ModelCreationInfo):
        model_creation_info = model
        model = model.instantiate_model()

    assert isinstance(model, torch.nn.Module)
    gm_with_dynamo_source_info, aten_gm = _get_aten_graph_with_original_names(
        model, example_args, example_kwargs, input_names, output_names
    )

    # Save GraphModule to cache dir.
    if do_cache:
        # Copy dynamo_source info from torch ir graph to aten graph.
        for torch_ir_gm_placeholder_node, aten_gm_placeholder_node in zip_equal(
            (node for node in gm_with_dynamo_source_info.graph.nodes if node.op == "placeholder"),
            (node for node in aten_gm.graph.nodes if node.op == "placeholder"),
        ):
            aten_gm_placeholder_node._dynamo_source = torch_ir_gm_placeholder_node._dynamo_source

        assert cache_dir

        existing_param_file_info = param_file_info
        if not existing_param_file_info:
            # If `param_file_info` is not given, find in cache_dir and create one if not exists.
            cached_param_file_path = get_param_file_with_cache(
                model_creation_info, Path(cache_dir) / "param_files"
            )
            existing_param_file_info = ParamFileInfo(
                cached_param_file_path.as_posix(), ParamfileFormat.SAFETENSORS
            )

        # Serialize and save the graphmodule.
        save_gm(
            aten_gm,
            gm_path / f"{model_name}-{hash_val}.fx",
            constant_tensor_path=gm_path / f"{model_name}-tensors-{hash_val}.safetensors",
            existing_param_file_info=existing_param_file_info,
            include_node_metadata=True,
        )

    _preprocess_gm_for_model_rewrite(
        aten_gm,
        do_decompositions_for_model_rewrite,
        is_quantized_gptj_mlperf_slice_prefill_model=is_quantized_gptj_mlperf_slice_prefill_model,
    )

    # Flatten nested type inputs into tuple of tensors.
    # This matching process is not stable. Might work wrong for some inputs.
    # TODO: make this more robust.
    if example_args and example_kwargs:
        raise NotImplementedError("We do not support cases that both args and kwargs exist.")
    inputs = example_args or example_kwargs
    flattened_input = flatten_input_tensors(gm_with_dynamo_source_info, inputs)

    return aten_gm, flattened_input
