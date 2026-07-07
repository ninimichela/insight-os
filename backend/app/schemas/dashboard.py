from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
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


class DailyTrendSignal(BaseModel):
    name: str
    explanation: str
    related_case_count: int


class DailyContentSignal(BaseModel):
    title: str
    why_it_matters: str
    how_to_use: str
    score: int


class DailyIdeaSignal(BaseModel):
    title: str
    inspiration: str
    execution: str


class DailyIntelligence(BaseModel):
    todays_trends: List[DailyTrendSignal] = Field(default_factory=list)
    todays_signals: List[DailyContentSignal] = Field(default_factory=list)
    todays_ideas: List[DailyIdeaSignal] = Field(default_factory=list)


class DashboardResponse(BaseModel):
    stats: DashboardStats
    daily_intelligence: DailyIntelligence = Field(default_factory=DailyIntelligence)
    todays_signals: List[ContentResponse] = Field(default_factory=list)
    todays_opportunities: List[ContentResponse] = Field(default_factory=list)
    top_trends: List[TrendResponse]
    top_ideas: List[IdeaResponse]
    latest_report: Optional[ReportResponse]
    recent_activity: List[DashboardActivity]
