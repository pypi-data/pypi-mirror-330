from argparse import Namespace
import logging

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, Response, StreamingResponse
import uvicorn

from furiosa_llm.server.middleware import RequestLoggerMiddleware
from furiosa_llm.server.models import load_llm_from_args
from furiosa_llm.server.protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    CompletionRequest,
    CompletionResponse,
    ErrorResponse,
)
from furiosa_llm.server.serving_chat import OpenAIServingChat
from furiosa_llm.server.serving_completions import OpenAIServingCompletion
from furiosa_llm.server.utils import parse_request

router = APIRouter()

openai_serving_completion: OpenAIServingCompletion
openai_serving_chat: OpenAIServingChat


@router.get("/health")
async def health() -> Response:
    """Health check."""
    # TODO: reflect LLM engine's health
    return Response(status_code=200)


@router.post("/v1/completions")
async def create_completion(raw_request: Request):
    request = await parse_request(raw_request, CompletionRequest)
    generator = await openai_serving_completion.create_completion(request)
    if isinstance(generator, ErrorResponse):
        return ORJSONResponse(content=generator.model_dump(), status_code=generator.code)
    elif isinstance(generator, CompletionResponse):
        return ORJSONResponse(content=generator.model_dump())

    return StreamingResponse(content=generator, media_type="text/event-stream")


@router.post("/v1/chat/completions")
async def create_chat_completion(raw_request: Request):
    request = await parse_request(raw_request, ChatCompletionRequest)
    generator = await openai_serving_chat.create_chat_completion(request)
    if isinstance(generator, ErrorResponse):
        return ORJSONResponse(content=generator.model_dump(), status_code=generator.code)
    elif isinstance(generator, ChatCompletionResponse):
        return ORJSONResponse(content=generator.model_dump())

    return StreamingResponse(content=generator, media_type="text/event-stream")


def init_app(
    args: Namespace,
) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=args.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    llm = load_llm_from_args(args)
    assert llm.is_generative_model

    override_chat_template = None
    if args.chat_template is not None:
        try:
            override_chat_template = open(args.chat_template).read()
        except Exception as e:
            raise ValueError(f"Error in reading chat template file: {e}")
    else:
        try:
            llm.tokenizer.get_chat_template()
        except Exception as e:
            raise ValueError(
                f"Failed to load chat template from tokenizer: {e}. Please specify a chat template using the --chat-template option."
            )

    global openai_serving_completion
    global openai_serving_chat
    openai_serving_completion = OpenAIServingCompletion(llm)
    openai_serving_chat = OpenAIServingChat(
        llm,
        override_chat_template,
        args.enable_auto_tool_choice,
        args.tool_call_parser,
        args.response_role,
    )

    return app


def run_server(args, **uvicorn_kwargs) -> None:
    app = init_app(args)

    if args.enable_payload_logging:
        app.add_middleware(RequestLoggerMiddleware)
        logging.warning(
            "Payload logging is enabled. This might expose sensitive data. If you do not fully understand the risks associated with this option, do not enable it."
        )
        # Disable uvicorn's access log
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["loggers"]["uvicorn.access"]["level"] = logging.CRITICAL + 1
        log_config["loggers"]["uvicorn.access"]["handlers"] = []
        log_config["loggers"]["uvicorn.access"]["propagate"] = False
        uvicorn_kwargs["log_config"] = log_config

    uvicorn.run(app, host=args.host, port=args.port, **uvicorn_kwargs)
