from __future__ import annotations

from typing import Any, Optional

from app.core.features import features
from app.core.telemetry import telemetry
from app.core.settings import settings
from app.services.ai.providers.mock_provider import MockProvider
from app.services.ai.providers.openai_provider import OpenAIProvider


_last_provider_name = "mock"
_last_model_name = "local-alpha-rules"
_last_fallback = True


def get_provider():
    if settings.ai_provider == "openai" and features.enable_openai:
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
    telemetry.increment(f"ai.provider.{provider.name}.calls")
    result = provider.generate_json(system_prompt, payload)
    _last_fallback = result is None
    if _last_fallback:
        telemetry.increment("ai.fallback.count")
    return result


def get_provider_trace() -> dict[str, object]:
    return {
        "provider": _last_provider_name,
        "model": _last_model_name,
        "fallback": _last_fallback,
    }
