from typing import Any, List, Tuple, Mapping

import random


class FormRequestBody:
    _data: Mapping[str, Any]
    _boundary: str
    _flattened_data: List[Tuple[str, str]]

    _BOUNDARY_PREFIX = "----WebKitFormBoundary"
    _BOUNDARY_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self, data: Mapping[str, Any]):
        self._data = data
        self._boundary = FormRequestBody.generate_boundary()
        self._flattened_data = FormRequestBody.flatten_data(data)

    @staticmethod
    def generate_boundary():
        return (
            FormRequestBody._BOUNDARY_PREFIX
            + "".join(random.choices(FormRequestBody._BOUNDARY_CHARS, k=16))
        )

    @staticmethod
    def flatten_data(data: Mapping[str, Any]) -> List[Tuple[str, str]]:
        def recurse_flatten(current_data: Any, parent_key: str) -> List[Tuple[str, str]]:
            items = []
            if isinstance(current_data, Mapping):
                for k, v in current_data.items():
                    final_k = f"{parent_key}[{k}]" if parent_key else str(k)
                    items.extend(recurse_flatten(v, final_k))
            elif isinstance(current_data, list):
                for i, v in enumerate(current_data):
                    final_k = f"{parent_key}[{i}]" if parent_key else str(i)
                    items.extend(recurse_flatten(v, final_k))
            else:
                items.append((parent_key, str(current_data)))
            return items
        return recurse_flatten(data, "")

    def get_content(self) -> bytes:
        lines = []
        for k, v in self._flattened_data:
            lines.append(f"--{self._boundary}")
            lines.append(f"Content-Disposition: form-data; name=\"{k}\"")
            lines.append("")
            lines.append(v)
        lines.append(f"--{self._boundary}--")
        return "\r\n".join(lines).encode("utf-8")

    def get_content_type(self) -> str:
        return f"multipart/form-data; boundary={self._boundary}"
