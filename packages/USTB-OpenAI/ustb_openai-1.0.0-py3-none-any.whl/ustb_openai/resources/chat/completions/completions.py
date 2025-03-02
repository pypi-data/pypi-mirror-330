from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    Iterable,
    Literal,
    Mapping,
    Optional,
    Union,
    overload
)

import httpx_sse

if TYPE_CHECKING:
    from ...._client import USTBOpenAI
    from ..chat import Chat

from ...._utils.form_request_builder import FormRequestBody
from ...._utils.openai_stream_adaptor import OpenAIStreamAdapter
from ....types.chat import ChatCompletion


class Completions:
    _chat: Chat
    _client: USTBOpenAI

    def __init__(self, chat: Chat) -> None:
        self._client = chat._client

    @overload
    def create(
        self,
        *,
        messages: Iterable[Mapping[str, str]],
        model: str,
        stream: Literal[True],
        **kwargs_ignored: Any
    ) -> Generator[ChatCompletion, Any, None]:
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[Mapping[str, str]],
        model: str,
        stream: Optional[Literal[False]] = None,
        **kwargs_ignored: Any
    ) -> ChatCompletion:
        ...

    def create(
        self,
        *,
        messages: Iterable[Mapping[str, str]],
        model: str,
        stream: Optional[bool] = None,
        **kwargs_ignored
    ) -> Union[ChatCompletion, Generator[ChatCompletion, Any, None]]:
        """Creates a new chat completion request.

        :param messages: The iterable of message dictionaries representing conversation history,
            each message dictionary in which must contain a `role` field and a `content` field;
        :param model: The identifier for the AI model to use;
        :param stream: If `True`, returns response chunks via generator,
            otherwise, returns complete response after full processing;
        :param kwargs_ignored: Additional keyword arguments are silently ignored;
        :rtype: ChatCompletion | Generator[ChatCompletion, Any, None];
        :returns: A full `ChatCompletion` for default, or a generator for `stream=True`;
        """
        data = {
            "content": "",
            "history": [],
            "compose_id": 3,
            "deep_search": 1,
            "model_name": model,
            "internet_search": 2
        }

        for m in messages:
            if "role" not in m or "content" not in m:
                raise ValueError("Role and content are required")
            role = m["role"].lower()
            content = m["content"].strip()
            if role not in ("user", "system", "assistant"):
                raise ValueError(f"Unsupported role: {role}")
            assert isinstance(data["history"], list)
            data["history"].append({
                "role": role,
                "content": content
            })

        if not data["history"]:
            raise ValueError("No message provided")
        last = data["history"].pop()
        if last["role"] != "user":
            raise ValueError(f"The last message must be a user prompt, got: {last['role']}")
        data["content"] = last["content"]

        body = FormRequestBody(data)
        headers = self._client._client.headers.copy()
        headers["Content-Type"] = body.get_content_type()
        generator = OpenAIStreamAdapter.generate_obj(
            httpx_sse.connect_sse(
                self._client._client,
                "POST",
                "/site/ai/compose_chat",
                content=body.get_content(),
                headers=headers
            )
        )

        if stream:
            return generator
        else:
            rst = ChatCompletion()
            for obj in generator:
                rst.choices[0].message.content += obj.choices[0].delta.content
            rst.choices[0].finish_reason = "stop"
            return rst
