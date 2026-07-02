from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.content import ContentResponse


class TrendGenerateRequest(BaseModel):
    lookback_days: int = Field(default=7, ge=1, le=90)
    min_content_count: int = Field(default=1, ge=1, le=100)


class TrendResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    topic: str
    category: Optional[str]
    tags: Optional[List[str]]
    keywords: Optional[List[str]]
    content_count: int
    growth_rate: float
    trend_score: int
    lifecycle: str
    related_contents: Optional[List[UUID]]
    recommended_projects: Optional[List[str]]
    recommendation_reason: Optional[str]
    generated_at: Optional[datetime]
    analysis_trace: Optional[dict[str, Any]]


class TrendListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[TrendResponse]


class TrendInsight(BaseModel):
    why_hot: str
    watch_points: List[str]
    suitable_for: List[str]


class TrendDetailResponse(TrendResponse):
    related_content_items: List[ContentResponse]
    top_competitors: List[str]
    ai_insight: TrendInsight


class TrendGenerateResponse(BaseModel):
    generated: int
    items: List[TrendResponse]
