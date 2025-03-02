from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._client import USTBOpenAI

from .completions import Completions


class Chat:
    _client: USTBOpenAI
    completions: Completions

    def __init__(self, client: USTBOpenAI) -> None:
        self._client = client
        self.completions = Completions(self)
