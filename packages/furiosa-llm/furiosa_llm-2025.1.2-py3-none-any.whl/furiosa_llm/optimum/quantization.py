import json
import logging
import os
from pathlib import Path
import tempfile
from typing import Optional, Type, Union

import furiosa_llm_models as flm
import model_compressor
import model_compressor_impl
from optimum.quantization_base import OptimumQuantizer
from torch.utils.data import DataLoader
import transformers
from transformers import AutoConfig, AutoTokenizer, PretrainedConfig, PreTrainedModel

import furiosa_llm
from furiosa_llm.optimum.modeling import (
    _FURIOSA_CONFIG_JSON,
    _QFORMAT_YAML,
    _QPARAM_NPY,
    _get_optimization_config,
    get_optimized_cls,
    requires_parameter_names_conversion,
    trace_target_models,
    update_config_inplace,
)
from furiosa_llm.optimum.transformers import _AutoModelFinder
from furiosa_llm.optimum.types import OptimizationConfig, QuantizationConfig

logger = logging.getLogger(__name__)

# This map is used to find the calibration model class for the given original model class.
# This data is originated from https://github.com/furiosa-ai/model-compressor-private/blob/92c06a9cb506919f262b2638d0eaa9dbd0d26a6a/examples/test_configs/W8fA8fKV8f/supported_models.yaml
# TODO - Remove this map after MCP 0.6.0 because MCP 0.6.0 and its later version will be
#  able to calibrate the models with the optimized model class.
_CALIBRATION_MODEL_CLASS_MAP = {
    flm.gptj.symbolic.tta_submission.GPTJForCausalLM: flm.gptj.symbolic.huggingface_rope_rngd_gelu.GPTJForCausalLM,
    flm.llama3.symbolic.mlperf_submission.LlamaForCausalLM: flm.llama3.symbolic.huggingface_rope.LlamaForCausalLM,
    flm.llama3.symbolic.mlperf_submission_slice.LlamaForCausalLM: flm.llama3.symbolic.huggingface_rope.LlamaForCausalLM,
}


def trace_hf_rope_llama(model, prefill_input_names=None, decode_input_names=None):

    (
        traced_prefill_model,
        prefill_input_names,
        prefill_concrete_args,
    ) = model_compressor.helper.llama_custom_symbolic_trace(
        model,
        input_names=(
            prefill_input_names
            if prefill_input_names is not None
            else ["input_ids", "attention_mask", "position_ids"]
        ),
        disable_check=True,
    )
    traced_prefill_model.input_names = prefill_input_names
    traced_prefill_model.concrete_args = prefill_concrete_args
    (
        traced_decode_model,
        decode_input_names,
        decode_concrete_args,
    ) = model_compressor.helper.llama_custom_symbolic_trace(
        model,
        input_names=(
            decode_input_names
            if decode_input_names is not None
            else ["input_ids", "past_key_values", "attention_mask", "position_ids"]
        ),
        disable_check=True,
    )
    traced_decode_model.input_names = decode_input_names
    traced_decode_model.concrete_args = decode_concrete_args
    return traced_prefill_model, traced_decode_model


class _FuriosaBaseQuantizer(_AutoModelFinder, OptimumQuantizer):
    def __init__(
        self,
        model_id: str,
        model: PreTrainedModel,
        config: PretrainedConfig,
        original_model_cls: Type[PreTrainedModel],
        optimized_model_cls: Type[PreTrainedModel],
        optimization_config: OptimizationConfig,
        parameter_conversion_map: Optional[dict] = None,
    ):
        self.model_id = model_id
        self.model = model
        self.config = config
        self.original_model_cls = original_model_cls
        self.optimized_model_cls = optimized_model_cls
        self.optimization_config = optimization_config
        self.parameter_conversion_map = parameter_conversion_map

    @classmethod
    def from_pretrained(
        cls,
        model_name_or_path: Union[str, Path],
        config: Optional[PretrainedConfig] = None,
        *,
        use_only_beam_search: bool = False,
        compute_logit_for_last_token: bool = True,
        **kwargs,
    ):
        """
        Instantiate a quantizer from a pre-trained model.

        Args:
            model_name_or_path: The model id or path to the pre-trained model.
            config: The configuration of the model.
            use_only_beam_search: If True, the quantizer will apply an optimization for only beam search
                to the model. It forces to allow only beam search rather than using both beam search and
                top-k sampling.
            compute_logit_for_last_token: If True, the model will compute only the logits for the last token.
                It's effective when the model is choosen for generative tasks.
            **kwargs: Additional keyword arguments.
        """

        # TODO - why it requires? The overriding of model config works only if the model_or_path is a model id.
        #  Remove this restriction when LLM-788 is resolved.
        # https://linear.app/furiosa-ai/issue/LLM-788/update-llama-implementation-which-doesnt-need-the-config-overrides
        if not isinstance(model_name_or_path, str):
            raise ValueError(
                f"model_or_path should be a string, but got {type(model_name_or_path)}"
            )

        if config is None:
            config = AutoConfig.from_pretrained(
                model_name_or_path,
                **kwargs,
            )

        try:
            model_cls = cls.find_model_class(model_name_or_path, config, **kwargs)
        except ValueError:
            raise ValueError(f"FuriosaQuantizer doesn't support {type(config)} for quantization")

        # OptimizationConfig is only for internal use. We expect OptimizationConfig to be passed
        # from furiosa-llm, and we don't expect users to pass it.
        optimization_config = kwargs.pop("optimization_config", None)
        if optimization_config is None:
            optimization_config = _get_optimization_config(
                model_cls,
                use_only_beam_search=use_only_beam_search,
                compute_logit_for_last_token=compute_logit_for_last_token,
            )

        update_config_inplace(model_name_or_path, config, optimization_config)

        optimized_model_cls = get_optimized_cls(
            model_name_or_path,
            model_cls,
            optimization_config,
        )

        # FIXME: should it be original class? Otherwise,
        #  we need to manage the mapping between model variations and calibration model classes.
        calibration_model_cls = _CALIBRATION_MODEL_CLASS_MAP.get(optimized_model_cls, None)
        if calibration_model_cls is None:
            raise ValueError(
                f"QuantizerForCausalLM doesn't support {model_cls.__module__}.{model_cls.__qualname__} for calibration"
            )

        prameter_name_conversion_map = None
        if requires_parameter_names_conversion(model_name_or_path, model_cls):
            if kwargs.pop("low_cpu_mem_usage", None):
                # `from_huggingface` doesn't support low_cpu_mem_usage option.
                logger.warning(
                    f"Ignore `low_cpu_mem_usage` option. It cannot be used for {model_name_or_path} due to parameter name conversion."
                )

            model, prameter_name_conversion_map = calibration_model_cls.from_huggingface(
                model_name_or_path, config=config, **kwargs
            )
            config = model.config
        else:
            model = calibration_model_cls.from_pretrained(
                model_name_or_path,
                config=config,
                **kwargs,
            )
        model.eval()
        model.requires_grad_(False)

        return cls(
            model_name_or_path,
            model,
            config,
            model_cls,
            optimized_model_cls,
            optimization_config,
            prameter_name_conversion_map,
        )

    def _trace_hf_models(self, prefill_input_names=None, decode_input_names=None):

        (
            traced_prefill_model,
            prefill_input_names,
            prefill_concrete_args,
        ) = model_compressor_impl.helper.llama_custom_symbolic_trace(
            self.model,
            input_names=(
                prefill_input_names
                if prefill_input_names is not None
                else ["input_ids", "attention_mask", "position_ids"]
            ),
            disable_check=True,
        )
        traced_prefill_model.input_names = prefill_input_names
        traced_prefill_model.concrete_args = prefill_concrete_args
        (
            traced_decode_model,
            decode_input_names,
            decode_concrete_args,
        ) = model_compressor_impl.helper.llama_custom_symbolic_trace(
            self.model,
            input_names=(
                decode_input_names
                if decode_input_names is not None
                else ["input_ids", "past_key_values", "attention_mask", "position_ids"]
            ),
            disable_check=True,
        )
        traced_decode_model.input_names = decode_input_names
        traced_decode_model.concrete_args = decode_concrete_args
        return traced_prefill_model, traced_decode_model

    def quantize(
        self,
        save_dir: Union[str, Path],
        dataloader: DataLoader,
        quantization_config: QuantizationConfig,
        file_prefix: Optional[str] = None,
        **kwargs,
    ):
        """
        Quantizes the model and saves the quantized model, qformat, qparam, config.json, vocab.json, and tokenizer.json.

        Args:
            save_dir: The directory to save the quantized model.
            dataloader: The dataloader for calibration.
            quantization_config: The quantization configuration.
            file_prefix: The prefix for the saved files.
            **kwargs: Additional keyword arguments.
        """

        temp_dir = kwargs.pop("temp_dir", None)
        if temp_dir is None:
            _tempdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
            temp_dir = _tempdir.name

        prefill_graph, decode_graph = self._trace_hf_models()
        hf_model_trace = model_compressor.FXGraphCausalLM(
            type(self.model), prefill_graph, decode_graph
        )

        disable_inout = (True, True)
        weight_calib_method = "AMAX_SYM"
        weight_dtype = quantization_config.weight.to_qformat()
        weight_granularity = "channel"
        act_dtype = quantization_config.activation.to_qformat()
        act_calib_method = "AMAX_SYM"
        act_granularity = "channel"
        kv_dtype = None
        if quantization_config.kv_cache is not None:
            kv_dtype = quantization_config.kv_cache.to_qformat()
        target_machine = "RGDA0"
        weighted_op_emul_dtype = "fp64"
        v_cache_granularity = "tensor"

        quantsim_model = model_compressor.create_quantsim_model(
            hf_model_trace,
            disable_inout=disable_inout,
            dataloader=dataloader,
            output_path=temp_dir,
            weight_calib_method=weight_calib_method,
            weight_dtype=weight_dtype,
            weight_granularity=weight_granularity,
            act_dtype=act_dtype,
            act_calib_method=act_calib_method,
            act_granularity=act_granularity,
            kv_dtype=kv_dtype,
            target_machine=target_machine,
            weighted_op_emul_dtype=weighted_op_emul_dtype,
            v_cache_granularity=v_cache_granularity,
            qlevel=2,
            disable_old_node_mapping=True,
        )

        quantsim_model = model_compressor.calibrate(
            quantsim_model,
            model_type=type(self.model),
            ckpt_folder_path=temp_dir,
            ckpt_to_state_key_map=self.parameter_conversion_map,
        )

        export_model = self.optimized_model_cls.from_pretrained(
            self.model_id,
            config=self.config,
            **kwargs,
        )

        del quantsim_model

        # Migrates the qparam, qformat to the optimized model, and save both qparam, qformat files
        prefill_trace, _ = trace_target_models(self.original_model_cls, export_model)

        hf_qformat_path = Path(temp_dir) / _QFORMAT_YAML
        hf_qparam_path = Path(temp_dir) / _QPARAM_NPY
        quantsim_model = model_compressor.create_quantsim_model(
            prefill_trace,
            qformat_path=os.fspath(hf_qformat_path),
            qparam_path=os.fspath(hf_qparam_path),
            target_machine='RGDA0',
            immigrate_qparams=True,
            output_path=save_dir,
        )
        qformat, qparam = model_compressor.extract_qformat_and_qparam(quantsim_model)
        model_compressor.save_qformat_qparam(
            qformat_dict=qformat,
            qformat_out_path=Path(save_dir) / _QFORMAT_YAML,
            qparam_dict=qparam,
            qparam_out_path=Path(save_dir) / _QPARAM_NPY,
            weight_calib_method=weight_calib_method,
            weight_granularity=weight_granularity,
            weight_dtype=weight_dtype,
            act_calib_method=act_calib_method,
            act_granularity=act_granularity,
            act_dtype=act_dtype,
            kv_dtype=kv_dtype,
            disable_inout=disable_inout,
        )

        # Saves the quantized parameters
        model_compressor.export(quantsim_model, qckpt_output_path=save_dir)

        # Save config.json, vocab.json, and tokenizer.json
        self.config.save_pretrained(save_dir)
        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        tokenizer.save_pretrained(save_dir)

        # Save the furiosa config
        furiosa_config = {
            "model_id": self.model_id,
            "versions": {
                "model_compressor": model_compressor.__version__,
                "furiosa_llm": furiosa_llm.__full_version__,
            },
            "model_class": {
                "module": self.optimized_model_cls.__module__,
                "name": self.optimized_model_cls.__name__,
            },
            "optimization_config": dict(self.optimization_config),
            "quantization_config": dict(quantization_config),
        }
        furiosa_config_json_path = Path(save_dir) / _FURIOSA_CONFIG_JSON
        with open(furiosa_config_json_path, "w", encoding="utf-8") as json_file:
            json.dump(furiosa_config, json_file, indent=2)


class QuantizerForCausalLM(_FuriosaBaseQuantizer):
    _model_mapping = transformers.MODEL_FOR_CAUSAL_LM_MAPPING


class QuantizerForQuestionAnswering(_FuriosaBaseQuantizer):
    _model_mapping = transformers.MODEL_FOR_QUESTION_ANSWERING_MAPPING
