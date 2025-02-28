import argparse
from argparse import ArgumentParser
import asyncio
from dataclasses import dataclass, fields
import os
from pathlib import Path
from typing import AsyncGenerator, Callable, List, Optional, Tuple, Union

from transformers import PreTrainedTokenizerBase
from typing_extensions import TypedDict

from furiosa.native_runtime.llm import NativeLLMEngine  # type: ignore
from furiosa_llm.api import (
    CACHE_DIR,
    LLM,
    RequestOutput,
    SamplingParams,
    SchedulerConfig,
    TokenizerModeType,
)
from furiosa_llm.outputs import NativeOutputConverter
from furiosa_llm.server.utils import AnyTokenizer


# adopted from https://github.com/vllm-project/vllm/blob/main/vllm/inputs/data.py
class TextPrompt(TypedDict):
    """Schema for a text prompt."""

    prompt: str
    """The input text to be tokenized before passing to the model."""


class TokensPrompt(TypedDict):
    """Schema for a tokenized prompt."""

    prompt_token_ids: List[int]
    """A list of token IDs to pass to the model."""


SingletonPrompt = Union[str, TextPrompt, TokensPrompt]

# TODO: support ExplicitEncoderDecoderPrompt later
PromptType = Union[SingletonPrompt]


# A shallow version of transformers.tokenization_utils_base.BatchEncoding
@dataclass
class BatchEncoding:
    input_ids: List[int]
    attention_mask: List[int]


@dataclass
class EngineArgs:
    # Currently only artifact path is supported
    model: str
    pipeline_parallel_size: Optional[int] = None
    data_parallel_size: Optional[int] = None
    tokenizer: Optional[str] = None
    tokenizer_mode: TokenizerModeType = "auto"
    seed: Optional[int] = None
    devices: Optional[str] = None
    cache_dir: os.PathLike = CACHE_DIR
    paged_attention_num_blocks: Optional[int] = None

    # scheduler_config
    npu_queue_limit: Optional[int] = None
    max_processing_samples: Optional[int] = None
    spare_blocks_ratio: Optional[float] = None
    is_offline: Optional[bool] = None

    @staticmethod
    def add_cli_args(parser: ArgumentParser) -> ArgumentParser:
        """Shared CLI arguments for vLLM engine."""

        # Model arguments
        parser.add_argument(
            '--model',
            type=str,
            required=True,
            help='Path to the LLM engine artifact (Pretrained id will be supported in the future releases).',
        )
        parser.add_argument(
            '--tokenizer',
            type=str,
            default=EngineArgs.tokenizer,
            help='The name or path of a HuggingFace Transformers tokenizer.',
        )
        parser.add_argument(
            '--tokenizer-mode',
            type=str,
            default=EngineArgs.tokenizer_mode,
            help='The tokenizer mode. "auto" will use the fast tokenizer '
            'if available, and "slow" will always use the slow tokenizer.',
        )
        parser.add_argument(
            '--seed',
            type=int,
            default=EngineArgs.seed,
            help='The seed to initialize the random number generator for sampling.',
        )

        # Furiosa LLM specific arguments
        parser.add_argument(
            '--devices',
            type=str,
            default=EngineArgs.devices,
            help='The devices to run the model. It can be a single device or a list of devices. '
            'Each device can be either "npu:X" or "npu:X:*" where X is a specific device index. '
            'If not given, available devices will be used.',
        )
        parser.add_argument(
            '--pipeline-parallel-size',
            type=int,
            default=EngineArgs.pipeline_parallel_size,
            help='The size of the pipeline parallelism group. '
            'If not given, it will use the default pp value of the artifact.',
        )
        parser.add_argument(
            '--data-parallel-size',
            type=int,
            default=EngineArgs.data_parallel_size,
            help='The size of the data parallelism group. '
            'If not given, it will be inferred from total avaialble PEs and other parallelism degrees.',
        )
        parser.add_argument(
            '--cache-dir',
            type=Path,
            default=EngineArgs.cache_dir,
            help='The cache directory for temporarily generated files for this LLM instance. '
            'When its value is ``None``, caching is disabled. The default is "$HOME/.cache/furiosa/llm".',
        )
        parser.add_argument(
            '--paged-attention-num-blocks',
            type=int,
            default=EngineArgs.paged_attention_num_blocks,
            help='The maximum number of blocks that each k/v storage per layer can store. '
            'This argument must be given if model uses paged attention.',
        )
        parser.add_argument(
            '--npu-queue-limit',
            type=int,
            default=EngineArgs.npu_queue_limit,
            help='The NPU queue limit of the scheduler config.',
        )
        parser.add_argument(
            '--max-processing-samples',
            type=int,
            default=EngineArgs.max_processing_samples,
            help='The maximum processing samples. Used as an hint for the scheduler.',
        )
        parser.add_argument(
            '--spare-blocks-ratio',
            type=float,
            default=EngineArgs.spare_blocks_ratio,
            help='The spare blocks ratio. Used as an hint for the scheduler.',
        )
        parser.add_argument(
            '--is-offline',
            type=bool,
            default=EngineArgs.is_offline,
            help='If True, the scheduler will assume the workload will be offline scenario.',
        )
        return parser

    @classmethod
    def from_cli_args(cls, args: argparse.Namespace):
        attrs = [attr.name for attr in fields(cls)]
        engine_args = cls(**{attr: getattr(args, attr) for attr in attrs})
        return engine_args


@dataclass
class AsyncEngineArgs(EngineArgs):
    # TODO: add async-specific arguments

    @staticmethod
    def add_cli_args(parser: ArgumentParser) -> ArgumentParser:
        # TODO: add async-specific arguments
        parser = EngineArgs.add_cli_args(parser)
        return parser


# XXX: Since SamplingParams.max_tokens in Rust is not an Option type,
# we must ensure max_tokens is not None when SamplingParams is converted from Python to Rust.
# That's why the validation logic is duplicated here and in `LLM._verify_token_len_and_finalize_max_tokens`.
# Unfortunately there is no way to avoid this duplication while minimizing unnecessary encode/decode operations
# and keeping the Python API compatible with vLLM at the same time.
# The best solution would be to change SamplingParams.max_tokens in Rust to an Option type in the future.
# related PR: https://github.com/furiosa-ai/furiosa-runtime/pull/1260
class LLMEngineBase:
    prompt_max_seq_len: int
    max_seq_len_to_capture: int

    def _verify_token_len_and_finalize_max_tokens(
        self, sampling_params: SamplingParams, prompt_len: int
    ):
        if prompt_len > self.prompt_max_seq_len:
            raise ValueError(
                f"This model's maximum input context length is {self.prompt_max_seq_len} tokens, however you requested {prompt_len} tokens. Please reduce your prompt."
            )
        if sampling_params.max_tokens is None:
            sampling_params.max_tokens = self.max_seq_len_to_capture - prompt_len
        else:
            if sampling_params.max_tokens + prompt_len > self.max_seq_len_to_capture:
                # Same error message as OpenAI's response
                raise ValueError(
                    f"This model's maximum context length is {self.max_seq_len_to_capture} tokens, however you requested {sampling_params.max_tokens + prompt_len} tokens ({prompt_len} in your prompt; {sampling_params.max_tokens} for the completion). Please reduce your prompt; or completion length."
                )

    # TODO: Also do __verify_sampling_params_with_generator_config


class LLMEngine(LLMEngineBase):
    """
    LLMEngine receives requests and generates texts.
    Implements the API interface compatible with vLLM's `LLMEngine`, but this class is based on furiosa-runtime and FuriosaAI NPU.

    The request scheduling approach of this engine is different from that of vLLM's . While vLLM provides
    fine-grained control over decoding via the `step` method, this engine immediately begins
    text generation in the background as soon as a request is submitted via :meth:`add_request`,
    continuing asynchronously until completion. The generated results are placed in a queue that
    clients can retrieve by calling :meth:`step`.

    The Furiosa native engine handles scheduling and batching internally,
    allowing clients to retrieve results via :meth:`step` calls without needing to manage the decoding schedule.

    Please note that cancelling a request using `abort_request` is not supported for now.
    """

    def __init__(
        self,
        native_engine: NativeLLMEngine,
        tokenizer: AnyTokenizer,
        prompt_max_seq_len: int,
        max_seq_len_to_capture: int,
    ):
        self.native_engine = native_engine
        self.tokenizer = tokenizer
        self.prompt_max_seq_len = prompt_max_seq_len
        self.max_seq_len_to_capture = max_seq_len_to_capture

        self.queue: asyncio.Queue[RequestOutput] = asyncio.Queue()
        self.unfinished = 0

        self.aio_loop = asyncio.new_event_loop()

    @classmethod
    def from_llm(
        cls,
        llm: LLM,
    ) -> "LLMEngine":
        assert (
            llm.max_seq_len_to_capture is not None
        ), "Generative models must have max_seq_len_to_capture set."
        return cls(
            llm.engine,
            llm.tokenizer,
            llm.prompt_max_seq_len,
            llm.max_seq_len_to_capture,
        )

    @classmethod
    def from_engine_args(cls, args: EngineArgs) -> "LLMEngine":
        """
        Creates an LLMEngine from EngineArgs.
        """
        try:
            scheduler_config_ = SchedulerConfig.load(f"{args.model}/runtime_config.json")
            for scheduler_config_attr in fields(SchedulerConfig):
                if (v := getattr(args, scheduler_config_attr.name, None)) is not None:
                    setattr(scheduler_config_, scheduler_config_attr.name, v)
        except Exception:
            scheduler_config_ = None

        llm = LLM.load_artifact(
            path=args.model,
            pipeline_parallel_size=args.pipeline_parallel_size,
            data_parallel_size=args.data_parallel_size,
            tokenizer=args.tokenizer,
            tokenizer_mode=args.tokenizer_mode,
            seed=args.seed,
            devices=args.devices,
            cache_dir=args.cache_dir,
            paged_attention_num_blocks=args.paged_attention_num_blocks,
            scheduler_config=scheduler_config_,
        )

        return cls.from_llm(llm)

    def add_request(
        self,
        request_id: str,
        prompt: PromptType,
        sampling_params: SamplingParams,
    ) -> None:
        """
        Adds a new request to the engine.
        The decoding iteration starts immediately after adding the request.

        Args:
            request_id: The unique id of the request.
            prompt: The prompt to the LLM.
            sampling_params: The sampling parameters of the request.
        """
        self.unfinished += 1

        batch_encoding, prompt_getter = preprocess_prompt(prompt, self.tokenizer)
        prompt_token_ids = batch_encoding.input_ids
        self._verify_token_len_and_finalize_max_tokens(sampling_params, len(prompt_token_ids))

        n = sampling_params.n if sampling_params is not None else 1

        # TODO: call prompt_getter after calling `self.native_engine.stream_generate` to reduce latency
        prompt_str = prompt_getter()
        converter = NativeOutputConverter(
            self.tokenizer, n, sampling_params.output_kind, request_id, prompt_str, prompt_token_ids
        )
        self.aio_loop.create_task(self._process_request(converter, batch_encoding, sampling_params))

    async def _process_request(
        self,
        converter: NativeOutputConverter,
        batch_encoding: BatchEncoding,
        sampling_params: Optional[SamplingParams] = None,
    ) -> None:
        native_output_generator = self.native_engine.stream_generate(
            batch_encoding, sampling_params
        )
        async for request_output in converter.convert_stream(native_output_generator):
            await self.queue.put(request_output)

    def has_unfinished_requests(self) -> bool:
        """
        Returns True if there are unfinished requests.
        """
        return self.unfinished > 0

    def step(self) -> List[RequestOutput]:
        """
        Returns newly generated results of one decoding iteration from the queue.
        """
        req_output = self.aio_loop.run_until_complete(self.queue.get())
        if req_output.finished:
            self.unfinished -= 1
        return [req_output]


class AsyncLLMEngine(LLMEngineBase):
    """
    AsyncLLMEngine receives requests and generates texts asynchronously.
    Implements the API interface compatible with vLLM's `AsyncLLMEngine`, but this class is based on furiosa-runtime and FuriosaAI NPU.
    """

    def __init__(
        self,
        native_engine: NativeLLMEngine,
        tokenizer: AnyTokenizer,
        prompt_max_seq_len: int,
        max_seq_len_to_capture: int,
    ):
        self.native_engine = native_engine
        self.tokenizer = tokenizer
        self.prompt_max_seq_len = prompt_max_seq_len
        self.max_seq_len_to_capture = max_seq_len_to_capture

    @classmethod
    def from_llm(
        cls,
        llm: LLM,
    ) -> "AsyncLLMEngine":
        assert (
            llm.max_seq_len_to_capture is not None
        ), "Generative models must have max_seq_len_to_capture set."
        return cls(
            llm.engine,
            llm.tokenizer,
            llm.prompt_max_seq_len,
            llm.max_seq_len_to_capture,
        )

    @classmethod
    def from_engine_args(cls, args: AsyncEngineArgs) -> "AsyncLLMEngine":
        """
        Creates an AsyncLLMEngine from AsyncEngineArgs.
        """
        try:
            scheduler_config_ = SchedulerConfig.load(f"{args.model}/runtime_config.json")
            for scheduler_config_attr in fields(SchedulerConfig):
                if (v := getattr(args, scheduler_config_attr.name, None)) is not None:
                    setattr(scheduler_config_, scheduler_config_attr.name, v)
        except Exception:
            scheduler_config_ = None

        llm = LLM.load_artifact(
            path=args.model,
            pipeline_parallel_size=args.pipeline_parallel_size,
            data_parallel_size=args.data_parallel_size,
            tokenizer=args.tokenizer,
            tokenizer_mode=args.tokenizer_mode,
            seed=args.seed,
            devices=args.devices,
            cache_dir=args.cache_dir,
            paged_attention_num_blocks=args.paged_attention_num_blocks,
            scheduler_config=scheduler_config_,
        )

        return cls.from_llm(llm)

    async def generate(
        self,
        prompt: PromptType,
        sampling_params: SamplingParams,
        request_id: str,
    ) -> AsyncGenerator[RequestOutput, None]:
        """
        Generates text completions for a given prompt.

        Args:
            prompt: The prompt to the LLM. See :class:`~PromptType`
                for more details about the format of each input.
            sampling_params: The sampling parameters of the request.
            request_id: The unique id of the request.
        """
        # TODO: add a path to send add_special_tokens to preprocess_prompt
        batch_encoding, prompt_getter = preprocess_prompt(prompt, self.tokenizer)
        prompt_token_ids = batch_encoding.input_ids
        self._verify_token_len_and_finalize_max_tokens(sampling_params, len(prompt_token_ids))

        native_output_generator = self.native_engine.stream_generate(
            batch_encoding, sampling_params
        )

        prompt_str = prompt_getter()
        converter = NativeOutputConverter(
            self.tokenizer,
            sampling_params.n,
            sampling_params.output_kind,
            request_id,
            prompt_str,
            prompt_token_ids,
        )

        async for request_output in converter.convert_stream(native_output_generator):
            yield request_output

    # TODO
    # async def engine_step(self): ...
    # async def abort(self, request_id): ...


def preprocess_prompt(
    prompt: PromptType,
    tokenizer: PreTrainedTokenizerBase,
) -> Tuple[BatchEncoding, Callable[[], str]]:
    """
    Returns a tuple containing `(BatchEncoding, prompt string getter)`.

    The reason we want prompt as string is for `RequestOutput`, not as an input to the model.
    Therefore to reduce latency it is recommended to call `prompt_getter` after calling `self.native_engine.stream_generate`.

    **Note:** `add_special_tokens` is currently set to `False` by default.

    This is because the majority of use cases rely on chat templates, which already include special tokens.
    If special tokens need to be added manually, the caller must handle encoding themselves.

    While this approach may seem unconventional, it is necessary for compatibility with vLLM,
    as there is no straightforward way to pass `add_special_tokens` in this context.
    """
    if isinstance(prompt, str):
        prompt_str = prompt
        input_ids = tokenizer.encode(prompt_str, padding=False, add_special_tokens=False)
        return (
            BatchEncoding(input_ids=input_ids, attention_mask=[1] * len(input_ids)),
            lambda: prompt_str,
        )
    if isinstance(prompt, dict):
        if "prompt" in prompt:
            prompt_str = prompt["prompt"]  # type: ignore
            input_ids = tokenizer.encode(prompt_str, padding=False, add_special_tokens=False)
            return (
                BatchEncoding(input_ids=input_ids, attention_mask=[1] * len(input_ids)),
                lambda: prompt_str,
            )
        elif "prompt_token_ids" in prompt:
            input_ids = prompt["prompt_token_ids"]
            return BatchEncoding(
                input_ids=input_ids, attention_mask=[1] * len(input_ids)
            ), lambda: tokenizer.decode(input_ids, skip_special_tokens=True)

    raise ValueError(f"Unsupported prompt type: {type(prompt)}")
