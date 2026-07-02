from __future__ import annotations

from typing import Any, Optional, Protocol


class AIProvider(Protocol):
    name: str
    model: str

    def generate_json(self, system_prompt: str, payload: dict[str, Any]) -> Optional[dict[str, Any]]:
        ...

