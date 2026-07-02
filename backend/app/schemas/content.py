from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ContentImportItem(BaseModel):
    title: str
    platform: str | None = None
    source_name: str | None = None
    source_type: str | None = None
    content_source: str = "article"
    url: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    raw_text: str | None = None


class ContentImportRequest(BaseModel):
    items: list[ContentImportItem] = Field(min_length=1)


class ContentImportResultItem(BaseModel):
    id: UUID | None = None
    title: str
    url: str | None = None
    content_status: str | None = None
    result: str
    reason: str | None = None


class ContentImportResponse(BaseModel):
    imported: int
    skipped: int
    items: list[ContentImportResultItem]


class ContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    content_source: str
    platform: str | None
    source_name: str | None
    source_type: str | None
    url: str | None
    author: str | None
    published_at: datetime | None
    collected_at: datetime | None
    summary: str | None
    raw_text: str | None
    tags: list[str] | None
    keywords: list[str] | None
    category: str | None
    suitable_for: list[str] | None
    heat_score: int
    brand_fit_in77: int
    brand_fit_in88: int
    innovation_score: int
    execution_score: int
    ai_reason: str | None
    analysis_version: str | None
    prompt_version: str | None
    brand_brain_version: str | None
    score_version: str | None
    workflow_version: str | None
    analysis_trace: dict | None
    content_status: str
    analysis_status: str


class ContentListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[ContentResponse]


class ContentAnalyzeRequest(BaseModel):
    content_ids: list[UUID] = Field(min_length=1)
    analysis_version: str = "gpt55-v1"
    force: bool = False


class ContentAnalyzeResultItem(BaseModel):
    id: UUID
    summary: str | None
    tags: list[str]
    keywords: list[str]
    category: str | None
    suitable_for: list[str]
    heat_score: int
    brand_fit_in77: int
    brand_fit_in88: int
    innovation_score: int
    execution_score: int
    analysis_version: str
    analysis_trace: dict


class ContentAnalyzeResponse(BaseModel):
    analyzed: int
    failed: int
    items: list[ContentAnalyzeResultItem]
    errors: list[dict]
