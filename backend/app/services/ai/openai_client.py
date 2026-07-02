from __future__ import annotations

from typing import Any, Optional

from app.core.settings import settings
from app.services.ai.providers.mock_provider import MockProvider
from app.services.ai.providers.openai_provider import OpenAIProvider


_last_provider_name = "mock"
_last_model_name = "local-alpha-rules"
_last_fallback = True


def get_provider():
    if settings.ai_provider == "openai":
        return OpenAIProvider()
    return MockProvider()


def generate_json(system_prompt: str, payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Call the configured AI provider and parse JSON.

    Returns None when no API key is configured or the response cannot be parsed.
    Alpha can then fall back to deterministic local analysis.
    """
    global _last_provider_name, _last_model_name, _last_fallback
    provider = get_provider()
    _last_provider_name = provider.name
    _last_model_name = provider.model
    result = provider.generate_json(system_prompt, payload)
    _last_fallback = result is None
    return result


def get_provider_trace() -> dict[str, object]:
    return {
        "provider": _last_provider_name,
        "model": _last_model_name,
        "fallback": _last_fallback,
    }
