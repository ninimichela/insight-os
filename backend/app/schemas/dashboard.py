from __future__ import annotations

from datetime import datetime
from typing import Any, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.content import ContentResponse
from app.schemas.idea import IdeaResponse
from app.schemas.report import ReportResponse
from app.schemas.trend import TrendResponse


class DashboardStats(BaseModel):
    contents: int
    trends: int
    ideas: int
    reports: int


class DashboardActivity(BaseModel):
    time: Optional[datetime]
    type: str
    label: str
    count: Optional[int] = None
    target_id: Optional[UUID] = None
    meta: dict[str, Any] = {}


class TrendChange(BaseModel):
    status: str
    reason: str
    growth_rate: float


class DailySignal(BaseModel):
    item_id: Optional[UUID] = None
    title: str
    what: str
    why_now: str
    opportunity: str
    trend_change: Optional[TrendChange] = None
    score: int
    related_case_count: int


class DailyOpportunity(BaseModel):
    item_id: Optional[UUID] = None
    title: str
    what: str
    why_now: str
    opportunity: str
    score: int


class DailyIdeaSignal(BaseModel):
    item_id: Optional[UUID] = None
    title: str
    what: str
    why_now: str
    opportunity: str


class DailyIntelligence(BaseModel):
    todays_signals: List[DailySignal] = Field(default_factory=list)
    todays_opportunities: List[DailyOpportunity] = Field(default_factory=list)
    todays_ideas: List[DailyIdeaSignal] = Field(default_factory=list)


class DailyFeedbackRequest(BaseModel):
    item_type: Literal["content", "trend", "idea"]
    item_id: UUID
    useful: bool


class DailyFeedbackResponse(BaseModel):
    item_type: str
    item_id: UUID
    useful: bool
    adjustment: int


class DashboardResponse(BaseModel):
    stats: DashboardStats
    daily_intelligence: DailyIntelligence = Field(default_factory=DailyIntelligence)
    todays_signals: List[ContentResponse] = Field(default_factory=list)
    todays_opportunities: List[ContentResponse] = Field(default_factory=list)
    top_trends: List[TrendResponse]
    top_ideas: List[IdeaResponse]
    latest_report: Optional[ReportResponse]
    recent_activity: List[DashboardActivity]
