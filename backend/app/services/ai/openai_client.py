from __future__ import annotations

import json
import os
from typing import Any


def has_openai_key() -> bool:
    key = os.getenv("OPENAI_API_KEY", "")
    return bool(key and key != "sk-xxx")


def generate_json(system_prompt: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    """Call OpenAI and parse JSON.

    Returns None when no API key is configured or the response cannot be parsed.
    Alpha can then fall back to deterministic local analysis.
    """
    if not has_openai_key():
        return None

    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")
    response = client.chat.completions.create(
        model=model,
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
