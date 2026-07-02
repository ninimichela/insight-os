from dataclasses import dataclass

from app.core.settings import settings


@dataclass(frozen=True)
class FeatureFlags:
    enable_openai: bool = settings.enable_openai
    enable_local_analysis: bool = settings.enable_local_analysis
    enable_brand_brain: bool = settings.enable_brand_brain
    enable_decision_engine: bool = settings.enable_decision_engine
    enable_memory: bool = False
    enable_explainability: bool = False


features = FeatureFlags()

