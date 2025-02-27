from collections import defaultdict
from copy import deepcopy
from itertools import chain
import logging
import re
from typing import (
    AbstractSet,
    Callable,
    DefaultDict,
    Dict,
    Final,
    List,
    Mapping,
    Sequence,
    Tuple,
    Type,
    cast,
)

import torch
from torch._subclasses.fake_tensor import FakeCopyMode, FakeTensorMode
from torch.fx import GraphModule, Node
from torch.fx.passes.split_module import split_module
from torch.utils._pytree import tree_flatten, tree_unflatten

from furiosa_llm.parallelize.node_meta import get_original_name, set_color
from furiosa_llm.parallelize.utils import is_typecast_node

# TODO - Find a better way to adopt the block slicer to various models.
# This is the 1st layernorm weight name of GPT-J blocks.
GPTJ_FIRST_LAYERNORM_WEIGHT_PATTERN = r"transformer\.h\.\d+\.ln_1(\.org_target)?\.weight"
GPT2_FIRST_LAYERNORM_WEIGHT_PATTERN = r"transformer\.h\.\d+\.ln_1\.weight"

# This is layernorm biases' names in BERT's embedding or attention output layers.
BERT_EMBEDDING_OR_ATTENTION_OUTPUT_LAYERNORM_BIAS_PATTERN = r"(bert\.encoder\.layer\.\d+\.output\.LayerNorm(\.org_target)?\.bias)|(bert\.embeddings\.LayerNorm(\.org_target)?\.bias)"
ROBERTA_EMBEDDING_OR_ATTENTION_OUTPUT_LAYERNORM_BIAS_PATTERN = r"(roberta\.embeddings\.LayerNorm(\.org_target)?\.bias)|(roberta\.encoder\.layer\.\d+\.output\.LayerNorm(\.org_target)?\.bias)"
# This is the 1st rms norm weight name of Llama blocks.
# Second pattern is for matching weights in torch ir level graph generated from torchdynamo tracing.
LLAMA_FIRST_RMS_NORM_WEIGHT_PATTERN = r"(model\.layers\.\d+\.input_layernorm(\.org_target)?\.weight)|(L__self___model_layers(_slice_None__\d+__None__)?_\d+\_input_layernorm_weight)"


aten = torch.ops.aten


def _is_mcp_type_emulation(node: Node) -> bool:
    try:
        mcp_emulation_op_types = (
            torch.ops.furiosa.type_emulation_in.default,
            torch.ops.furiosa.type_emulation_out.default,
        )
    except AttributeError:
        logging.warning("torch.ops.furiosa has not been found, check mcp has been loaded")
        return False
    return node.target in mcp_emulation_op_types


def _get_children(
    node: Node,
    skip_type_emulation_nodes: bool = True,
    skip_typecast_nodes: bool = True,
    excludes: AbstractSet[Node] = frozenset(),
) -> List[Node]:
    maybe_children = [node for node in node.users if node not in excludes]

    children = []

    while maybe_children:
        candidate = maybe_children.pop()
        if (skip_type_emulation_nodes and _is_mcp_type_emulation(candidate)) or (
            skip_typecast_nodes and is_typecast_node(candidate)
        ):
            maybe_children.extend(candidate.users)
        else:
            children.append(candidate)
    return children


def _get_children_if_type_emulation(node: Node) -> Node:
    """Return child if child node is type emulation node. Otherwise return `node`."""
    if len(node.users) == 1 and _is_mcp_type_emulation(next(iter(node.users))):
        return next(iter(node.users))
    else:
        assert all(not _is_mcp_type_emulation(child) for child in node.users)
        return node


def _get_child_if_typecast_to_lower_precision(node: Node) -> Node:
    """Return child if child node is typecast node to lower precision. Otherwise return `node`."""
    if len(node.users) != 1:
        return node
    child = next(iter(node.users))

    # TODO: add other typecast ops
    if child.target == torch.ops.aten.to.dtype:
        dst_dtype = child.args[1]
    elif child.target == torch.ops.aten._to_copy.default:
        if "dtype" in child.kwargs:
            dst_dtype = child.kwargs["dtype"]
        else:
            return node
    else:
        return node

    cur_dtype = node.meta["tensor_meta"].dtype
    assert isinstance(dst_dtype, torch.dtype)

    # Return child only if child is typecast node to lower-precision dtype.
    if torch.finfo(cur_dtype).bits > torch.finfo(dst_dtype).bits:
        return child
    else:
        return node


def _get_parent_with_index(
    node: Node,
    arg_index: int,
    skip_type_emulation_nodes: bool = True,
    skip_typecast_nodes: bool = True,
) -> Node:
    parent = node.args[arg_index]
    if not isinstance(parent, Node):
        raise ValueError("`node`'s specified parent is not a Node")

    while True:
        if (skip_type_emulation_nodes and _is_mcp_type_emulation(parent)) or (
            skip_typecast_nodes and is_typecast_node(parent)
        ):
            # Because we only consider ops with only one parent.
            assert len(parent.all_input_nodes) == 1
            parent = parent.all_input_nodes[0]
        else:
            break

    return parent


def _get_parents(
    node: Node,
    skip_type_emulation_nodes: bool = True,
    skip_typecast_nodes: bool = True,
    excludes: AbstractSet[Node] = frozenset(),
) -> List[Node]:
    maybe_parents = [node for node in node.all_input_nodes if node not in excludes]

    parents = []

    while maybe_parents:
        candidate = maybe_parents.pop()
        if (skip_type_emulation_nodes and _is_mcp_type_emulation(candidate)) or (
            skip_typecast_nodes and is_typecast_node(candidate)
        ):
            maybe_parents.extend(candidate.all_input_nodes)
        else:
            parents.append(candidate)

    return parents


def is_power_of_two(num: int) -> bool:
    return num > 0 and num & (num - 1) == 0


def log_2(num: int) -> int:
    return len(bin(num)) - 3


def _get_only_live_child(node: Node) -> Node:
    live_children = [child for child in node.users if child.users]
    if len(live_children) > 1:
        raise ValueError("Node has more than one live child")
    return live_children[0]


def get_attention_output_layernorm_edge_names(
    gm: torch.fx.GraphModule,
    layernorm_bias_patterns: str,
) -> List[List[Tuple[str, str]]]:
    """Get outgoing edges from layernorm layers with ``layernorm_bias_patterns``."""
    param_constants = (
        n for n in gm.graph.nodes if n.op == 'get_attr' and n.name.startswith("_param")
    )
    layernorm_biases = [
        n for n in param_constants if re.search(layernorm_bias_patterns, get_original_name(n))
    ]
    # Remove the last layernorm bias node because layernorm exists at the end of each block
    # and we will find the boundary by going down from the layernorm node.
    if layernorm_biases:
        layernorm_biases.pop()
    if not layernorm_biases:
        raise ValueError("Layernorm bias not found")
    num_blocks = len(layernorm_biases)
    adds_or_layernorms = [x for y in layernorm_biases for x in _get_children(y)]

    # For this case, logic for finding target node is same regardless of whether layernorm was decomposed or not.
    # Always layernorm_bias's child node is the final node of the layernorm operation.
    _check_nodes_with_exepected_ops(
        adds_or_layernorms,
        {
            torch.ops.aten.add.Tensor,
            torch.ops.aten.layer_norm.default,
            torch.ops.aten.native_layer_norm.default,
        },
    )

    # torch.ops.aten.native_layer_norm.default produces multiple tensors and we expect only one child is live.
    if adds_or_layernorms[0].target == torch.ops.aten.native_layer_norm.default:
        xs = [_get_only_live_child(x) for x in adds_or_layernorms]
    else:
        xs = adds_or_layernorms

    xs = [_get_child_if_typecast_to_lower_precision(_get_children_if_type_emulation(x)) for x in xs]

    if len(xs) != num_blocks:
        raise ValueError("Failed to get same number of nodes as blocks")

    x_out_edges = [[(x.name, dst.name) for dst in x.users.keys()] for x in xs]

    return x_out_edges


def _get_nodes_not_with_expected_op(
    nodes: Sequence[Node], expected_ops: AbstractSet[Callable]
) -> Tuple[Node, ...]:
    return tuple(node for node in nodes if node.target not in expected_ops)


def get_first_layernorm_edge_names(
    gm: torch.fx.GraphModule,
    first_layernorm_weight_pattern: str,
) -> List[List[Tuple[str, str]]]:
    """Get the first layernorm's input's output edges' names for each layer.

        +------------------+     +-----+
        | layernorm_weight | --> | mul | <----+
        +------------------+     +-----+      |
                                              |
    +-----+     +-------+     +------+     +-----+
    | pow | <-- |   x   | --> | mean | --> | sub |
    +-----+     +-------+     +------+     +-----+
                  |   |                       ^
    next layer <--+   +-----------------------+

    Starts from layernorm_weight and returns x's 4 out edges for each layer
    """
    param_constants = [
        n for n in gm.graph.nodes if n.op == 'get_attr' and n.name.startswith("_param")
    ]
    first_layernorm_weights = [
        n
        for n in param_constants
        if re.search(first_layernorm_weight_pattern, get_original_name(n))
    ]
    num_blocks = len(first_layernorm_weights)

    if not first_layernorm_weights:
        raise ValueError("First layernorm weights not found")
    muls_or_layernorms = [x for y in first_layernorm_weights for x in _get_children(y)]

    if all(x.target == torch.ops.aten.mul.Tensor for x in muls_or_layernorms):
        # Layernorm has been decomposed
        subs = [
            parent
            for parents in map(_get_parents, muls_or_layernorms)
            for parent in parents
            if parent not in first_layernorm_weights
        ]
        _check_nodes_with_exepected_ops(
            subs,
            {
                torch.ops.aten.sub.Tensor,
            },
        )
        xs = [_get_parent_with_index(n, 0) for n in subs]
    elif all(
        x.target in (torch.ops.aten.layer_norm.default, torch.ops.aten.native_layer_norm.default)
        for x in muls_or_layernorms
    ):
        # Layernorm was not decomposed
        # Get "input" parents for layernorm, which is first arg,
        xs = [_get_parent_with_index(layernorm, 0) for layernorm in muls_or_layernorms]
    else:
        not_mul_or_layernorm_ops = _get_nodes_not_with_expected_op(
            muls_or_layernorms,
            {
                torch.ops.aten.mul.Tensor,
                torch.ops.aten.layer_norm.default,
                torch.ops.aten.native_layer_norm.default,
            },
        )
        raise ValueError(
            "Unexpected node type. expected: mul or layernorm, got: {}".format(
                not_mul_or_layernorm_ops[0].target
            )
        )

    if len(xs) != num_blocks:
        raise ValueError("Failed to get same number of nodes as blocks")
    xs = [_get_child_if_typecast_to_lower_precision(x) for x in xs]
    x_out_edges = [[(x.name, dst.name) for dst in x.users.keys()] for x in xs]

    return x_out_edges


def _check_nodes_with_exepected_ops(
    nodes: Sequence[Node], expected_ops: AbstractSet[Callable]
) -> None:
    unexpected_nodes = _get_nodes_not_with_expected_op(nodes, expected_ops)
    if unexpected_nodes:
        unexpected_ops = set(node.target for node in unexpected_nodes)
        raise ValueError(f"Unexpected node type. expected: {expected_ops}, got: {unexpected_ops}")


def get_first_rms_norm_edge_names(
    gm: torch.fx.GraphModule,
    first_rms_norm_weight_pattern: str,
) -> List[List[Tuple[str, str]]]:
    param_constants = (
        n for n in gm.graph.nodes if n.op == 'get_attr' and n.name.startswith("_param")
    )

    first_rms_norm_weights = tuple(
        n for n in param_constants if re.search(first_rms_norm_weight_pattern, get_original_name(n))
    )
    num_blocks = len(first_rms_norm_weights)
    if not first_rms_norm_weight_pattern:
        raise ValueError("First rms norm weights not found")

    muls = tuple(x for y in first_rms_norm_weights for x in _get_children(y))
    _check_nodes_with_exepected_ops(
        muls,
        {
            torch.ops.aten.mul.Tensor,
        },
    )

    muls_2 = tuple(_get_parents(x, excludes={cast(Node, x.args[0])})[0] for x in muls)
    _check_nodes_with_exepected_ops(
        muls_2,
        {
            torch.ops.aten.mul.Tensor,
        },
    )

    add_or_embeddings = tuple(
        _get_parents(mul, excludes={cast(Node, mul.args[1])})[0] for mul in muls_2
    )
    _check_nodes_with_exepected_ops(
        add_or_embeddings, {torch.ops.aten.add.Tensor, torch.ops.aten.embedding.default}
    )

    if len(add_or_embeddings) != num_blocks:
        raise ValueError("Failed to get same number of nodes as blocks")

    xs = [_get_child_if_typecast_to_lower_precision(x) for x in add_or_embeddings]
    add_out_edges = [[(add.name, dst.name) for dst in add.users] for add in xs]

    return add_out_edges


def mark_color_to_node_meta(
    node_to_color: Mapping[str, Sequence[int]], node_name_to_node: Mapping[str, Node]
) -> None:
    """Assigns colors to the meta attribute of nodes in-place.

    `node_to_color` is a mapping of node names to colors, and `node_name_to_node` is a mapping of
    node names to Node objects. This function modifies the Node objects by reference, meaning the
    original objects are changed. You can create node_name_to_node by
    `{node.name: node for node in gm.graph.nodes}`

    Args:
        node_to_color (Dict[str, int]): A mapping of node names to colors.
        node_name_to_node (Dict[str, Node]): A mapping of node names to Node objects.
    """
    for node_name, color in node_to_color.items():
        set_color(node_name_to_node[node_name], color)


def bitmap_to_binary_digits(bitmap: int) -> Tuple[int, ...]:
    """Converts a bitmap to a tuple of integers (binary digits).

    Args:
        bitmap (int): The input bitmap.

    Returns:
        Tuple[int]: A tuple of integers (binary digits).
    """
    return tuple(i for i, bit in enumerate(reversed(f"{bitmap:b}")) if bit == '1')


def get_blockwise_sliced_color_map(
    gm: torch.fx.GraphModule,
    split_edges: Sequence[Sequence[Tuple[str, str]]],
    mark_common_ancestor_as_first_layer: bool = False,
    mark_color_to_meta: bool = True,
) -> Dict[str, Tuple[int, ...]]:
    """Assigns a unique color to each node in the graph based on the specified split edges.

    If `mark_common_ancestor_as_first_layer` is True, the common ancestor of all nodes is marked as
    the first layer (i.e., color 1). If `mark_color_to_meta` is True, the color is assigned to the
    meta attribute of the nodes.

    Args:
        gm: The input graph module.
        split_edges: A Sequence of sequences where each inner list represents a stage boundaries,
            and each tuple within the inner list represents an edge between two node names (source,
            destination) indicating the split points for that stage.
        mark_common_ancestor_as_first_layer: If True, the common ancestor of all nodes is marked as
            the first layer (i.e., color 1).
        mark_color_to_meta: If True, the color is assigned to the meta attribute of the nodes.

    Returns:
        Dict[str, int]: A dictionary mapping each node name to its assigned color.
    """
    node_name_to_node = {node.name: node for node in gm.graph.nodes}
    node_to_bitmap: DefaultDict[str, int] = defaultdict(int)
    layer_count = len(split_edges)

    # visit from the last layer (we stop propagating if node is already colored)
    for i, stage_split_points in enumerate(reversed(split_edges)):
        current_color = 1 << (layer_count - i - 1)
        # Mypy differs chain type from iterator type :<
        to_visits = chain(iter(dst for _, dst in stage_split_points))
        while True:
            # explore new node by calling next, break if to_visits is empty
            if (node_name := next(to_visits, None)) is None:
                break
            if node_to_bitmap[node_name]:
                continue
            node_to_bitmap[node_name] |= current_color
            # no more memory required cause we're using dict's iterator
            to_visits = chain(
                to_visits, iter(x.name for x in iter(node_name_to_node[node_name].users))
            )

    nodes_to_color = {node.name for node in gm.graph.nodes if node_to_bitmap[node.name] == 0}

    # loop until all nodes are colored.
    while nodes_to_color:
        num_nodes_to_color = len(nodes_to_color)
        # propagate color to blank ancestors
        need_coloring = set()
        for n in reversed(gm.graph.nodes):
            for x in n.all_input_nodes:
                if node_to_bitmap[x.name] == 0:
                    need_coloring.add(x.name)
                if x.name in need_coloring:
                    node_to_bitmap[x.name] |= node_to_bitmap[n.name]
                    if node_to_bitmap[x.name] != 0:
                        nodes_to_color.discard(x.name)

        # Color dead nodes that are not colored.
        for n in gm.graph.nodes:
            if node_to_bitmap[n.name] == 0:
                if n.users and any(node_to_bitmap[user.name] != 0 for user in n.users):
                    raise ValueError(f"Node {n.name} is not dead node but not colored")
                parent_colors = set(node_to_bitmap[parent.name] for parent in n.all_input_nodes)
                parent_colors.discard(0)
                if len(parent_colors) == 0:
                    continue
                elif len(parent_colors) != 1:
                    raise ValueError(
                        f"Node {n.name} is dead node but its parents has different colors"
                    )
                node_to_bitmap[n.name] = next(iter(parent_colors))
                nodes_to_color.discard(n.name)
        if num_nodes_to_color == len(nodes_to_color):
            break

    for node in gm.graph.nodes:
        if node_to_bitmap[node.name] == 0:
            if node.op == "output" and not node.args[0]:
                # No output tensor: output node is dead. Don't need to color it.
                continue
            raise ValueError(f"node {node.name} was not colored")

    # to prevent unwanted behavior (ex. node_to_color['non-exist'] = 0)
    node_to_bitmap.default_factory = None

    # mark common anncesstor with first layer (i.e. 1)
    if mark_common_ancestor_as_first_layer:
        for n in gm.graph.nodes:
            # if all bits are set, it means it's common ancestor of all nodes
            colors = bitmap_to_binary_digits(node_to_bitmap[n.name])
            if len(colors) > 1:
                if len(colors) != layer_count:
                    raise ValueError(
                        "This graph has node that shared by some blocks. This cannot be made as common ancestor."
                    )
                node_to_bitmap[n.name] = 1

    node_to_color: Dict[str, Tuple[int, ...]] = {}
    for n in gm.graph.nodes:
        color_bitmap = node_to_bitmap[n.name]
        node_to_color[n.name] = bitmap_to_binary_digits(color_bitmap)

    if mark_color_to_meta:
        mark_color_to_node_meta(node_to_color, node_name_to_node)

    return node_to_color


MODEL_ARCH_TO_BLOCK_SPLITTER_AND_WEIGHT_NODE_PATTERN: Final[
    Dict[str, Tuple[Callable[[GraphModule, str], List[List[Tuple[str, str]]]], str]]
] = {
    "GPTJForCausalLM": (get_first_layernorm_edge_names, GPTJ_FIRST_LAYERNORM_WEIGHT_PATTERN),
    "GPT2LMHeadModel": (get_first_layernorm_edge_names, GPT2_FIRST_LAYERNORM_WEIGHT_PATTERN),
    "BertForQuestionAnswering": (
        get_attention_output_layernorm_edge_names,
        BERT_EMBEDDING_OR_ATTENTION_OUTPUT_LAYERNORM_BIAS_PATTERN,
    ),
    "RobertaForQuestionAnswering": (
        get_attention_output_layernorm_edge_names,
        ROBERTA_EMBEDDING_OR_ATTENTION_OUTPUT_LAYERNORM_BIAS_PATTERN,
    ),
    "LlamaForCausalLM": (get_first_rms_norm_edge_names, LLAMA_FIRST_RMS_NORM_WEIGHT_PATTERN),
}


def get_block_slicing_edges(
    gm: GraphModule, original_model_type: Type[torch.nn.Module]
) -> List[List[Tuple[str, str]]]:
    original_model_type_name = original_model_type.__name__

    if block_slicing_info := MODEL_ARCH_TO_BLOCK_SPLITTER_AND_WEIGHT_NODE_PATTERN.get(
        original_model_type_name
    ):
        block_slicing_function, weight_node_pattern = block_slicing_info
        return block_slicing_function(gm, weight_node_pattern)
    else:
        raise NotImplementedError(f"Block slicing for {original_model_type_name} is not supported.")


def get_blockwise_sliced_gms(
    original_gm: torch.fx.GraphModule,
    node_to_color: Mapping[str, Sequence[int]],
    common_ancestor_as_first_layer: bool = False,
    keep_original_order: bool = False,
) -> List[Tuple[int, torch.fx.GraphModule]]:
    """Slices the input graph module into multiple graph modules based on the assigned colors.

    Args:
        original_gm: The input graph module.
        node_to_color: A dictionary mapping each node name to its assigned color.
        common_ancestor_as_first_layer: If True, assumes the common ancestor of all nodes is marked
            as the first layer (i.e., color 1).
        keep_original_order: If True, the original order of the graph modules is preserved.

    Returns:
        List[Tuple[int, torch.fx.GraphModule]]: A list of tuples where each tuple contains the
            color and the corresponding sliced graph module.
    """
    colors = set(node_to_color.values())
    gms = []

    for color in colors:
        if common_ancestor_as_first_layer:

            def key(x):
                assert len(node_to_color[x.name]) == 1
                return node_to_color[x.name][0]

        else:
            if len(color) != 1:
                continue

            # if common part, return current `color` else return node's annotated color
            def key(x):
                node_color = node_to_color[x.name]
                if len(node_color) != 1:
                    return color[0]
                return node_color[0]

        with FakeTensorMode(allow_non_fake_inputs=True) as mode:
            with FakeCopyMode(mode):
                gm = deepcopy(original_gm)
        # To avoid the circular depency error, delete [common] -> [rest color] edges
        for n in gm.graph.nodes:
            if node_to_color[n.name] != color:
                # if [x] -> [n] is [common] -> [rest color] edge, replace x with dummy node
                raw_args, specs = tree_flatten((n.args, n.kwargs))
                for i, x in enumerate(raw_args):
                    if (
                        isinstance(x, torch.fx.Node)
                        and node_to_color[x.name] != node_to_color[n.name]
                        and len(node_to_color[x.name]) > 1
                    ):
                        raw_args[i] = None
                n.args, n.kwargs = tree_unflatten(raw_args, specs)
        gm.recompile()

        # FIXME: there's a bug (KeyError raised) if `keep_original_order=True`
        sliced = split_module(gm, None, key, keep_original_order=keep_original_order)

        gms.append((color[0], deepcopy(getattr(sliced, f"submod_{color[0]}"))))
        # hopefully release memory
        del sliced, gm

    return gms
