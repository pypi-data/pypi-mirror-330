from enum import Enum
import functools
import os
import re
from typing import Any, Dict, Final, FrozenSet, Optional, Set, Union

from pydantic import BaseModel, field_serializer, field_validator, model_validator
import torch
from typing_extensions import Self

WEIGHT_QDTYPE_FIELD_NAME_IN_QFORMAT: Final[str] = "weight_dtype"
ACTIVATION_QDTYPE_FIELD_NAME_IN_QFORMAT: Final[str] = "act_dtype"
KVCACHE_QDTYPE_FIELD_NAME_IN_QFORMAT: Final[str] = "kv_dtype"


@functools.total_ordering
class AttentionType(str, Enum):
    VANILLA = "VANILLA"
    PAGED_ATTENTION = "PAGED_ATTENTION"
    # preallocate memory space for kv cache, return in-place updated kv cache (concat)
    PREALLOCATION_CONCAT = "PREALLOCATION_CONCAT"

    def __lt__(self, other):
        if not isinstance(other, AttentionType):
            return NotImplemented
        return self.value < other.value


@functools.total_ordering
class OptimizationConfig(BaseModel):
    attention_type: AttentionType = AttentionType.VANILLA
    optimize_rope: bool = False
    optimize_packed: bool = False
    decompose_layernorm: bool = False
    optimize_furiosa: bool = False
    use_unsplit_packed: bool = False
    compact_causal_mask: bool = False
    use_rngd_gelu: bool = False
    causal_mask_free_decoding: bool = False
    kv_cache_sharing_across_beams: bool = False
    inbound_beamsearch_softmax: bool = False
    # https://furiosa-ai.slack.com/archives/C06R68UU9DJ/p1720453142548739
    calculate_logit_only_for_last_token: bool = False
    optimized_for_speculative_decoding: bool = False

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other):
        return repr(self) < repr(other)

    def get_activated_options(self) -> FrozenSet[str]:
        return frozenset(
            key
            for key, value in self.model_dump().items()
            if value and key not in {"attention_type"}
        )

    def get_all_flags(self) -> FrozenSet[str]:
        return frozenset(key for key in self.model_dump() if key != "attention_type")

    def contains(self, other: "OptimizationConfig") -> bool:
        return self.get_enabled_opts().issuperset(other.get_enabled_opts())

    def get_enabled_opts(self) -> Set[str]:
        return {
            k
            for k, v in self.model_dump().items()
            if (k == "attention_type" and v != AttentionType.VANILLA)
            or (k != "attention_type" and v)
        }

    def with_optimizations(self, opts: Dict[str, Any]) -> "OptimizationConfig":
        new_dict = self.model_dump()
        new_dict.update(opts)
        return OptimizationConfig(**new_dict)


class QDtype(str, Enum):
    INT4 = "int4"
    INT8 = "int8"
    FP8 = "fp8"
    BF16 = "bf16"
    FP32 = "fp32"

    @classmethod
    def from_qformat_dtype(cls, dtype: str) -> "QDtype":
        if dtype == "int8":
            return QDtype.INT8
        elif dtype == "fp8-E4M3":
            return QDtype.FP8
        elif dtype == "bf16":
            return QDtype.BF16
        else:
            raise ValueError(f"Unsupported qformat dtype string: {dtype}")

    def to_qformat(self) -> str:
        if self == QDtype.INT4:
            return "int4"
        elif self == QDtype.INT8:
            return "int8"
        elif self == QDtype.FP8:
            return "fp8-E4M3"
        elif self == QDtype.BF16:
            return "bf16"
        else:
            raise ValueError(f"{self}.to_qformat_dtype() is not supported")

    def bits(self) -> int:
        if self == QDtype.INT4:
            return 4
        elif self in (QDtype.INT8, QDtype.FP8):
            return 8
        elif self == QDtype.BF16:
            return 16
        else:
            raise ValueError(f"{self}.bits() is not supported")

    def to_torch_dtype(self) -> torch.dtype:
        if self is QDtype.INT4:
            # NOTE: There's no int4 type in torch. int8 is used instead.
            return torch.int8
        elif self is QDtype.INT8:
            return torch.int8
        elif self is QDtype.FP8:
            # NOTE: We decided to use torch.int8 to represent fp8 in compression stack.
            return torch.int8
        elif self is QDtype.BF16:
            return torch.bfloat16
        elif self is QDtype.FP32:
            return torch.float32
        else:
            raise ValueError(f"{self} has no corresponding torch dtype")

    def suffix(self):
        if self is QDtype.INT4:
            return "4"
        elif self is QDtype.INT8:
            return "8"
        elif self is QDtype.FP8:
            return "8f"
        elif self is QDtype.BF16:
            return "16"
        else:
            raise ValueError(f"{self} is not supported")


def get_field_dtype_from_qformat(field_name: str, qformat_path: Union[os.PathLike, str]) -> QDtype:
    with open(qformat_path, "r") as f:
        metadata_line = f.readline()
    matched = re.search(rf"--{field_name} \S+\b", metadata_line)
    if not matched:
        raise ValueError(f"Cannot find kv_cache_dtype from '{metadata_line}'")
    dtype = matched.group().split()[-1]

    try:
        return QDtype.from_qformat_dtype(dtype)
    except Exception:
        raise RuntimeError(f"Failed to parse dtype information for {field_name} in qformat file.")


def get_kv_cache_dtype_from_qformat(qformat_path: Union[os.PathLike, str]) -> QDtype:
    return get_field_dtype_from_qformat(KVCACHE_QDTYPE_FIELD_NAME_IN_QFORMAT, qformat_path)


@functools.total_ordering
class QuantizationConfig(BaseModel):
    weight: QDtype
    activation: QDtype
    kv_cache: Optional[QDtype]
    use_mcp: bool = True

    @model_validator(mode="after")
    def validate_quantization_config(self):
        if not self.use_mcp and not self != QuantizationConfig.w_16_a_16_kv_16():
            raise ValueError(f"{self} type needs mcp.")
        return self

    @classmethod
    def from_qformat(cls, qformat_path: Union[os.PathLike, str]) -> Self:
        weight_type = get_field_dtype_from_qformat(
            WEIGHT_QDTYPE_FIELD_NAME_IN_QFORMAT, qformat_path
        )
        act_dtype = get_field_dtype_from_qformat(
            ACTIVATION_QDTYPE_FIELD_NAME_IN_QFORMAT, qformat_path
        )
        try:
            kv_dtype = get_kv_cache_dtype_from_qformat(qformat_path)
        except ValueError:
            kv_dtype = None
        return cls(
            weight=weight_type,
            activation=act_dtype,
            kv_cache=kv_dtype,
            use_mcp=True,
        )

    def __hash__(self) -> int:
        return hash(repr(self))

    @classmethod
    def w_i8_a_i8_kv_i8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.INT8, activation=QDtype.INT8, kv_cache=QDtype.INT8)

    @classmethod
    def w_i8_a_i8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.INT8, activation=QDtype.INT8, kv_cache=None)

    @classmethod
    def w_f8_a_f8_kv_f8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.FP8, activation=QDtype.FP8, kv_cache=QDtype.FP8)

    @classmethod
    def w_f8_a_f8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.FP8, activation=QDtype.FP8, kv_cache=None)

    @classmethod
    def w_4_a_16_kv_f8(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.INT4, activation=QDtype.BF16, kv_cache=QDtype.FP8)

    @classmethod
    def w_16_a_16_kv_16(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.BF16, activation=QDtype.BF16, kv_cache=QDtype.BF16)

    @classmethod
    def w_16_a_16_kv_16_no_mcp(cls) -> "QuantizationConfig":
        return cls(weight=QDtype.BF16, activation=QDtype.BF16, kv_cache=QDtype.BF16, use_mcp=False)

    @field_serializer('weight', 'activation', 'kv_cache')
    def serialize(self, dtype: Optional[QDtype]) -> Optional[str]:
        return dtype.value if dtype else None

    @field_validator('weight', 'activation', 'kv_cache', mode="before")
    @classmethod
    def deserialize(cls, dtype: Union[None, str, QDtype]) -> Optional[QDtype]:
        if dtype is None:
            return None
        if isinstance(dtype, QDtype):
            return dtype
        elif isinstance(dtype, str):
            return QDtype(dtype)
        raise ValueError(f"Invalid dtype: {dtype!r}")

    def __str__(self) -> str:
        return "W{}A{}{}{}".format(
            self.weight.suffix(),
            self.activation.suffix(),
            f"KV{self.kv_cache.suffix()}" if self.kv_cache else "",
            "_NO_MCP" if not self.use_mcp else "",
        )

    def __lt__(self, other):
        return str(self) < str(other)
