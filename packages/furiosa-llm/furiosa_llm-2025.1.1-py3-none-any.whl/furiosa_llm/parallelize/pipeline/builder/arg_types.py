from dataclasses import dataclass
from typing import Any, Dict, List, Union

from furiosa_llm.parallelize.compiler_config import CompilerConfigContext
from furiosa_llm.parallelize.pipeline.types import TensorGenInfo


# TODO: better name?
@dataclass
class NonSharedPipelineBuildConfig:
    args_data: List[Any]
    kwargs_data: Dict[str, Union[TensorGenInfo, Any]]
    pipeline_name: str
    compile_config: "CompilerConfigContext"
    add_last_block_slice: bool = False
    remove_output_logit: bool = False
