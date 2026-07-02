from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./alpha.db")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = os.getenv("OPENAI_MODEL", "gpt-5.5")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    ai_provider: str = os.getenv("AI_PROVIDER", "openai")
    enable_openai: bool = os.getenv("ENABLE_OPENAI", "true").lower() == "true"
    enable_local_analysis: bool = os.getenv("ENABLE_LOCAL_ANALYSIS", "true").lower() == "true"
    enable_brand_brain: bool = os.getenv("ENABLE_BRAND_BRAIN", "false").lower() == "true"
    enable_decision_engine: bool = os.getenv("ENABLE_DECISION_ENGINE", "false").lower() == "true"


settings = Settings()
