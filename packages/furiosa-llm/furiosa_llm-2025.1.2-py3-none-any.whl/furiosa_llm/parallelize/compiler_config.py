from dataclasses import dataclass
from enum import Enum
from functools import cache, cached_property, reduce
import glob
import logging
import operator
import os
from pathlib import Path
import re
from typing import List, Mapping, Optional, Set

import yaml

from furiosa_llm.models import ModelMetadata
from furiosa_llm.models.config_types import Bucket


class PipelineMode(Enum):
    UNKNOWN = "unknown"
    LLM_PREFILL = "prefill"
    LLM_DECODE = "decode"

    def __str__(self):
        return self.value

    @classmethod
    def _missing_(cls, value):
        if value is None:
            return cls.UNKNOWN


class BlockType(str, Enum):
    FIRST = "first"
    MID = "mid"
    LAST = "last"
    WHOLE = "whole"


# FIXME: CompilerConfigContext must provide more generic way to match between target node and compiler config.
# the following implementation is MLPerf-specific (mostly targets gptj and bert) and should be fixed in the future.
@dataclass
class CompilerConfigContext:
    model_metadata: ModelMetadata
    num_pe: Optional[int] = None
    block_type: Optional[BlockType] = None
    bucket: Optional[Bucket] = None
    phase: Optional[PipelineMode] = None
    beam_size: Optional[int] = None
    compiler_config_overrides: Optional[Mapping] = None

    @cached_property
    def model_family(self) -> str:
        model_cls = self.model_metadata.get_optimized_cls().__name__
        if model_cls == "LlamaForCausalLM":
            return "llama"
        elif model_cls == "GPTJForCausalLM":
            return "gptj"
        elif model_cls == "BertForQuestionAnswering":
            return "bert"
        else:
            return "unknown"

    @cached_property
    def quant_dtype(self) -> Optional[str]:
        quant_config = self.model_metadata.llm_config.quantization_config
        if quant_config is None:
            return None
        return str(quant_config).lower()

    def is_exact_match(self, other: "CompilerConfigMetadata") -> bool:
        # XXX: couldn't use `if not all(...)` because mypy cannot recognize it
        if (
            self.num_pe is None
            or self.block_type is None
            or self.bucket is None
            or self.phase is None
            or self.quant_dtype is None
        ):
            return False

        if self.phase == PipelineMode.LLM_DECODE and self.beam_size is not None:
            b = self.bucket.batch_size // self.beam_size
        else:
            b = self.bucket.batch_size

        if self.phase == PipelineMode.LLM_DECODE:
            matches_input_ids_cond = self.bucket.input_ids_size == other.input_ids_size
        else:
            matches_input_ids_cond = True

        if other.quant_dtype and other.quant_dtype in self.quant_dtype:
            matches_quant_dtype = True  # FIXME: naive condition
        else:
            matches_quant_dtype = False

        return (
            self.is_loose_match(other)
            and self.model_metadata.pretrained_id in other.compat_pretrained_ids
            and b == other.batch_size
            and self.bucket.attention_size == other.sequence_length
            and matches_input_ids_cond
            and matches_quant_dtype
        )

    def is_loose_match(self, other: "CompilerConfigMetadata") -> bool:
        return (
            self.model_family == other.model_family
            and self.num_pe == other.num_pe
            and self.phase == other.phase
            and self.block_type == other.block_type
        )

    def default_config(self) -> Mapping:
        if self.phase == PipelineMode.LLM_PREFILL:
            tactic_hint = "ForLlmModelPrefill"
        elif self.phase == PipelineMode.LLM_DECODE:
            tactic_hint = "ForLlmModelDecode"
        else:
            tactic_hint = "Default"  # XXX: for non-generative models

        return {
            "allow_unlowered_operators": False,
            "implicit_type_casting": False,
            "lowering_mode": "Optimal",
            "tactic_hint": tactic_hint,
            "instruction_mem_budget": 720896,  # For double buffering
        }

    def load_config(self) -> Mapping:
        logging.info(f"Loading compiler config for {self}")
        config: Optional[Mapping] = None
        all_config_meta = list_all_installed_config_metadata()
        for meta in all_config_meta:
            if self.is_exact_match(meta):
                logging.info(f"Found exact match compiler config at {meta.path}")
                config = yaml.safe_load(open(meta.path / "compile_config.yaml"))
                if self.is_selected_tactic_enabled():
                    config["SelectedTactics"] = meta.path / "selected_tactics/serialized/"  # type: ignore
                break
        if config is None:
            logging.info("Failed to locate exact match compiler config; looking for fallback")
            for meta in all_config_meta:
                if self.is_loose_match(meta):
                    logging.info(f"Found loose match compiler config at {meta.path}")
                    config = yaml.safe_load(open(meta.path / "compile_config.yaml"))
                    # do not use selected tactics here
                    break
        if config is None:
            logging.info(
                "Failed to locate loose match compiler config; using default compiler config"
            )
            config = self.default_config()

        if self.compiler_config_overrides is not None:
            config = {**config, **self.compiler_config_overrides}
        return config

    def is_selected_tactic_enabled(self) -> bool:
        return os.environ.get("ENABLE_SELECTED_TACTIC_HINT", "0") == "1"


@dataclass
class CompilerConfigMetadata:
    """
    The context of the compiler.
    The field definition is of compiler team's definition.
    """

    model_family: str
    compat_pretrained_ids: Set[str]
    num_pe: int
    quant_dtype: Optional[str]
    input_ids_size: Optional[int]

    phase: PipelineMode
    block_type: BlockType
    batch_size: int
    sequence_length: int

    path: Path

    @classmethod
    def from_path(cls, path: str) -> Optional["CompilerConfigMetadata"]:
        pat = re.compile(
            r"test_compile_"
            r"(?P<model>[a-z0-9_]+?)_"
            r"(?:(?P<quant_dtype>w\d+f?a\d+f?(?:kv\d+f?)?)_)?"
            r"(?:(?P<phase>prefill|decode|chunked_prefill)_)?"
            r"(?:(?P<block>first|mid|last|whole)_block_)"
            r"b(?P<batch_size>\d+)_s(?P<sequence_length>\d+(?:x\d+)?)(?:_i(?P<input_ids_size>\d+))?"
        )

        search = pat.search(path)
        if search is None:
            return None
        model, quant_dtype, phase, block, batch_size, sequence_length, input_ids_size = (
            search.groups()
        )

        # TODO: we should handle this `input_ids_size > 1` case more generally,
        # but fot now our naming is spec-decoding specific.
        if phase == "chunked_prefill":
            sequence_length = reduce(operator.mul, map(int, sequence_length.split("x")))
            assert input_ids_size
            input_ids_size = int(input_ids_size)
            phase = "prefill" if input_ids_size == sequence_length else "decode"
        elif "_spec_decode_" in path:
            match = re.search(r"_draft_(\d+)_", path)
            assert match is not None
            draft_length = int(match.group(1))
            input_ids_size = draft_length
            phase = "decode"
        elif phase == "decode":
            input_ids_size = 1
        else:
            input_ids_size = None

        return cls(
            cls._get_model_family(path),
            cls._get_compat_pretrained_ids(path),
            cls._get_num_pe(path),
            quant_dtype,
            input_ids_size,
            PipelineMode(phase),
            BlockType(block),
            int(batch_size),
            int(sequence_length),
            Path(path),
        )

    @classmethod
    def _get_model_family(cls, path: str) -> str:
        if "llama" in path or "solar" in path or "exaone" in path:
            return "llama"
        elif "gptj" in path:
            return "gptj"
        elif "bert" in path:
            return "bert"
        else:
            return "unknown"

    # XXX: this method is highly vulnerable to npu-tools test changes.
    @classmethod
    def _get_compat_pretrained_ids(cls, path: str) -> Set[str]:
        if "llama3_1_8b" in path:
            return {"meta-llama/Meta-Llama-3.1-8B-Instruct"}
        elif "llama3_1" in path:
            return {"meta-llama/Meta-Llama-3.1-70B-Instruct"}
        elif "llama" in path:
            return {"meta-llama/Llama-2-70b-chat-hf"}
        elif "gptj" in path:
            return {"furiosa-ai/mlperf-gpt-j-6b"}
        elif "bert" in path:
            return {"furiosa-ai/mlperf-bert-large"}
        elif "solar" in path:
            return {"upstage/SOLAR-10.7B-Instruct-v1.0"}
        elif "exaone" in path:
            return {
                "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
                "furiosa-ai/EXAONE-3.0-7.8B-Instruct-converted",
                "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct",
            }
        else:
            return set()

    @classmethod
    def _get_num_pe(cls, path: str) -> int:
        match = re.search(r"test-snapshot-(\d+)pe", path)
        if match is None:
            raise ValueError(f"Cannot find num_pe from {path}")
        return int(match.group(1))


@cache
def list_all_installed_configs_paths() -> List[str]:
    return glob.glob("/usr/share/furiosa/compiler/configs/*/*/")


@cache
def list_all_installed_config_metadata() -> List[CompilerConfigMetadata]:
    return [
        metadata
        for metadata in (
            CompilerConfigMetadata.from_path(path) for path in list_all_installed_configs_paths()
        )
        if metadata is not None
    ]
