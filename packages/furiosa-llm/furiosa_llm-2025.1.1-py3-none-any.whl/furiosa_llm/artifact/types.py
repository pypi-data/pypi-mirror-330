import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, RootModel
from typing_extensions import Self

from furiosa_llm.models.metadata import LLMConfig, ModelMetadata

from ..models.config_types import (
    GeneratorConfig,
    ModelRewritingConfig,
    ParallelConfig,
    PipelineMetadata,
)

logger = logging.getLogger(__name__)


class ArtifactVersion(BaseModel):
    furiosa_llm: str
    furiosa_compiler: str


class ArtifactMetadata(BaseModel):
    artifact_id: str
    name: str
    timestamp: int
    version: ArtifactVersion


class ModelMetadataForArtifact(ModelMetadata):
    """
    Child class of ModelMetadata used for loading artifacts.
    The object doesn't cause any huggingface config / weight download
    for obtaining all configs needed for artifact loading.
    """

    config_: Optional[Dict[str, Any]] = None
    model_qname_: Optional[str] = None

    def __init__(
        self,
        pretrained_id: str,
        task_type: Optional[str] = None,
        llm_config: LLMConfig = LLMConfig(),
        hf_configs: Dict = {},
        model_weight_path: Optional[os.PathLike] = None,
        trust_remote_code: Optional[bool] = None,
        config_: Optional[Dict[str, Any]] = None,
        model_qname_: Optional[str] = None,
    ):
        super(ModelMetadataForArtifact, self).__init__(
            pretrained_id,
            task_type,
            llm_config,
            hf_configs,
            model_weight_path,
            trust_remote_code,
        )
        self.config_ = config_
        self.model_qname_ = model_qname_

    @classmethod
    def from_metadata(
        cls,
        model_metadata: ModelMetadata,
        config: Optional[Dict[str, Any]] = None,
        model_qname: Optional[str] = None,
    ) -> Self:
        return cls(
            **model_metadata.model_dump(),
            config_=config,
            model_qname_=model_qname,
        )

    @property
    def config_dict(self) -> Dict[str, Any]:
        if self.config_ is None:
            return super().config_dict
        return self.config_

    @property
    def model_qname(self) -> str:
        if self.model_qname_ is None:
            return super().model_qname
        return self.model_qname_


class Artifact(BaseModel):
    metadata: ArtifactMetadata

    devices: str
    generator_config: GeneratorConfig
    hf_config: Dict[str, Any]
    model_metadata: ModelMetadata
    model_rewriting_config: ModelRewritingConfig
    parallel_config: ParallelConfig

    pipelines: List[Dict[str, Any]] = []
    pipeline_metadata_list: Optional[List[PipelineMetadata]] = None

    # TODO: store this field somewhere else.
    max_prompt_len: Optional[int] = None

    def append_pipeline(self, pipeline_dict: Dict[str, Any]):
        self.pipelines.append(pipeline_dict)

    def export(self, path: Union[str, os.PathLike]):
        with open(path, "w") as f:
            f.write(RootModel[Artifact](self).model_dump_json(indent=2))

    @classmethod
    def load(cls, path: Union[str, os.PathLike]) -> "Artifact":
        try:
            with open(path) as f:
                o = json.load(f)
                return Artifact(**o)
        except Exception as e:
            logger.error(e)
            raise ValueError("Artifact schema mismatched.")


class RuntimeConfig(BaseModel):
    """
    * npu_queue_limit: Maximum number of tasks that can be queued in the hardward
    * max_processing_samples: Maximum number of samples that can be processed by the scheduler
    * spare_blocks_ratio: Ratio of spare blocks that are reserved by scheduler. Smaller value will force the scheduler to use dram aggressively
    * is_offline: If True, use strategies optimzed for offline scenario
    * paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store.
    * prefill_chunk_size: Prefill chunk size used for chunked prefill.
    """

    npu_queue_limit: int
    max_processing_samples: int
    spare_blocks_ratio: float
    is_offline: bool
    paged_attention_num_blocks: Optional[int] = None
    prefill_buckets: Optional[List[Tuple[int, int]]] = None
    decode_buckets: Optional[List[Tuple[int, int]]] = None
    prefill_chunk_size: Optional[int] = None

    def export(self, path: Union[str, os.PathLike]):
        with open(path, "w") as f:
            f.write(RootModel[RuntimeConfig](self).model_dump_json(indent=2))

    @classmethod
    def load(cls, path: Union[str, os.PathLike]) -> "RuntimeConfig":
        with open(path) as f:
            o = json.load(f)
            return RuntimeConfig(**o)
