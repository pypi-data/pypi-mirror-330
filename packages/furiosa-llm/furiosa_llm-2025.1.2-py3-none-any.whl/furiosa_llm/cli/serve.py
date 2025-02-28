import json

from furiosa_llm.server.app import run_server
from furiosa_llm.server.tool_parsers import ToolParserManager


def add_serve_args(serve_parser):
    serve_parser.add_argument(
        "model",
        type=str,
        help="The Hugging Face model id, or path to Furiosa model artifact. Currently only one model is supported per server.",
    )
    serve_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the server to (default: %(default)s)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to (default: %(default)s)",
    )
    serve_parser.add_argument(
        "--allowed-origins",
        type=json.loads,
        default=["*"],
        help='Allowed origins in json list (default: ["*"])',
    ),
    serve_parser.add_argument(
        "--enable-payload-logging",
        default=False,
        action="store_true",
        help="Enabling HTTP POST request payload logging. This logging can expose sensitive data,"
        " increasing the risk of data breaches and regulatory non-compliance (e.g., GDPR)."
        " It may also lead to excessive storage usage and potential security vulnerabilities if the logs are not properly protected."
        " If you do not fully understand the risks associated with this option, do not enable it.",
    )
    serve_parser.add_argument(
        "--chat-template",
        type=str,
        help="If given, the default chat template will be overridden with the given file. (Default: use chat template from tokenizer)",
    )
    serve_parser.add_argument(
        "--enable-auto-tool-choice",
        action="store_true",
        default=False,
        help="Enable auto tool choice for supported models. Use --tool-call-parser to specify which parser to use",
    )
    valid_tool_parsers = ToolParserManager.tool_parsers.keys()
    serve_parser.add_argument(
        "--tool-call-parser",
        type=str,
        metavar="{" + ",".join(valid_tool_parsers) + "}",
        default=None,
        help="Select the tool call parser depending on the model that you're using."
        " This is used to parse the model-generated tool call into OpenAI API "
        "format. Required for --enable-auto-tool-choice.",
    )
    serve_parser.add_argument(
        "--response-role",
        type=str,
        default="assistant",
        help="Response role for /v1/chat/completions API (default: %(default)s)",
    )
    serve_parser.add_argument(
        "-tp",
        "--tensor-parallel-size",
        type=int,
        help="Number of tensor parallel replicas. (default: 4)",
    )
    serve_parser.add_argument(
        "-pp",
        "--pipeline-parallel-size",
        type=int,
        help="Number of pipeline stages. (default: 1)",
    )
    serve_parser.add_argument(
        "-dp",
        "--data-parallel-size",
        type=int,
        help="Data parallelism size. If not given, it will be inferred from total avaialble PEs and other parallelism degrees.",
    )
    serve_parser.add_argument(
        "--devices",
        type=str,
        default=None,
        help='Devices to use (e.g. "npu:0,npu:1"). If unspecified, all available devices from the host will be used.',
    )
    serve_parser.add_argument(
        "--npu-queue-limit",
        type=int,
        default=None,
        help="If given, override the NPU queue limit of the scheduler config. (default: use value from artifact)",
    )
    serve_parser.add_argument(
        "--max-processing-samples",
        type=int,
        default=None,
        help="If given, override the maximum processing samples of the scheduler config. (default: use value from artifact)",
    )
    serve_parser.add_argument(
        "--spare-blocks-ratio",
        type=float,
        default=0.0,  # LLM-924
        help="The spare blocks ratio of the scheduler config (default: 0.0)."
        " Increasing this value might improve the performance but might lead to OOM.",
    )
    serve_parser.add_argument(
        "--speculative-model",
        type=str,
        default=None,
        help="The Hugging Face model id, or path to Furiosa model artifact for the speculative model.",
    )
    serve_parser.add_argument(
        "--num-speculative-tokens",
        type=int,
        default=None,
        help="The number of speculative tokens to sample from the draft model in speculative decoding.",
    )
    serve_parser.add_argument(
        "-draft-tp",
        "--speculative-draft-tensor-parallel-size",
        type=int,
        default=None,
        help="Number of tensor parallel replicas for the speculative model. (default: 4)",
    )
    serve_parser.add_argument(
        "-draft-pp",
        "--speculative-draft-pipeline-parallel-size",
        type=int,
        default=None,
        help="Number of pipeline stages for the speculative model. (default: 1)",
    )
    serve_parser.add_argument(
        "-draft-dp",
        "--speculative-draft-data-parallel-size",
        type=int,
        default=None,
        help="Data parallelism size for the speculative model. If not given, it will be inferred from total avaialble PEs and other parallelism degrees.",
    )

    serve_parser.set_defaults(dispatch_function=serve)


def serve(args):
    run_server(args)
