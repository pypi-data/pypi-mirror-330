from http import HTTPStatus
import json
from logging import Logger
import time
from typing import AsyncGenerator, AsyncIterator, List, Optional, Union

from furiosa_llm.api import LLM, RequestOutput
from furiosa_llm.llm_engine import AsyncLLMEngine
from furiosa_llm.outputs import CompletionOutput, RequestOutputKind
from furiosa_llm.server.protocol import (
    ChatCompletionNamedToolChoiceParam,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    DeltaFunctionCall,
    DeltaMessage,
    DeltaToolCall,
    ErrorResponse,
    FunctionCall,
    ToolCall,
    UsageInfo,
)
from furiosa_llm.server.serving_base import OpenAIServing
from furiosa_llm.server.tool_parsers import ToolParser, ToolParserManager
from furiosa_llm.server.utils import AnyTokenizer, ConversationMessage, random_uuid

logger = Logger(__name__)


class OpenAIServingChat(OpenAIServing):
    def __init__(
        self,
        llm: LLM,
        chat_template: Optional[str],
        enable_auto_tools: bool = False,
        tool_parser: Optional[str] = None,
        response_role: str = "assistant",
    ):
        self.async_llm_engine: AsyncLLMEngine = AsyncLLMEngine.from_llm(llm)
        self.tokenizer: AnyTokenizer = llm.tokenizer

        self.model_name = llm.model_metadata.pretrained_id
        self.response_role = response_role

        self.chat_template = chat_template
        self.enable_auto_tools = enable_auto_tools
        if self.enable_auto_tools:
            try:
                # XXX(n0gu): Copied from vllm. Currently this code path is not used since only llama3_json parser is supported,
                # but it may be used in the future.
                if tool_parser == "pythonic" and self.model_name.startswith("meta-llama/Llama-3.2"):
                    logger.warning("Llama3.2 models may struggle to emit valid pythonic tool calls")
                self.tool_parser = ToolParserManager.get_tool_parser(tool_parser)
            except Exception as e:
                raise TypeError(
                    "Error: --enable-auto-tool-choice requires "
                    f"tool_parser:'{tool_parser}' which has not "
                    "been registered"
                ) from e

        # Hack to pre-warm tokenizer and pre-compile default chat template
        try:
            self.tokenizer.apply_chat_template(
                [ConversationMessage({"role": "user", "content": "Hello!"})],
                chat_template=self.chat_template,
                add_generation_prompt=True,
                tokenize=True,
            )
        except Exception as e:
            logger.warning("Error in pre-warming tokenizer and chat template: %s", e)

    async def create_chat_completion(
        self,
        request: ChatCompletionRequest,
    ) -> Union[AsyncGenerator[str, None], ChatCompletionResponse, ErrorResponse]:
        """
        Completion API similar to OpenAI's API.

        See https://platform.openai.com/docs/api-reference/chat/create
        for the API specification. This API mimics the OpenAI
        ChatCompletion API.
        """
        try:
            messages = [ConversationMessage(m) for m in request.messages]  # type: ignore
            tools = (
                [tool.model_dump() for tool in request.tools]
                if (request.tools and request.tool_choice != "none")
                else None
            )
            # TODO: Support `chat_template` field in the request and use it as vllm does.
            prompt_text: str = self.tokenizer.apply_chat_template(
                messages,
                tools=tools,
                chat_template=self.chat_template,
                add_generation_prompt=True,
                tokenize=False,
            )
        except Exception as e:
            logger.error("Error in applying chat template from request: %s", e)
            return self.create_error_response(str(e))

        try:
            sampling_params = request.to_sampling_params()
        except ValueError as e:
            return self.create_error_response(str(e))

        request_id = f"chat-{random_uuid()}"

        stream = (
            request.stream
            and (request.best_of is None or request.n == request.best_of)
            and not request.use_beam_search
        )
        if stream:
            sampling_params.output_kind = RequestOutputKind.DELTA
            result_generator = self.async_llm_engine.generate(
                prompt_text, sampling_params, request_id
            )
            return self.chat_completion_stream_generator(
                request,
                result_generator,
                request_id,
            )

        try:
            sampling_params.output_kind = RequestOutputKind.FINAL
            result_generator = self.async_llm_engine.generate(
                prompt_text, sampling_params, request_id
            )
            return await self.chat_completion_full_generator(
                request,
                result_generator,
                request_id,
            )
        except ValueError as e:
            # TODO(vllm): Use a vllm-specific Validation Error
            return self.create_error_response(str(e))

    async def chat_completion_stream_generator(
        self,
        request: ChatCompletionRequest,
        result_generator: AsyncIterator[RequestOutput],
        request_id: str,
    ) -> AsyncGenerator[str, None]:
        created_time = int(time.time())

        num_choices = 1 if request.n is None else request.n
        previous_num_tokens = [0] * num_choices
        finish_reason_sent = [False] * num_choices
        usage_prompt_tokens = 0
        usage_completion_tokens = 0

        if isinstance(request.tool_choice, ChatCompletionNamedToolChoiceParam):
            tool_choice_function_name = request.tool_choice.function.name
        else:
            tool_choice_function_name = None

        # Determine whether tools are in use with "auto" tool choice
        tool_choice_auto = (
            not tool_choice_function_name
            and request.tools
            and self.tool_parser
            and self.enable_auto_tools
            and request.tool_choice in ['auto', None]
        )

        all_previous_token_ids: Optional[List[List[int]]]
        if tool_choice_auto:
            # These are only required in "auto" tool choice case
            previous_texts = [""] * num_choices
            all_previous_token_ids = [[]] * num_choices
        else:
            previous_texts, all_previous_token_ids = None, None

        # Prepare the tool parser if it's needed
        try:
            if tool_choice_auto and self.tool_parser:
                tool_parsers: List[Optional[ToolParser]] = [
                    self.tool_parser(self.tokenizer)
                ] * num_choices
            else:
                tool_parsers = [None] * num_choices
        except Exception as e:
            logger.exception("Error in tool parser creation.")
            data = self.create_streaming_error_response(str(e))
            yield f"data: {data}\n\n"
            yield "data: [DONE]\n\n"
            return

        first_iteration = True
        try:
            async for res in result_generator:
                if first_iteration:
                    usage_prompt_tokens = len(res.prompt_token_ids)
                    role = self.get_chat_request_role(request)
                    for i in range(num_choices):
                        choice_data = ChatCompletionResponseStreamChoice(
                            index=i,
                            delta=DeltaMessage(
                                role=role,
                                content="",
                            ),
                            logprobs=None,
                            finish_reason=None,
                        )
                        chunk = ChatCompletionStreamResponse(
                            id=request_id,
                            object="chat.completion.chunk",
                            created=created_time,
                            choices=[choice_data],
                            model=self.model_name,
                        )

                        data = chunk.model_dump_json(exclude_unset=True)
                        yield f"data: {data}\n\n"

                    first_iteration = False

                for output in res.outputs:
                    usage_completion_tokens += len(output.token_ids)
                    i = output.index
                    tool_parser = tool_parsers[i]

                    if finish_reason_sent[i]:
                        continue

                    delta_text = output.text

                    if not delta_text and not output.token_ids and not previous_num_tokens[i]:
                        # Chunked prefill case, don't return empty chunks
                        continue
                    if delta_text == "" and output.finish_reason is None:
                        # EOS case, don't return empty content
                        continue

                    delta_message: Optional[DeltaMessage]

                    # handle streaming deltas for tools with named tool_choice
                    if tool_choice_function_name:
                        delta_message = DeltaMessage(
                            tool_calls=[
                                DeltaToolCall(
                                    function=DeltaFunctionCall(
                                        name=tool_choice_function_name, arguments=delta_text
                                    ),
                                )
                            ]
                        )

                    # handle streaming deltas for tools with "auto" tool choice
                    elif tool_choice_auto:
                        assert previous_texts is not None
                        assert all_previous_token_ids is not None
                        assert tool_parser is not None
                        # TODO optimize manipulation of these lists
                        previous_text = previous_texts[i]
                        previous_token_ids = all_previous_token_ids[i]
                        current_text = previous_text + delta_text
                        current_token_ids = previous_token_ids + list(output.token_ids)

                        delta_message = tool_parser.extract_tool_calls_streaming(
                            previous_text=previous_text,
                            current_text=current_text,
                            delta_text=delta_text,
                            previous_token_ids=previous_token_ids,
                            current_token_ids=current_token_ids,
                            delta_token_ids=output.token_ids,
                            request=request,
                        )

                        # update the previous values for the next iteration
                        previous_texts[i] = current_text
                        all_previous_token_ids[i] = current_token_ids

                    # Handle streaming of content-only delta messages
                    # Following OpenAI's convention: when the delta contains no content and only includes
                    # a finish reason, return an empty delta object that serializes to {"delta": {}}
                    elif not output.token_ids and output.finish_reason is not None:
                        delta_message = DeltaMessage()
                    else:
                        delta_message = DeltaMessage(content=delta_text)

                    # set the previous values for the next iteration
                    previous_num_tokens[i] += len(output.token_ids)

                    # if the message delta is None (e.g. because it was a
                    # "control token" for tool calls or the parser otherwise
                    # wasn't ready to send a token, then
                    #   get the next token without streaming a chunk
                    if delta_message is None:
                        continue

                    if output.finish_reason is None:
                        # Send token-by-token response for each request.n
                        choice_data = ChatCompletionResponseStreamChoice(
                            index=i, delta=delta_message, finish_reason=None
                        )

                    # if the model is finished generating
                    else:
                        # check to make sure we haven't "forgotten" to stream
                        #   any tokens that were generated but previously
                        #   matched by partial json parsing
                        # only happens if we are NOT using guided decoding
                        auto_tools_called = False
                        if tool_parser:
                            auto_tools_called = len(tool_parser.prev_tool_call_arr) > 0
                            index = (
                                len(tool_parser.prev_tool_call_arr) - 1 if auto_tools_called else 0
                            )
                        else:
                            index = 0

                        if (
                            self._should_check_for_unstreamed_tool_arg_tokens(delta_message, output)
                            and tool_parser
                        ):
                            latest_delta_len = 0
                            if (
                                isinstance(delta_message.tool_calls[0].function, DeltaFunctionCall)
                            ) and isinstance(delta_message.tool_calls[0].function.arguments, str):
                                latest_delta_len = len(
                                    delta_message.tool_calls[0].function.arguments
                                )

                            # get the expected call based on partial JSON
                            # parsing which "autocompletes" the JSON
                            expected_call = json.dumps(
                                tool_parser.prev_tool_call_arr[index].get("arguments", {}),
                                ensure_ascii=False,
                            )

                            # get what we've streamed so far for arguments
                            # for the current tool
                            actual_call = tool_parser.streamed_args_for_tool[index]
                            if latest_delta_len > 0:
                                actual_call = actual_call[:-latest_delta_len]

                            # check to see if there's anything left to stream
                            remaining_call = expected_call.replace(actual_call, "", 1)
                            # set that as a delta message
                            delta_message = DeltaMessage(
                                tool_calls=[
                                    DeltaToolCall(
                                        function=DeltaFunctionCall(arguments=remaining_call)
                                    )
                                ]
                            )

                        # Send the finish response for each request.n only once
                        choice_data = ChatCompletionResponseStreamChoice(
                            index=i,
                            delta=delta_message,
                            finish_reason=(
                                output.finish_reason if not auto_tools_called else "tool_calls"
                            ),
                        )

                        finish_reason_sent[i] = True

                    chunk = ChatCompletionStreamResponse(
                        id=request_id,
                        object="chat.completion.chunk",
                        created=created_time,
                        choices=[choice_data],
                        model=self.model_name,
                    )

                    data = chunk.model_dump_json(exclude_unset=True)
                    yield f"data: {data}\n\n"

        except ValueError as e:
            # TODO(vllm): Use a vllm-specific Validation Error
            data = self.create_streaming_error_response(str(e))
            yield f"data: {data}\n\n"
        except Exception as e:
            logger.error("Error in chat completion stream: %s", e, exc_info=True)
            data = self.create_streaming_error_response(
                "internal server error",
                err_type="InternalServerError",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            yield f"data: {data}\n\n"

        if request.stream_options and request.stream_options.include_usage:
            # Send the final usage message after all response.n are finished
            usage = UsageInfo(
                prompt_tokens=usage_prompt_tokens,
                completion_tokens=usage_completion_tokens,
                total_tokens=usage_prompt_tokens + usage_completion_tokens,
            )
            chunk = ChatCompletionStreamResponse(
                id=request_id,
                object="chat.completion.chunk",
                created=created_time,
                choices=[],
                model=self.model_name,
                usage=usage,
            )
            data = chunk.model_dump_json(exclude_unset=True)
            yield f"data: {data}\n\n"

        # Send the final done message after all response.n are finished
        yield "data: [DONE]\n\n"

    async def chat_completion_full_generator(
        self,
        request: ChatCompletionRequest,
        result_generator: AsyncIterator[RequestOutput],
        request_id: str,
    ) -> Union[ErrorResponse, ChatCompletionResponse]:
        created_time = int(time.time())
        role = self.get_chat_request_role(request)

        choices: List[ChatCompletionResponseChoice] = []

        result = None
        async for result in result_generator:
            # only get the last `result`
            continue
        if result is None:
            return self.create_error_response("No result from model")

        usage_prompt_tokens = len(result.prompt_token_ids)
        usage_completion_tokens = 0

        for output in result.outputs:
            usage_completion_tokens += len(output.token_ids)
            auto_tools_called = False

            if (not self.enable_auto_tools or not self.tool_parser) and not isinstance(
                request.tool_choice, ChatCompletionNamedToolChoiceParam
            ):
                message = ChatMessage(role=role, content=output.text)

            # if the request uses tools and specified a tool choice
            elif (
                request.tool_choice
                and type(request.tool_choice) is ChatCompletionNamedToolChoiceParam
            ):
                message = ChatMessage(
                    role=role,
                    content="",
                    tool_calls=[
                        ToolCall(
                            function=FunctionCall(
                                name=request.tool_choice.function.name, arguments=output.text
                            )
                        )
                    ],
                )

            # if the request specifies to not use a tool
            elif not request.tools or request.tool_choice == "none":
                message = ChatMessage(role=role, content=output.text)

            # handle when there are tools and tool choice is auto
            elif (
                request.tools
                and (request.tool_choice == "auto" or request.tool_choice is None)
                and self.enable_auto_tools
                and self.tool_parser
            ):
                try:
                    tool_parser = self.tool_parser(self.tokenizer)
                except RuntimeError as e:
                    logger.exception("Error in tool parser creation.")
                    return self.create_error_response(str(e))

                tool_call_info = tool_parser.extract_tool_calls(output.text, request=request)
                # In the OpenAI API the finish_reason is "tools_called"
                # if the tool choice is auto and the model produced a tool
                # call. The same is not true for named function calls
                auto_tools_called = tool_call_info.tools_called
                if tool_call_info.tools_called:
                    message = ChatMessage(
                        role=role,
                        content=tool_call_info.content,
                        tool_calls=tool_call_info.tool_calls,
                    )
                else:
                    # FOR NOW make it a chat message; we will have to detect
                    # the type to make it later.
                    message = ChatMessage(role=role, content=output.text)
            else:
                logger.error(
                    "Error in chat_completion_full_generator - cannot determine"
                    " if tools should be extracted. Returning a standard chat "
                    "completion."
                )
                message = ChatMessage(role=role, content=output.text)
            choice_data = ChatCompletionResponseChoice(
                index=output.index,
                message=message,
                finish_reason=(
                    "tool_calls"
                    if auto_tools_called
                    else output.finish_reason if output.finish_reason else "stop"
                ),
            )
            choices.append(choice_data)

        usage = UsageInfo(
            prompt_tokens=usage_prompt_tokens,
            completion_tokens=usage_completion_tokens,
            total_tokens=usage_prompt_tokens + usage_completion_tokens,
        )
        response = ChatCompletionResponse(
            id=request_id,
            created=created_time,
            model=self.model_name,
            choices=choices,
            usage=usage,
            # TODO: support logprobs
            prompt_logprobs=None,
        )

        return response

    def get_chat_request_role(self, request: ChatCompletionRequest) -> str:
        if request.add_generation_prompt:
            return self.response_role
        else:
            return request.messages[-1]["role"]

    def _should_check_for_unstreamed_tool_arg_tokens(
        self,
        delta_message: Optional[DeltaMessage],
        output: CompletionOutput,
    ) -> bool:
        """
        Check to see if we should check for unstreamed tool arguments tokens.
        This is only applicable when auto tool parsing is enabled, the delta
        is a tool call with arguments.
        """

        # yapf: disable
        return bool(
            # if there is a delta message that includes tool calls which
            # include a function that has arguments
            output.finish_reason is not None
            and self.enable_auto_tools and self.tool_parser and delta_message
            and delta_message.tool_calls and delta_message.tool_calls[0]
            and delta_message.tool_calls[0].function
            and delta_message.tool_calls[0].function.arguments is not None
        )
