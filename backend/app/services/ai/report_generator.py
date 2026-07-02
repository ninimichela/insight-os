from __future__ import annotations

from typing import Any

from app.services.ai.openai_client import generate_json

from .prompt_loader import load_prompt


def get_report_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="report", name="weekly")


def generate_weekly_report_markdown(payload: dict[str, Any], fallback_markdown: str) -> str:
    result = generate_json(get_report_prompt(), payload)
    if result and result.get("markdown_content"):
        return result["markdown_content"]
    if result and result.get("markdown"):
        return result["markdown"]
    return fallback_markdown
