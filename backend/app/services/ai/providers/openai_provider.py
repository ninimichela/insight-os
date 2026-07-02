from __future__ import annotations

import json
from typing import Any, Optional

from app.core.settings import settings


class OpenAIProvider:
    name = "openai"

    def __init__(self) -> None:
        self.model = settings.model_name

    def generate_json(self, system_prompt: str, payload: dict[str, Any]) -> Optional[dict[str, Any]]:
        if not settings.openai_api_key or settings.openai_api_key == "sk-xxx":
            return None

        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
            timeout=15,
        )
        content = response.choices[0].message.content
        if not content:
            return None
        return json.loads(content)
