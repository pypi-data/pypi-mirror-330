from argparse import Namespace
from dataclasses import fields
import logging
import os
import re
from typing import Optional

from furiosa_llm.api import LLM, SchedulerConfig
from furiosa_llm.utils import get_logger_with_tz

logger = get_logger_with_tz(logging.getLogger(__name__))


def load_llm_from_args(args: Namespace) -> LLM:
    model: str = args.model
    tp: Optional[int] = args.tensor_parallel_size
    pp: Optional[int] = args.pipeline_parallel_size
    dp: Optional[int] = args.data_parallel_size
    devices = args.devices

    speculative_model = args.speculative_model
    num_speculative_tokens = args.num_speculative_tokens
    draft_tp: Optional[int] = args.speculative_draft_tensor_parallel_size
    draft_pp: Optional[int] = args.speculative_draft_pipeline_parallel_size
    draft_dp: Optional[int] = args.speculative_draft_data_parallel_size

    if (num_speculative_tokens or speculative_model) and not (
        num_speculative_tokens and speculative_model
    ):
        raise ValueError(
            "To use speculative decoding, both --num-speculative-tokens and --speculative-model should be given."
        )

    # Create LLM for speculative model if given.
    if speculative_model:
        assert num_speculative_tokens

        # FIXME(ssh): Remove this constraint after adjusting the LLM to provide a model parallelization interface for the original and speculative model seperately.
        if draft_dp != dp:
            raise ValueError(
                "Different value for --data-parallel-size and --speculative-draft-pipeline-parallel-size is not allowed now."
            )

        use_speculative_model_artifact_load_path = os.path.isdir(
            speculative_model
        ) and os.path.exists(os.path.join(speculative_model, "artifact.json"))

        if use_speculative_model_artifact_load_path:
            logger.info(f"Loading Speculative model LLM from artifact: {speculative_model}")
            if args.speculative_draft_tensor_parallel_size:
                logger.warning(
                    "When loading Speculative model LLM from artifact, given -tp value will be ignored."
                )
            speculative_model = LLM.load_artifact(
                speculative_model,
                data_parallel_size=draft_dp,
                pipeline_parallel_size=draft_pp,
                devices=devices,
            )
        else:
            speculative_model = LLM(
                speculative_model,
                tensor_parallel_size=draft_tp or 4,
                pipeline_parallel_size=draft_pp or 1,
                data_parallel_size=draft_dp,
                devices=devices,
            )

    use_artifact_load_path = os.path.isdir(model) and os.path.exists(
        os.path.join(model, "artifact.json")
    )
    if use_artifact_load_path:
        logger.info(f"Loading LLM from artifact: {model}")
        if args.tensor_parallel_size:
            logger.warning("When loading LLM from artifact, given -tp value will be ignored.")

        try:
            scheduler_config = SchedulerConfig.load(f"{model}/runtime_config.json")
            for scheduler_config_attr in fields(SchedulerConfig):
                if (v := getattr(args, scheduler_config_attr.name, None)) is not None:
                    setattr(scheduler_config, scheduler_config_attr.name, v)
            scheduler_config.is_offline = False
        except Exception:
            scheduler_config = None

        return LLM.load_artifact(
            model,
            devices=devices,
            data_parallel_size=dp,
            pipeline_parallel_size=pp,
            scheduler_config=scheduler_config,
            # TODO: support speculative_model, num_speculative_tokens
        )

    if model == "furiosa-ai/fake-llm":
        from transformers import AutoTokenizer

        from tests.utils import FakeLLM

        return FakeLLM(AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer"))

    if not is_hf_model_id_like(model):
        logger.warning(
            f"The given --model argument is not a valid artifact path, nor a valid Hugging Face model id: {model}"
        )
        logger.warning("Trying Hugging Face model id anyways.")

    logger.info(
        f"Loading LLM from Hugging Face model id: {model}, pp={pp}, tp={tp}, dp={dp}, devices={devices}"
    )
    scheduler_config = SchedulerConfig()
    for scheduler_config_attr in fields(SchedulerConfig):
        if (v := getattr(args, scheduler_config_attr.name, None)) is not None:
            setattr(scheduler_config, scheduler_config_attr.name, v)
    scheduler_config.is_offline = False
    return LLM(
        model,
        speculative_model=speculative_model,
        num_speculative_tokens=num_speculative_tokens,
        tensor_parallel_size=tp or 4,
        pipeline_parallel_size=pp or 1,
        data_parallel_size=dp,
        devices=devices,
        scheduler_config=scheduler_config,
    )


def is_hf_model_id_like(model_id: str) -> bool:
    pattern = r"^[\w-]+/[\w.-]+$"
    return bool(re.match(pattern, model_id))
