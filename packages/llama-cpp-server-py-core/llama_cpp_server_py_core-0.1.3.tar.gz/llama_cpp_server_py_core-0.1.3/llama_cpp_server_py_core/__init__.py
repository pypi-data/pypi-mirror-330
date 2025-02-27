import dataclasses
import os
import time
from pathlib import Path
from typing import Any, Dict, Iterable

from .api_models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    CompletionRequest,
    CompletionResponse,
    ModelCard,
    ModelList,
)
from .utils import (
    ServerConfig,
    ServerProcess,
    ServerResponse,
    ServerRetryStrategy,
    ServerStatus,
)


def get_server_binary_path(binary_name: str = "llama-server") -> str:
    if os.name == "nt":
        binary_name += ".exe"
    # Get binary file path in the package
    base_dir = Path(__file__).resolve().parent
    binary_path = base_dir / "lib" / binary_name

    if not binary_path.exists():
        raise FileNotFoundError(f"{binary_path} not found.")

    return str(binary_path)


class LlamaCppServer:
    def __init__(self, server_process: ServerProcess, server_config: ServerConfig):
        self.server = server_process
        self.server_config = server_config

    def health(self) -> ServerStatus:
        res = self.server.make_request("GET", "/health")
        if res.status_code == 200 and res.body["status"] == "ok":
            return ServerStatus.RUNNING
        return ServerStatus.ERROR

    def props(self) -> Dict[str, Any]:
        res = self.server.make_request("GET", "/props")
        if res.status_code == 200:
            return res.body
        raise Exception(
            f"Query props failed, status code: {res.status_code}, {res.body}"
        )

    def models(self) -> ModelList:
        res = self.server.make_request("GET", "/models")
        if res.status_code == 200:
            return ModelList(data=[ModelCard(**model) for model in res.body["data"]])
        raise Exception(
            f"Query models failed, status code: {res.status_code}, {res.body}"
        )

    def slots(self) -> Dict[str, Any]:
        res = self.server.make_request("GET", "/slots")
        if res.status_code == 501:
            if "error" in res.body and "message" in res.body["error"]:
                raise Exception(f"Query slots failed: {res.body['error']['message']}")
            raise Exception(f"Query slots failed: {res.body}")
        if res.status_code == 200:
            return res.body
        raise Exception(
            f"Query slots failed, status code: {res.status_code}, {res.body}"
        )

    def completion(self, request: CompletionRequest) -> CompletionResponse:
        json_request = dataclasses.asdict(request)
        json_request["stream"] = False
        res = self.server.make_request("POST", "/completion", data=json_request)
        if res.status_code not in [200, 201]:
            if "error" in res.body and "message" in res.body["error"]:
                raise Exception(
                    f"Send completion failed: {res.body['error']['message']}"
                )
            raise Exception(
                f"Send completion failed, status code: {res.status_code}, {res.body}"
            )
        else:
            return CompletionResponse.from_dict(res.body)

    def stream_completion(
        self, request: CompletionRequest
    ) -> Iterable[CompletionResponse]:
        json_request = dataclasses.asdict(request)
        json_request["stream"] = True
        res = self.server.make_stream_request("POST", "/completion", data=json_request)
        for data in res:
            yield CompletionResponse.from_dict(data)

    def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        json_request = dataclasses.asdict(request)
        json_request["stream"] = False
        res = self.server.make_request("POST", "/chat/completions", data=json_request)
        if res.status_code not in [200, 201]:
            if "error" in res.body and "message" in res.body["error"]:
                raise Exception(
                    f"Send chat completion failed: {res.body['error']['message']}"
                )
            raise Exception(
                f"Send chat completion failed, status code: {res.status_code}, {res.body}"
            )
        else:
            return ChatCompletionResponse.from_dict(res.body)

    def stream_chat_completion(
        self, request: ChatCompletionRequest
    ) -> Iterable[ChatCompletionStreamResponse]:
        json_request = dataclasses.asdict(request)
        json_request["stream"] = True
        res = self.server.make_stream_request(
            "POST", "/chat/completions", data=json_request
        )
        for data in res:
            yield ChatCompletionStreamResponse.from_dict(data)
