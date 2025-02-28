from contextlib import AbstractContextManager, ExitStack, contextmanager
import copy
import functools
import importlib
import json
import logging
from pathlib import Path
from typing import (
    Any,
    ContextManager,
    Dict,
    Final,
    FrozenSet,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)
from unittest.mock import patch
import warnings

import accelerate
from huggingface_hub.constants import HUGGINGFACE_HUB_CACHE
from optimum.modeling_base import OptimizedModel
import torch
from torch.fx import GraphModule
import transformers
from transformers import LlamaConfig, PretrainedConfig, PreTrainedModel

from furiosa_llm.models.quant import (
    QuantCausalLM,
    _get_input_names_and_concrete_args_for_symbolic_trace,
    fx_symbolic_trace_model,
)
from furiosa_llm.optimum.transformers import _AutoModelFinder
from furiosa_llm.optimum.types import AttentionType, OptimizationConfig, QuantizationConfig

_WARNINGS_TO_IGNORE = [
    ".*copying from a non-meta parameter in the checkpoint to a meta parameter in the current model, which is a no-op..*",
]

_FURIOSA_CONFIG_JSON = "furiosa_config.json"
_QFORMAT_YAML = "qformat.yaml"
_QPARAM_NPY = "qparam.npy"
_EXPORTED_MODEL_QCKPT = "exported_model.qckpt"


# Pretrained model IDs
FURIOSA_EXAONE3_7D8B_INSTRUCT_PRETRAINED_ID: Final[str] = (
    "furiosa-ai/EXAONE-3.0-7.8B-Instruct-converted"
)
EXAONE3_7D8B_INSTRUCT_PRETRAINED_ID: Final[str] = "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct"
EXAONE3_5_2D4B_INSTRUCT_PRETRAINED_ID: Final[str] = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"
EXAONE3_5_7D8B_INSTRUCT_PRETRAINED_ID: Final[str] = "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct"
EXAONE3_5_32B_INSTRUCT_PRETRAINED_ID: Final[str] = "LGAI-EXAONE/EXAONE-3.5-32B-Instruct"

GPT_2_PRETRAINED_ID: Final[str] = "gpt2"
GPT_NEO_PRETRAINED_ID: Final[str] = "EleutherAI/gpt-neo-125m"
GPT_J_PRETRAINED_ID: Final[str] = "EleutherAI/gpt-j-6B"

MLPERF_BERT_LARGE_PRETRAINED_ID: Final[str] = "furiosa-ai/mlperf-bert-large"
MLPERF_GPTJ_PRETRAINED_ID: Final[str] = "furiosa-ai/mlperf-gpt-j-6b"

LLAMA_7B_PRETRAINED_ID: Final[str] = "huggyllama/llama-7b"
LLAMA2_70B_CHAT_PRETRAINED_ID: Final[str] = "meta-llama/Llama-2-70b-chat-hf"
LLAMA3_1_8B_PRETRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-8B"
LLAMA3_1_70B_PRETRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-70B"
LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-8B-Instruct"
LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID: Final[str] = "meta-llama/Meta-Llama-3.1-70B-Instruct"

LLAMA3_1_8B_ELICEAI_HELPY_EDU_B_PRETRAINED_ID: Final[str] = "eliceai/helpy-edu-b-llama3.1"

LLAMA3_3_70B_INSTRUCT_PRETRAINED_ID: Final[str] = "meta-llama/Llama-3.3-70B-Instruct"

SOLAR_10D7B_INSTRUCT_PRETRAINED_ID: Final[str] = "upstage/SOLAR-10.7B-Instruct-v1.0"

LLAMA3_BASED_MODEL_TYPES: Final[Set[str]] = {
    "ExaoneForCausalLM",
}

LLAMA3_BASED_MODEL_CONFIG_TYPES: Final[Set[str]] = {"ExaoneConfig"}
LLAMA3_BASED_MODEL_IDS: Final[Set[str]] = {
    FURIOSA_EXAONE3_7D8B_INSTRUCT_PRETRAINED_ID,
}

# FIXME: there exists a gptj_rope_packed_rngd_gelu model and it differs from mlperf_submission
MODEL_CLS_TO_MLPERF_OPT_CONFIGS = {
    transformers.GPTJForCausalLM: OptimizationConfig(
        attention_type=AttentionType.PAGED_ATTENTION,
        optimize_rope=True,
        optimize_packed=True,
        use_rngd_gelu=True,
        kv_cache_sharing_across_beams=True,
        causal_mask_free_decoding=True,
        inbound_beamsearch_softmax=True,
    ),
    transformers.LlamaForCausalLM: OptimizationConfig(
        attention_type=AttentionType.PAGED_ATTENTION,
        optimize_rope=True,
        optimize_packed=True,
        causal_mask_free_decoding=True,
    ),
    transformers.BertForQuestionAnswering: OptimizationConfig(
        use_unsplit_packed=True,
        use_rngd_gelu=True,
    ),
}

OPTIMIZATION_CONFIG_MAPPER = {
    "use_only_beam_search": "kv_cache_sharing_across_beams",
    "compute_logit_for_last_token": "calculate_logit_only_for_last_token",
}


def is_mlperf_optimized(model_cls: Type, optimization_config: OptimizationConfig) -> bool:
    if mlperf_option := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(model_cls):
        return optimization_config == mlperf_option
    return False


def contains_mlperf_opts(model_cls: Type, optimization_config: OptimizationConfig) -> bool:
    if mlperf_option := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(model_cls):
        return (
            optimization_config.get_enabled_opts().issuperset(mlperf_option.get_enabled_opts())
            and optimization_config.attention_type == mlperf_option.attention_type
        )
    return False


def is_mlperf_optimized_with(
    model_cls: Type, optimization_config: OptimizationConfig, **kwargs
) -> bool:
    if mlperf_option := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(model_cls):
        copied = copy.deepcopy(mlperf_option)
        for k, v in kwargs.items():
            setattr(copied, k, v)
        return optimization_config == copied
    return False


def is_llama3(pretrained_id: str) -> bool:
    # TODO - We will be able to change this part to use PretrainedConfig
    #   instead of pretrained_id when we use the single llama model implementation.
    return pretrained_id in {
        LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID,
        LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID,
        LLAMA3_1_8B_PRETRAINED_ID,
        LLAMA3_1_70B_PRETRAINED_ID,
        LLAMA3_1_8B_ELICEAI_HELPY_EDU_B_PRETRAINED_ID,
    }


def is_llama3_based(
    pretrained_id: str, model_or_config_cls: Union[Type[PreTrainedModel], Type[PretrainedConfig]]
) -> bool:
    if is_llama3(pretrained_id) or pretrained_id in LLAMA3_BASED_MODEL_IDS:
        return True
    if issubclass(model_or_config_cls, PreTrainedModel):
        return model_or_config_cls.__qualname__ in LLAMA3_BASED_MODEL_TYPES
    if issubclass(model_or_config_cls, PretrainedConfig):
        return model_or_config_cls.__qualname__ in LLAMA3_BASED_MODEL_CONFIG_TYPES
    return False


def get_llama_kind(pretrained_id: str) -> str:
    if pretrained_id == LLAMA_7B_PRETRAINED_ID:
        return "1-7B"
    elif pretrained_id == LLAMA2_70B_CHAT_PRETRAINED_ID:
        return "2-70B"
    elif pretrained_id in (
        LLAMA3_1_8B_INSTRUCT_PRETRAINED_ID,
        LLAMA3_1_8B_PRETRAINED_ID,
        LLAMA3_1_8B_ELICEAI_HELPY_EDU_B_PRETRAINED_ID,
    ):
        return "3.1-8B"
    elif pretrained_id in (
        LLAMA3_1_70B_INSTRUCT_PRETRAINED_ID,
        LLAMA3_1_70B_PRETRAINED_ID,
    ):
        return "3.1-70B"
    else:
        raise ValueError(f"Unsupported llama model: {pretrained_id}")


def is_generative_model(model_cls: Type[PreTrainedModel]) -> bool:
    return (
        get_mapped_class_for_optimization(model_cls)
        in transformers.MODEL_FOR_CAUSAL_LM_MAPPING.values()
    )


def update_config_inplace(
    pretrained_id: str, config: PretrainedConfig, optimization_config: OptimizationConfig
) -> PretrainedConfig:
    """Update PretrainedConfig inplace for an optimized class"""
    # NOTE: this function might be called multiple times for one model's config.
    # Make sure config is in intended state after arbitrary number of updates.

    # Apply this update to only models that use LlamaConfig.
    # Models that use its own config type (e.g., Exaone) will go through this conversion inside `from_huggingface` method.
    if (
        is_llama3_based(pretrained_id, type(config))
        and type(config) is transformers.LlamaConfig
        and getattr(config, "rope_scaling", None)
        and not getattr(config, "inv_freq_config", None)
    ):
        # FIXME: This is needed because furiosa-llm-models llama3 model cannot accept
        # the config as it is.
        config.inv_freq_config = config.rope_scaling
        config.rope_scaling = None

    # This is a workaround to make model with decomposed layernorm distinguishable after instantiation.
    if optimization_config.decompose_layernorm:
        config.decompose_layernorm = True

    return config


class DecomposedLayerNorm(torch.nn.Module):
    def __init__(self, hidden_size, eps=1e-5):
        """
        Decomposed torch.nn.LayerNorm for efficient chip2chip communication by decomposing in more smaller units.
        This is only available for inference.
        """
        super().__init__()
        self.weight = torch.nn.Parameter(torch.ones(hidden_size))
        self.bias = torch.nn.Parameter(torch.zeros(hidden_size))
        self.variance_epsilon = eps
        self.hidden_size = hidden_size

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        mean = hidden_states.mean(-1, keepdim=True)
        pow_mean = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = (
            self.weight
            * (hidden_states - mean)
            * torch.rsqrt(pow_mean - mean.pow(2) + self.variance_epsilon)
            + self.bias
        )

        return hidden_states.to(input_dtype)


@contextmanager
def replace_layernorm(temp_layernorm):
    original_layernorm = torch.nn.LayerNorm
    torch.nn.LayerNorm = temp_layernorm  # type: ignore
    try:
        yield
    finally:
        torch.nn.LayerNorm = original_layernorm  # type: ignore


# To suppress verbose but not important warnings
class MCPLogFilter(logging.Filter):
    def filter(self, record):
        return (
            "torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction is enabled. \
                This optimization may affect performance."
            not in record.msg
        )


_cqm_logger = logging.getLogger("create_quantsim_model")
_cqm_logger.addFilter(MCPLogFilter())


logger = logging.getLogger(__name__)


def apply_warning_filters():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    for warning_to_ignore in _WARNINGS_TO_IGNORE:
        warnings.filterwarnings(action="ignore", message=warning_to_ignore, append=True)


def get_mapped_class_for_optimization(original: Type[PreTrainedModel]) -> Type[PreTrainedModel]:
    """Some models share other model's optimized class in furiosa-llm-models
    because their architectures are essentially same.
    """
    if original.__qualname__ == "ExaoneForCausalLM":
        return transformers.LlamaForCausalLM
    return original


def _get_default_optimization_config(model_cls: Type[PreTrainedModel]) -> OptimizationConfig:
    model_cls = get_mapped_class_for_optimization(model_cls)

    if optim_options := MODEL_CLS_TO_MLPERF_OPT_CONFIGS.get(model_cls):
        return optim_options
    else:
        return OptimizationConfig()


def _get_optimization_config(model_cls: Type[PreTrainedModel], **kwargs) -> OptimizationConfig:
    optimization_config = _get_default_optimization_config(model_cls)

    overridden_config: Dict[str, Any] = {}
    for k in OPTIMIZATION_CONFIG_MAPPER.keys():
        if k in kwargs:
            v = OPTIMIZATION_CONFIG_MAPPER[k]
            overridden_config[v] = kwargs.pop(k)

    return optimization_config.with_optimizations(overridden_config)


def _is_model_path(model_id: Union[str, Path]) -> bool:
    return isinstance(model_id, Path) or model_id.startswith("/") or model_id.startswith(".")


def is_quantized_model_path(model_id: Union[str, Path]) -> bool:
    return _is_model_path(model_id) and (Path(model_id) / _FURIOSA_CONFIG_JSON).exists()


def trace_target_models(
    original_model_cls: Type[PreTrainedModel], target_model: PreTrainedModel
) -> tuple[GraphModule, Optional[GraphModule]]:
    # use torch.fx.symbolic_trace for tracing.
    prefill_input_names, prefill_concrete_args, decode_input_names, decode_concrete_args = (
        _get_input_names_and_concrete_args_for_symbolic_trace(target_model)
    )

    prefill_graph = fx_symbolic_trace_model(
        target_model, prefill_input_names, prefill_concrete_args
    )
    prefill_graph.input_names = prefill_input_names
    prefill_graph.concrete_args = prefill_concrete_args

    if is_generative_model(original_model_cls):
        if decode_input_names is None:
            raise ValueError("decode_input_names is None even though it's generative model")
        decode_graph = fx_symbolic_trace_model(
            target_model, decode_input_names, decode_concrete_args
        )
        decode_graph.input_names = decode_input_names
        decode_graph.concrete_args = decode_concrete_args
    else:
        decode_graph = None

    return prefill_graph, decode_graph


def get_optimized_cls(
    pretrained_id: str,
    model_cls: Type[PreTrainedModel],
    optimization_config: OptimizationConfig,
) -> Type[PreTrainedModel]:

    import furiosa_llm_models as flm

    # If no optimization is enabled, return the original model class.
    if not optimization_config.get_enabled_opts():
        return model_cls

    is_llama3_based_model = is_llama3_based(pretrained_id, model_cls)

    model_cls = get_mapped_class_for_optimization(model_cls)

    if model_cls is transformers.BertForQuestionAnswering:
        if is_mlperf_optimized(model_cls, optimization_config):
            return flm.bert.symbolic.mlperf_submission.BertForQuestionAnswering
        elif optimization_config.compact_causal_mask:
            return (
                flm.bert.symbolic.experimental.huggingface_unsplit_packed.BertForQuestionAnswering
            )
        elif optimization_config.optimize_furiosa:
            return flm.bert.symbolic.huggingface.BertForQuestionAnswering
        else:
            raise ValueError(
                f"Unsupported bert model: pretrained_id={pretrained_id}, model_cls={model_cls}, optimization_config={optimization_config}"
            )
    elif model_cls is transformers.LlamaForCausalLM:
        if is_mlperf_optimized(model_cls, optimization_config):
            if is_llama3_based_model:
                return flm.llama3.symbolic.mlperf_submission.LlamaForCausalLM
            else:
                return flm.llama.symbolic.mlperf_submission.LlamaForCausalLM
        elif is_mlperf_optimized_with(
            model_cls, optimization_config, calculate_logit_only_for_last_token=True
        ):
            if is_llama3_based_model:
                return flm.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM
            else:
                return flm.llama.symbolic.mlperf_submission_slice.LlamaForCausalLM
        elif (
            is_mlperf_optimized_with(
                model_cls,
                optimization_config,
                optimized_for_speculative_decoding=True,
            )
            and is_llama3_based_model
        ):
            return flm.llama3.symbolic.aramco_specdec.LlamaForCausalLM
        elif (
            is_mlperf_optimized_with(
                model_cls,
                optimization_config,
                calculate_logit_only_for_last_token=True,
                optimized_for_speculative_decoding=True,
            )
            and is_llama3_based_model
        ):
            return flm.llama3.symbolic.aramco_specdec_slice_integrated.LlamaForCausalLM
        else:
            raise ValueError(
                f"Unsupported llama model: pretrained_id={pretrained_id}, model_cls={model_cls}, optimization_config={optimization_config}"
            )
    elif model_cls is transformers.GPTJForCausalLM:
        optim_options = optimization_config
        assert not optim_options.use_unsplit_packed, "Unsplit packed is not supported for GPT-J"
        if is_mlperf_optimized(model_cls, optimization_config):
            return flm.gptj.symbolic.mlperf_submission.GPTJForCausalLM
        elif is_mlperf_optimized_with(
            model_cls, optimization_config, calculate_logit_only_for_last_token=True
        ):
            return flm.gptj.symbolic.mlperf_submission_slice.GPTJForCausalLM
        elif is_mlperf_optimized_with(
            model_cls, optimization_config, kv_cache_sharing_across_beams=False
        ):
            return flm.gptj.symbolic.tta_submission.GPTJForCausalLM

        # fmt: off
        self_to_cls: Dict[Tuple[AttentionType,FrozenSet[str]],Type[PreTrainedModel]] = {
            (AttentionType.VANILLA, frozenset(("optimize_furiosa",))): flm.gptj.symbolic.huggingface.GPTJForCausalLM,
            (AttentionType.VANILLA, frozenset(("decompose_layernorm",))): transformers.GPTJForCausalLM,
            (AttentionType.VANILLA, frozenset()): transformers.GPTJForCausalLM,
            (AttentionType.VANILLA, frozenset(("optimize_rope",))): flm.gptj.symbolic.huggingface_rope.GPTJForCausalLM,
            (AttentionType.VANILLA, frozenset(("optimize_rope", "use_rngd_gelu"))): flm.gptj.symbolic.huggingface_rope_rngd_gelu.GPTJForCausalLM,
            (AttentionType.PREALLOCATION_CONCAT, frozenset()): flm.gptj.symbolic.preallocated_concat.GPTJForCausalLM,
            (AttentionType.PREALLOCATION_CONCAT, frozenset(("optimize_rope",))): flm.gptj.symbolic.preallocated_concat_rope.GPTJForCausalLM,
            (AttentionType.PAGED_ATTENTION, frozenset(("optimize_rope",))): flm.gptj.symbolic.paged_attention_rope.GPTJForCausalLM,
            (AttentionType.PAGED_ATTENTION, frozenset(("optimize_rope", "optimize_packed", "causal_mask_free_decoding"))): flm.gptj.symbolic.paged_attention_optimized_packed_rope.GPTJForCausalLM,
        }
        # fmt: on
        assert set(key for keys in self_to_cls.keys() for key in keys[1]).issubset(
            OptimizationConfig().model_dump().keys()
        )

        if cls_ := self_to_cls.get(
            (optim_options.attention_type, optimization_config.get_activated_options())
        ):
            return cls_
        else:
            raise ValueError(
                f"Unsupported model: pretrained_id={pretrained_id}, model_cls={model_cls}, optimization_config={optimization_config}"
            )

    return model_cls


def _load_quantized_model_meta(
    path: Path,
) -> Tuple[Dict[str, Any], OptimizationConfig, QuantizationConfig, Path, Path, Path]:
    furiosa_config_file = path / _FURIOSA_CONFIG_JSON
    qformat_path = path / _QFORMAT_YAML
    qparam_path = path / _QPARAM_NPY
    quant_ckpt_file_path = path / _EXPORTED_MODEL_QCKPT

    furiosa_config = json.loads(furiosa_config_file.read_text())
    optimization_config = OptimizationConfig.model_validate(furiosa_config['optimization_config'])
    quantization_config = QuantizationConfig.from_qformat(qformat_path)
    return (
        furiosa_config,
        optimization_config,
        quantization_config,
        qformat_path,
        qparam_path,
        quant_ckpt_file_path,
    )


def requires_parameter_names_conversion(model_id: str, model_cls: Type[PreTrainedModel]) -> bool:
    return model_cls.__qualname__ == "ExaoneForCausalLM"


def convert_exoane_config_to_llama_config(original_config: PretrainedConfig) -> LlamaConfig:
    if type(original_config).__qualname__ != "ExaoneConfig":
        raise ValueError("`original_config` is not an exaone config.")
    # borrowed from `furiosa_llm_models.llama3.symbolic.mlperf_submission.LlamaForCausalLM.from_huggingface`
    # https://github.com/furiosa-ai/furiosa-llm-models/blob/702cc4ba4209f02a452e49cef5afdf89d7d8af34/furiosa_llm_models/llama3/symbolic/mlperf_submission.py#L823
    # TODO: make this conversion as an independent method in furiosa-llm-models and use it.
    new_exaone_config = LlamaConfig(
        vocab_size=original_config.vocab_size,
        hidden_size=original_config.hidden_size,
        intermediate_size=original_config.intermediate_size,
        num_hidden_layers=original_config.num_layers,
        num_attention_heads=original_config.num_attention_heads,
        max_position_embeddings=original_config.max_position_embeddings,
        rms_norm_eps=original_config.layer_norm_epsilon,
        num_key_value_heads=original_config.num_key_value_heads,
        rope_theta=original_config.rope_theta,
        bos_token_id=original_config.bos_token_id,
        eos_token_id=original_config.eos_token_id,
        pad_token_id=original_config.pad_token_id,
        attention_bias=False,
    )
    new_exaone_config.architectures = ["LlamaForCausalLM"]
    new_exaone_config.torch_dtype = original_config.torch_dtype

    # Furiosa specific: we currently utilize inv_freq_config for rope scaling
    if new_exaone_config.rope_scaling is not None:
        new_exaone_config.inv_freq_config = new_exaone_config.rope_scaling
        new_exaone_config.rope_scaling = None

    return new_exaone_config


def convert_config_for_optimized_cls(
    original_config: PretrainedConfig, optimized_cls: Type[PreTrainedModel]
) -> PretrainedConfig:
    if (
        type(original_config).__qualname__ == "ExaoneConfig"
        and optimized_cls.__qualname__ == "LlamaForCausalLM"
    ):
        return convert_exoane_config_to_llama_config(original_config)
    raise ValueError(f"Cannot convert config of type {original_config} for {type(optimized_cls)}")


class _FuriosaBaseAutoModelClass(_AutoModelFinder):
    @classmethod
    def _from_quantized_model(cls, path: Path, config: PretrainedConfig) -> "OptimizedModel":
        ctx_mgrs: List[Union[AbstractContextManager[Any], ContextManager[Any]]] = []
        ctx_mgrs.append(accelerate.init_empty_weights())

        model_cls = cls.find_model_class(path, config)

        furiosa_config, optimization_config, _, qformat_path, qparam_path, quant_ckpt_file_path = (
            _load_quantized_model_meta(path)
        )
        if optimization_config.decompose_layernorm:
            ctx_mgrs.append(replace_layernorm(DecomposedLayerNorm))

        optimized_cls_module = importlib.import_module(furiosa_config['model_class']['module'])
        optimized_cls_name = furiosa_config['model_class']['name']
        optimized_cls = getattr(optimized_cls_module, optimized_cls_name)

        with ExitStack() as stack:
            for ctx_mgr in ctx_mgrs:
                stack.enter_context(ctx_mgr)

            # Loading the random weights
            model = optimized_cls(config)
            model.eval()
            model.requires_grad_(False)

        prefill_graph, decode_graph = trace_target_models(model_cls, model)

        # Load the quantized model directly from the checkpoint
        quant_model = QuantCausalLM(
            model,
            prefill_graph,
            decode_graph,
            qparam_path=qparam_path,
            qformat_path=qformat_path,
            quant_ckpt_file_path=quant_ckpt_file_path,
        )

        # Set configs to be comapatible with PretrainedModel and LLM
        quant_model.config = config
        quant_model.optimization_config = optimization_config
        quant_model.quantization_config = QuantizationConfig.from_qformat(qformat_path)
        return quant_model

    @classmethod
    def _from_pretrained(
        cls,
        model_id: Union[str, Path],
        config: PretrainedConfig,
        use_auth_token: Optional[Union[bool, str]] = None,
        token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: str = HUGGINGFACE_HUB_CACHE,
        subfolder: str = "",
        local_files_only: bool = False,
        *,
        use_only_beam_search: bool = False,
        compute_logit_for_last_token: bool = False,
        **kwargs,
    ) -> "OptimizedModel":
        ctx_mgrs: List[Union[AbstractContextManager[Any], ContextManager[Any]]] = []
        model_cls = cls.find_model_class(model_id, config, **kwargs)
        exported_model_qckpt_path: Optional[Path] = None

        # If the model is quantized by FuriosaQuantizer (a conditional branch for production)
        if is_quantized_model_path(model_id):
            model_path = Path(model_id) if not isinstance(model_id, Path) else model_id
            return cls._from_quantized_model(model_path, config)
        else:
            # If the model is not quantized but a model id with qparam, qformat are specified,
            # this code path will be invoked.
            # TODO - we can remove this branch if we improve LLM class and e2e_pipe.py
            #   to pass the directory path of furiosa-llm-models-artifacts instead of individual files.

            # TODO - Remove this assertion after the dependency of model_id is removed.
            #  It should be able to run with the model directory. See update_config_inplace() and
            #  get_optimized_cls(). They depend on a model_id string.
            assert isinstance(
                model_id, str
            ), "model_id must be a string rather than Path if it is not a quantized model"

            # OptimizationConfig is only for internal use. We expect OptimizationConfig to be passed
            # from furiosa-llm, and we don't expect users to pass it.
            optimization_config = kwargs.pop("optimization_config", None)
            if optimization_config is None:
                optimization_config = _get_optimization_config(
                    model_cls,
                    use_only_beam_search=use_only_beam_search,
                    compute_logit_for_last_token=compute_logit_for_last_token,
                )

            if optimization_config.decompose_layernorm:
                ctx_mgrs.append(replace_layernorm(DecomposedLayerNorm))

            config = update_config_inplace(model_id, config, optimization_config)
            optimized_cls = get_optimized_cls(model_id, model_cls, optimization_config)

            # Fill qformat, qparam, exported_models.qckpt if they exist
            quantization_checkpt_path = kwargs.pop("quantization_checkpt_path", None)
            if quantization_checkpt_path:
                if not isinstance(quantization_checkpt_path, Path):
                    quantization_checkpt_path = Path(quantization_checkpt_path)

                qformat_path = quantization_checkpt_path / _QFORMAT_YAML
                qparam_path = quantization_checkpt_path / _QPARAM_NPY
                exported_model_qckpt_path = quantization_checkpt_path / _EXPORTED_MODEL_QCKPT

                if not qformat_path.exists() or not qparam_path.exists():
                    raise ValueError(
                        f"qformat.yaml or qparam.npy checkpoint files are not found in {quantization_checkpt_path}"
                    )

                if exported_model_qckpt_path and exported_model_qckpt_path.exists():
                    ctx_mgrs.append(accelerate.init_empty_weights())
                else:
                    exported_model_qckpt_path = None

            def load_from_pretrained():
                base_kwargs = {
                    "config": config,
                    "use_auth_token": use_auth_token,
                    "token": token,
                    "revision": revision,
                    "force_download": force_download,
                    "cache_dir": cache_dir,
                    "subfolder": subfolder,
                    "local_files_only": local_files_only,
                }

                if requires_parameter_names_conversion(model_id, model_cls):
                    if kwargs.pop("low_cpu_mem_usage", None):
                        logger.warning(
                            "`low_cpu_mem_usage` option cannot be used for models that need parameter name conversion. It's ignored."
                        )
                    return optimized_cls.from_huggingface(
                        model_id,
                        **base_kwargs,
                        **kwargs,
                    )[0]
                else:
                    low_cpu_mem_usage = kwargs.pop("low_cpu_mem_usage", True)
                    return optimized_cls.from_pretrained(
                        model_id,
                        low_cpu_mem_usage=low_cpu_mem_usage,
                        **base_kwargs,
                        **kwargs,
                    )

            with ExitStack() as stack:
                for ctx_mgr in ctx_mgrs:
                    stack.enter_context(ctx_mgr)

                # Suppress too verbose warnings
                with warnings.catch_warnings(record=True):
                    apply_warning_filters()

                    # if the exported_model.qckpt exists, the model should be loaded from exported_model.qckpt.
                    if exported_model_qckpt_path:
                        if requires_parameter_names_conversion(model_id, model_cls):
                            config = convert_config_for_optimized_cls(config, optimized_cls)

                        model = optimized_cls(config=config)
                    else:  # otherwise, load the model from the pretrained model
                        try:
                            with patch(
                                "torch.load",
                                new=functools.partial(torch.load, mmap=True, weights_only=True),
                            ):
                                model = load_from_pretrained()
                        except OSError:
                            # Error occurs if the model was not saved with `_use_new_zipfile_serialization` option.
                            # Try again without mmap option.
                            model = load_from_pretrained()

                    model.eval()
                    model.requires_grad_(False)

            # Quantize model weights with qparam/format or loading a quantized model directly
            if quantization_checkpt_path:
                prefill_graph, decode_graph = trace_target_models(model_cls, model)
                return QuantCausalLM(
                    model,
                    prefill_graph,
                    decode_graph,
                    qparam_path=qparam_path,
                    qformat_path=qformat_path,
                    quant_ckpt_file_path=exported_model_qckpt_path,
                )
            else:
                return model


class AutoModel(_FuriosaBaseAutoModelClass, OptimizedModel):
    _model_mapping = transformers.MODEL_MAPPING


class AutoModelForCausalLM(_FuriosaBaseAutoModelClass, OptimizedModel):
    _model_mapping = transformers.MODEL_FOR_CAUSAL_LM_MAPPING


class AutoModelForQuestionAnswering(_FuriosaBaseAutoModelClass, OptimizedModel):
    _model_mapping = transformers.MODEL_FOR_QUESTION_ANSWERING_MAPPING
