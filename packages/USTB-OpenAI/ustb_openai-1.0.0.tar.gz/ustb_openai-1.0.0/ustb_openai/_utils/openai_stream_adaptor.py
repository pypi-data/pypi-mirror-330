from abc import ABCMeta, abstractmethod
from typing import (
    Any,
    ContextManager,
    Generator,
    Generic,
    Iterator,
    TypeVar
)
from typing_extensions import override

import httpx
from httpx_sse import EventSource

from ..api_models.compose_chat import ComposeChat, ComposeChatItem
from ..types.chat.chat_completion import ChatCompletion, ChatChoice, ChatContent
from .._exceptions import APIError

T = TypeVar("T")


class EventSourceConsumer(ABCMeta, Generic[T]):
    @classmethod
    @abstractmethod
    def iter_obj(cls, event_source: EventSource) -> Iterator[T]:
        raise NotImplementedError()

    @classmethod
    def generate_obj(
        cls,
        event_source_context: ContextManager[EventSource]
    ) -> Generator[T, Any, None]:
        def generator():
            with event_source_context as event_source:
                yield from cls.iter_obj(event_source)
        return generator()

    @staticmethod
    def raise_for_content_type(response: httpx.Response):
        ctt = response.headers.get("Content-Type", "")
        if "text/event-stream" not in ctt:
            if "application/json" in ctt:
                data = None
                try:
                    response.read()
                    data = response.json()
                except BaseException as e:
                    pass
                if isinstance(data, dict):
                    raise APIError(
                        "No event stream provided",
                        e=data.get("e", None),
                        m=data.get("m", None)
                    )
            raise APIError("No event stream provided (most likely due to API failure)")


class OpenAIStreamAdapter(EventSourceConsumer[ChatCompletion]):
    _event_source: EventSource

    def __init__(self, event_source: EventSource) -> None:
        self._event_source = event_source

    @staticmethod
    def _convert_chunk(compose_item: ComposeChatItem) -> ChatCompletion:
        return ChatCompletion(
            choices=[
                ChatChoice(
                    delta=ChatContent(content=compose_item.answer),
                    index=0,
                    finish_reason=None
                )
            ]
        )

    @classmethod
    @override
    def iter_obj(cls, event_source: EventSource) -> Iterator[ChatCompletion]:
        cls.raise_for_content_type(event_source.response)
        for sse_event in event_source.iter_sse():
            compose_chat = ComposeChat.model_validate(sse_event.json())
            if compose_chat.data and compose_chat.data.answer:
                yield cls._convert_chunk(compose_chat.data)
