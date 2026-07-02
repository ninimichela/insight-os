from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReportGenerateRequest(BaseModel):
    week_start: Optional[date] = None
    week_end: Optional[date] = None


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    week_start: Optional[date]
    week_end: Optional[date]
    markdown_content: Optional[str]
    trend_ids: Optional[List[UUID]]
    idea_ids: Optional[List[UUID]]
    content_ids: Optional[List[UUID]]
    status: str
    created_at: Optional[datetime]


class ReportListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[ReportResponse]


class ReportGenerateResponse(BaseModel):
    generated: int
    item: ReportResponse
