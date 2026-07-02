from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel

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


class DashboardResponse(BaseModel):
    stats: DashboardStats
    top_trends: List[TrendResponse]
    top_ideas: List[IdeaResponse]
    latest_report: Optional[ReportResponse]
    recent_activity: List[DashboardActivity]
