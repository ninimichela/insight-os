from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ContentImportItem(BaseModel):
    title: str
    platform: Optional[str] = None
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    content_source: str = "article"
    url: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    raw_text: Optional[str] = None


class ContentImportRequest(BaseModel):
    items: List[ContentImportItem] = Field(min_length=1)


class ContentImportResultItem(BaseModel):
    id: Optional[UUID] = None
    title: str
    url: Optional[str] = None
    content_status: Optional[str] = None
    result: str
    reason: Optional[str] = None


class ContentImportResponse(BaseModel):
    imported: int
    skipped: int
    items: List[ContentImportResultItem]


class ContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    content_source: str
    platform: Optional[str]
    source_name: Optional[str]
    source_type: Optional[str]
    url: Optional[str]
    author: Optional[str]
    published_at: Optional[datetime]
    collected_at: Optional[datetime]
    summary: Optional[str]
    raw_text: Optional[str]
    tags: Optional[List[str]]
    keywords: Optional[List[str]]
    category: Optional[str]
    suitable_for: Optional[List[str]]
    heat_score: int
    brand_fit_in77: int
    brand_fit_in88: int
    innovation_score: int
    execution_score: int
    ai_reason: Optional[str]
    analysis_version: Optional[str]
    prompt_version: Optional[str]
    brand_brain_version: Optional[str]
    score_version: Optional[str]
    workflow_version: Optional[str]
    analysis_trace: Optional[dict[str, Any]]
    content_status: str
    analysis_status: str


class ContentListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[ContentResponse]


class ContentAnalyzeRequest(BaseModel):
    content_ids: List[UUID] = Field(min_length=1)
    analysis_version: str = "gpt55-v1"
    force: bool = False


class ContentAnalyzeResultItem(BaseModel):
    id: UUID
    summary: Optional[str]
    tags: List[str]
    keywords: List[str]
    category: Optional[str]
    suitable_for: List[str]
    heat_score: int
    brand_fit_in77: int
    brand_fit_in88: int
    innovation_score: int
    execution_score: int
    analysis_version: str
    analysis_trace: dict[str, Any]


class ContentAnalyzeResponse(BaseModel):
    analyzed: int
    failed: int
    items: List[ContentAnalyzeResultItem]
    errors: List[dict[str, Any]]
