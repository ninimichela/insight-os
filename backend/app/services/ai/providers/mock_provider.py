from __future__ import annotations

from typing import Any, Optional


class MockProvider:
    name = "mock"
    model = "local-alpha-rules"

    def generate_json(self, system_prompt: str, payload: dict[str, Any]) -> Optional[dict[str, Any]]:
        return None

