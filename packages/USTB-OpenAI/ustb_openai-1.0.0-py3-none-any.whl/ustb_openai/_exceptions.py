from typing import Any, Dict, Optional


class USTBOpenAIException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


class APIError(USTBOpenAIException):
    def __init__(self, reason: str, e: Optional[int] = None, m: Optional[str] = None):
        detail = []
        if e is not None:
            detail.append(f"e={e}")
            if m is not None:
                detail.append(f"m={m}")
        super().__init__(reason, *detail)
