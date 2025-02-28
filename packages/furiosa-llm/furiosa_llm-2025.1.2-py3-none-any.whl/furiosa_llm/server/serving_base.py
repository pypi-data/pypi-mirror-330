from http import HTTPStatus
import json

from furiosa_llm.server.protocol import ErrorResponse


class OpenAIServing:
    def create_error_response(
        self,
        message: str,
        err_type: str = "BadRequestError",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ) -> ErrorResponse:
        return ErrorResponse(message=message, type=err_type, code=status_code.value)

    def create_streaming_error_response(
        self,
        message: str,
        err_type: str = "BadRequestError",
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ) -> str:
        json_str = json.dumps(
            {
                "error": self.create_error_response(
                    message=message, err_type=err_type, status_code=status_code
                ).model_dump()
            }
        )
        return json_str
