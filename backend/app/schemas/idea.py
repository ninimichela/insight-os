from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.content import ContentResponse
from app.schemas.trend import TrendResponse


class IdeaGenerateRequest(BaseModel):
    projects: List[str] = Field(default_factory=lambda: ["in77", "in88"])
    ideas_per_project: int = Field(default=5, ge=1, le=10)


class IdeaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    project: str
    trend_id: Optional[UUID]
    priority: int
    outline: Optional[str]
    references: Optional[List[UUID]]
    recommendation_reason: Optional[str]
    execution_cost: str
    platforms: Optional[List[str]]
    status: str
    source_trends: Optional[List[UUID]]
    source_contents: Optional[List[UUID]]
    ai_trace: Optional[dict[str, Any]]
    created_at: Optional[datetime]


class IdeaListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[IdeaResponse]


class IdeaDetailResponse(IdeaResponse):
    trend: Optional[TrendResponse]
    reference_items: List[ContentResponse]


class IdeaGenerateResponse(BaseModel):
    generated: int
    items: List[IdeaResponse]
