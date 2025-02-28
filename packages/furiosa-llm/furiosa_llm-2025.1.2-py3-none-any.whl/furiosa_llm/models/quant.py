# Most of code is copied from npu-tools/crates/npu-torch-models/pymodels/model_quantize/transformers_llm.py
# https://github.com/furiosa-ai/npu-tools/blob/daaed216eb409bc1e84afe0a582b9e417f1d7876/crates/npu-torch-models/pymodels/model_quantize/transformers_llm.py
from itertools import chain
import logging
import os
import tempfile
from time import time
import typing
from typing import AbstractSet, Any, Dict, Mapping, Optional, Sequence, Set, Tuple

import furiosa_llm_models
from furiosa_llm_models.symbolic.helper import CustomHFTracer
import model_compressor as mcp  # type: ignore
import torch
from torch.fx import GraphModule
from transformers import PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithPast  # type: ignore
from transformers.utils.import_utils import is_torch_fx_proxy  # type: ignore

from .config_types import Bucket, KvCacheSharingAcrossBeamsConfig, PagedAttentionConfig

if typing.TYPE_CHECKING:
    from .metadata import ModelMetadata

SAMPLE_PREFILL_BUCKET = Bucket.prefill(4, 128)
SAMPLE_DECODE_BUCKET = Bucket.decode(4, 256)
SAMPLE_PAGED_ATTENTION_CONFIG = PagedAttentionConfig(4096, 1)
SAMPLE_KVCACHE_SHARING_ACROSS_BEAMS_CONFIG = KvCacheSharingAcrossBeamsConfig(4, 128)


logger = logging.getLogger(__file__)


def fx_symbolic_trace_model(
    model: torch.nn.Module,
    input_names: AbstractSet[str],
    custom_concrete_args: Optional[Mapping[str, Any]] = None,
) -> torch.fx.GraphModule:
    from transformers.utils.fx import get_concrete_args  # type: ignore

    concrete_args = get_concrete_args(model, list(input_names))
    if custom_concrete_args is not None:
        concrete_args.update(custom_concrete_args)

    tracer = CustomHFTracer()
    traced_graph = tracer.trace(model, concrete_args=concrete_args)
    traced = torch.fx.GraphModule(model, traced_graph)

    traced.config = model.config
    # The model class must be stored as an attribute to allow model deserialization, which uses trace, and thus
    # _generate_dummy_input, where the model class is needed.
    traced.class_for_deserialization = model.__class__
    traced.device = model.device
    traced.module_name = f"{model.__class__.__module__}.{model.__class__.__name__}"

    return traced


def torchdynamo_trace_model(
    model: torch.nn.Module,
    example_kwargs: Mapping[str, Any],
) -> torch.fx.GraphModule:
    return torch._dynamo.export(model, tracing_mode="symbolic", aten_graph=False)(**example_kwargs)[
        0
    ]


def torch_gather_i32(
    x: torch.Tensor, dim: int, index: torch.Tensor, *, sparse_grad: bool = False
) -> torch.Tensor:
    return torch.ops.furiosa.gather_i32.default(x, dim, index, sparse_grad)


# FIXME: move this to PipelineBuilder
def _replace_torch_gather_with_gather_i32(
    gm: torch.fx.GraphModule,
) -> None:
    for node in gm.graph.nodes:
        if node.target != torch.gather:
            continue
        if len(node.args) == 3 and isinstance(node.args[1], int):
            node.target = torch_gather_i32
        else:
            raise NotImplementedError("We don't support this form of torch.gather op yet.")
    gm.recompile()


def _load_params_from_bin_file(
    quantized_model: GraphModule, quant_ckpt_file_path: os.PathLike
) -> None:
    assert quantized_model.device == torch.device("meta")
    mcp.load_qckpt(
        quantized_model, os.fspath(quant_ckpt_file_path), map_location=torch.device("cpu")
    )


# Borrowed from https://github.com/furiosa-ai/npu-tools/blob/daaed216eb409bc1e84afe0a582b9e417f1d7876/crates/npu-torch-models/pymodels/model_quantize/quant_causal.py
class QuantCausalLM(PreTrainedModel):
    """This is a wrapper class around quantized models to mimic behavior of original model."""

    def __init__(
        self,
        model: PreTrainedModel,
        prefill_graph: GraphModule,
        decode_graph: Optional[GraphModule],
        qparam_path: os.PathLike,
        qformat_path: os.PathLike,
        quant_ckpt_file_path: Optional[os.PathLike],
    ):
        # order matters
        self.original_type = type(model)
        self.qparam_path = qparam_path
        self.qformat_path = qformat_path
        super().__init__(model.config)

        need_parameter_load = any(
            t.device == torch.device("meta") for t in chain(model.parameters(), model.buffers())
        )

        logger.info(
            f"Quantizing model: {type(model)}, qparam: {qparam_path}, qformat: {qformat_path}"
        )
        start = time()

        with tempfile.TemporaryDirectory() as tmp_dir:
            if decode_graph:
                quantsim_model = mcp.FXGraphCausalLM(
                    self.original_type, prefill_graph, decode_graph
                )
            else:
                quantsim_model = prefill_graph

            try:
                self.model = mcp.create_quantsim_model(
                    quantsim_model,
                    qformat_path=os.fspath(qformat_path),
                    qparam_path=os.fspath(qparam_path),
                    qlevel=4,
                    target_machine='RGDA0',
                    decode_phase=False,
                    output_path=tmp_dir,
                )
            except (KeyError, TypeError):
                # Retry with `disable_auto_node_mapping=True`. With this option, model is splitted into layers with model class-specific rules,
                # instead of using general transformer block pattern matching algorithm.
                # This general pattern matching algorithm might doesn't work for the following cases. Auto node mapping should be disabled for them:
                # - model's number of layers (transformer / bert blocks) is smaller than 3.
                # - quantization artifacts for model with larger number of layers is used.
                logger.info(
                    "Failed to quantize with `disable_auto_node_mapping=False`, retry with `disable_auto_node_mapping=True`."
                )
                self.model = mcp.create_quantsim_model(
                    quantsim_model,
                    qformat_path=os.fspath(qformat_path),
                    qparam_path=os.fspath(qparam_path),
                    qlevel=4,
                    target_machine='RGDA0',
                    decode_phase=False,
                    output_path=tmp_dir,
                    disable_auto_node_mapping=True,
                )

            if decode_graph:
                self.prefill_model = self.model.prefill_model
                self.decode_model = self.model.decode_model
            else:
                self.prefill_model = self.model

            # Replace gathers with gather_i32 for gptj_mlperf_* models.
            replace_gathers_with_gather_i32 = isinstance(
                model,
                (
                    furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
                    furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
                    furiosa_llm_models.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
                    furiosa_llm_models.gptj.symbolic.paged_attention_rope.GPTJForCausalLM,
                    furiosa_llm_models.gptj.symbolic.paged_attention.GPTJForCausalLM,
                    furiosa_llm_models.gptj.symbolic.tta_submission.GPTJForCausalLM,
                ),
            )

        if need_parameter_load:
            if quant_ckpt_file_path is None:
                raise ValueError(
                    "`quant_ckpt_file_path` is required when quantization is done by loading quantized parameter directly."
                )
            _load_params_from_bin_file(self.model, quant_ckpt_file_path)

        logger.info(f"Quantization done, elapsed: {time() - start:.2f}s")

        if replace_gathers_with_gather_i32:
            # FIXME: do this in PipelineBuilder at aten level and make logic more general.
            # Replace torch.gather ops to make position_ids's dtype i32.
            _replace_torch_gather_with_gather_i32(self.model.prefill_model)

            if decode_graph:
                _replace_torch_gather_with_gather_i32(self.model.decode_model)

        self._merge_duplicate_parameters()

    def _merge_duplicate_parameters(self) -> None:
        if not hasattr(self, "decode_model") or self.prefill_model is self.decode_model:
            return
        # merge duplicated parameters.
        decode_model_param_and_buffers = dict(
            chain(self.decode_model.named_parameters(), self.decode_model.named_buffers())
        )
        for name, param_in_prefill in tuple(
            chain(self.prefill_model.named_parameters(), self.prefill_model.named_buffers())
        ):
            param_in_decode = decode_model_param_and_buffers.get(name)
            if param_in_decode is None or not param_in_decode.equal(param_in_prefill):
                continue

            # Two param or buffer types should be same.
            assert type(param_in_prefill) is type(param_in_decode)
            submodule_name, final_attr_name = name.rsplit(".", maxsplit=1)
            submodule = self.decode_model.get_submodule(submodule_name)

            # To ensure memory deallocation.
            delattr(submodule, final_attr_name)
            setattr(submodule, final_attr_name, param_in_prefill)

    def _is_prefill(self, kwargs: Mapping[str, Any]) -> bool:
        if self.original_type in (
            furiosa_llm_models.gptj.symbolic.huggingface.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.preallocated.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.preallocated_concat.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.huggingface_rope_rngd_gelu.GPTJForCausalLM,
        ):
            return kwargs.get("past_key_values", None) is None
        elif (
            self.original_type
            == furiosa_llm_models.gptj.symbolic.paged_attention_rope.GPTJForCausalLM
        ):
            # paged_attention_rope model has same model for prefill/decode.
            return True
        elif self.original_type in (
            furiosa_llm_models.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.tta_submission.GPTJForCausalLM,
            furiosa_llm_models.llama.symbolic.mlperf_submission.LlamaForCausalLM,
            furiosa_llm_models.llama.symbolic.mlperf_submission_slice.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.mlperf_submission.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.aramco_specdec.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.aramco_specdec_slice_integrated.LlamaForCausalLM,
        ):
            # For paged_attention_optimized_packed_rope model, prefill / decode cannot be distinguished with the presence of past_key_values.
            # Instead, past_valid_key_indices can be used.
            return kwargs.get("past_valid_key_indices", None) is None
        elif self.original_type in (
            furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
        ):
            return kwargs.get("past_valid_key_prompt_indices", None) is None
        elif self.original_type in (
            furiosa_llm_models.bert.symbolic.mlperf_submission.BertForQuestionAnswering,
            furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
        ):
            return True
        else:
            raise ValueError(f"Invalid model: {self}")

    # Doesn't use kwargs for maintain same signature as original Model. This information will be used for input matching in PipelineBuilder.
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        **kwargs,
    ):
        if is_torch_fx_proxy(input_ids):
            # in tracing
            output = self.model(input_ids=input_ids, position_ids=position_ids, **kwargs)
        else:
            # This is needed for this module to support GenerationMixin.generate method.
            # FIXME
            for key in tuple(kwargs.keys()):
                if kwargs[key] is None:
                    del kwargs[key]
            output = self.model(input_ids=input_ids, position_ids=position_ids, **kwargs)

        if return_dict:
            # we assume that this option is only used by huggingface generator and `labels` shold be None.
            # output `loss` is None if `labels` is None.
            assert kwargs.get("labels", None) is None
            # First element of `CausalLMOutputWithPast` is loss.
            assert isinstance(output, Sequence)
            return CausalLMOutputWithPast(None, *output)
        else:
            return output

    # Without ``attention_mask=None``, error occurs from ``GenerationMixin``'s unused argument check.
    # https://github.com/huggingface/transformers/blob/d502bd64756535ff6af43cbc5a15aa5da7f52483/src/transformers/generation/utils.py#L1155
    def prepare_inputs_for_generation(self, input_ids, attention_mask=None, **model_kwargs):
        return self.original_type.prepare_inputs_for_generation(
            self, input_ids, attention_mask=attention_mask, **model_kwargs
        )

    def _reorder_cache(
        self, past_key_values: Tuple[Tuple[torch.Tensor]], beam_idx: torch.Tensor
    ) -> Tuple[Tuple[torch.Tensor]]:
        """
        This function is used to re-order the `past_key_values` cache if [`~PretrainedModel.beam_search`] or
        [`~PretrainedModel.beam_sample`] is called. This is required to match `past_key_values` with the correct
        beam_idx at every generation step.
        """
        assert issubclass(self.original_type, PreTrainedModel)
        return self.original_type._reorder_cache(self, past_key_values, beam_idx)

    def can_generate(self):
        return self.original_type.can_generate()


BUCKET_SIZE_ARG_NAME = "bucket_size"


def _get_input_names_and_concrete_args_for_symbolic_trace(
    model: PreTrainedModel,
):
    prefill_concrete_args: Dict[str, Any] = {}
    decode_input_names: Optional[Set[str]] = None
    decode_concrete_args = None

    if isinstance(
        model,
        (
            furiosa_llm_models.gptj.symbolic.huggingface.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.huggingface_rope_rngd_gelu.GPTJForCausalLM,
        ),
    ):
        prefill_concrete_args = decode_concrete_args = {
            'return_dict': False,
            'use_cache': True,
            'output_attentions': False,
            'output_hidden_states': False,
        }
        prefill_input_names = {'input_ids', 'attention_mask', 'position_ids'}
        decode_input_names = {*prefill_input_names, 'past_key_values'}
    elif isinstance(model, furiosa_llm_models.gptj.symbolic.paged_attention_rope.GPTJForCausalLM):
        prefill_input_names = {
            'input_ids',
            'past_key_values',
            'position_ids',
            'attention_mask',
            "input_metadata",
        }
        prefill_concrete_args = {
            'use_cache': False,
            'return_dict': False,
            'output_attentions': False,
            'output_hidden_states': False,
        }
    elif isinstance(model, furiosa_llm_models.llama.symbolic.huggingface.LlamaForCausalLM):
        prefill_input_names = {"input_ids"}
        decode_input_names = {*prefill_input_names, "past_key_values"}

        prefill_concrete_args = decode_concrete_args = {
            "return_dict": True,
            "use_cache": True,
            "output_attentions": False,
            "output_hidden_states": False,
        }

    elif isinstance(
        model,
        (
            furiosa_llm_models.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.tta_submission.GPTJForCausalLM,
        ),
    ):
        # `furiosa_llm_models.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM`
        # model has different concrete_args for tracing for prefill and decode mode.
        prefill_input_names_, prefill_concrete_args = model.get_input_names_and_concrete_args(model)
        decode_input_names_, decode_concrete_args = model.get_input_names_and_concrete_args(
            model, prefill_phase=False
        )

        assert isinstance(decode_concrete_args, dict)

        # We want to concretize bucket size after quantization.
        prefill_input_names = set(prefill_input_names_)
        # bucket_size arg is not used when it's prefill phase.
        try:
            prefill_input_names.remove(BUCKET_SIZE_ARG_NAME)
            # This value has no effect.
            prefill_concrete_args[BUCKET_SIZE_ARG_NAME] = 39482
        except KeyError:
            pass

        decode_input_names = set(decode_input_names_)
        decode_input_names.add(BUCKET_SIZE_ARG_NAME)
        decode_concrete_args.pop(BUCKET_SIZE_ARG_NAME, None)
    elif isinstance(
        model,
        (
            furiosa_llm_models.gptj.symbolic.mlperf_submission.GPTJForCausalLM,
            furiosa_llm_models.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM,
        ),
    ):
        prefill_input_names_, prefill_concrete_args = model.get_input_names_and_concrete_args(model)
        decode_input_names_, decode_concrete_args = model.get_input_names_and_concrete_args(
            model, prefill_phase=False
        )
        prefill_input_names = set(prefill_input_names_)
        decode_input_names = set(decode_input_names_)

        # bucket_size arg is not used when it's prefill phase.
        try:
            prefill_input_names.remove(BUCKET_SIZE_ARG_NAME)
            # This value has no effect.
            prefill_concrete_args[BUCKET_SIZE_ARG_NAME] = 39482
        except KeyError:
            pass

        # due to mypy
        assert isinstance(decode_concrete_args, dict)

        # We want to concretize these arguments after quantization.
        for name in ("num_beam", "max_new_tokens", "num_real_batch", "bucket_size"):
            decode_input_names.add(name)
            decode_concrete_args.pop(name, None)
    elif isinstance(
        model,
        (
            furiosa_llm_models.bert.symbolic.mlperf_submission.BertForQuestionAnswering,
            furiosa_llm_models.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering,
        ),
    ):
        prefill_input_names = {
            "input_ids",
            "token_type_ids",
            "attention_mask",
            "position_ids",
        }
    elif isinstance(
        model,
        (
            furiosa_llm_models.llama.symbolic.mlperf_submission.LlamaForCausalLM,
            furiosa_llm_models.llama.symbolic.mlperf_submission_slice.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.mlperf_submission.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.aramco_specdec.LlamaForCausalLM,
            furiosa_llm_models.llama3.symbolic.aramco_specdec_slice_integrated.LlamaForCausalLM,
        ),
    ):
        prefill_input_names_, prefill_concrete_args = model.get_input_names_and_concrete_args(model)
        decode_input_names_, decode_concrete_args = model.get_input_names_and_concrete_args(
            model, prefill_phase=False
        )

        # due to mypy
        assert isinstance(decode_concrete_args, dict)
        prefill_input_names = set(prefill_input_names_)
        decode_input_names = set(decode_input_names_)

        # bucket_size arg is not used when it's prefill phase.
        try:
            prefill_input_names.remove(BUCKET_SIZE_ARG_NAME)
            # This value has no effect.
            prefill_concrete_args[BUCKET_SIZE_ARG_NAME] = 39482
        except KeyError:
            pass

        decode_input_names.add(BUCKET_SIZE_ARG_NAME)
        decode_concrete_args.pop(BUCKET_SIZE_ARG_NAME, None)
    else:
        raise ValueError(f"Quantization for {type(model)} model is not supported.")

    return prefill_input_names, prefill_concrete_args, decode_input_names, decode_concrete_args


def _get_example_input_with_mode(
    model: "ModelMetadata",
    mode: str,
    paged_attention_config: Optional[PagedAttentionConfig] = None,
    kv_cache_sharing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig] = None,
    random_value: bool = False,
) -> Tuple[Tuple, Dict]:
    if isinstance(model, str):
        if model in ("simple_matmul", "matmul-2L"):
            return (torch.rand(4, 4),), {}
        else:
            raise ValueError(f"Unknown model: {model}")

    # FIXME: compare with `AttentionType.PAGED_ATTENTION` after fixing circular import problem.
    if model.attention_type.value == "PAGED_ATTENTION":
        paged_attention_config = paged_attention_config or SAMPLE_PAGED_ATTENTION_CONFIG

    if model.is_beam_search_kv_cache_sharing_model:
        kv_cache_sharing_across_beams_config = (
            kv_cache_sharing_across_beams_config or SAMPLE_KVCACHE_SHARING_ACROSS_BEAMS_CONFIG
        )

    if mode == "prefill":
        bucket = SAMPLE_PREFILL_BUCKET
    elif mode == "decode":
        bucket = SAMPLE_DECODE_BUCKET
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return model.get_example_input(
        bucket,
        paged_attention_config,
        kv_cache_sharing_across_beams_config,
        random_value,
    )


def get_quantized_causal_lm(
    model: PreTrainedModel,
    metadata: "ModelMetadata",
    qformat_path: os.PathLike,
    qparam_path: os.PathLike,
    use_torch_dynamo: bool = False,
    quant_ckpt_file_path: Optional[os.PathLike] = None,
) -> QuantCausalLM:
    if use_torch_dynamo:
        # use torchdynamo for tracing.
        prefill_example_args, prefill_example_kwargs = _get_example_input_with_mode(
            metadata, "prefill"
        )
        if prefill_example_args:
            raise ValueError("Only keyword arguments are expected for LLMs.")

        prefill_graph = torchdynamo_trace_model(model, prefill_example_kwargs)
        if metadata.is_generative_model:
            decode_example_args, decode_example_kwargs = _get_example_input_with_mode(
                metadata, "decode"
            )
            if decode_example_args:
                raise ValueError("Only keyword arguments are expected for LLMs.")
            decode_graph = torchdynamo_trace_model(model, decode_example_kwargs)
        else:
            decode_graph = None
    else:
        # use torch.fx.symbolic_trace for tracing.
        prefill_input_names, prefill_concrete_args, decode_input_names, decode_concrete_args = (
            _get_input_names_and_concrete_args_for_symbolic_trace(model)
        )

        prefill_graph = fx_symbolic_trace_model(model, prefill_input_names, prefill_concrete_args)
        prefill_graph.input_names = prefill_input_names
        prefill_graph.concrete_args = prefill_concrete_args

        if metadata.is_generative_model:
            if decode_input_names is None:
                raise ValueError("decode_input_names is None even though it's generative model")
            decode_graph = fx_symbolic_trace_model(model, decode_input_names, decode_concrete_args)
            decode_graph.input_names = decode_input_names
            decode_graph.concrete_args = decode_concrete_args
        else:
            decode_graph = None

    return QuantCausalLM(
        model,
        prefill_graph,
        decode_graph,
        qparam_path,
        qformat_path,
        quant_ckpt_file_path,
    )
