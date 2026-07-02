from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import DateTime, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Content(Base):
    __tablename__ = "contents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content_source: Mapped[str] = mapped_column(String, default="article")
    platform: Mapped[Optional[str]] = mapped_column(String)
    source_name: Mapped[Optional[str]] = mapped_column(String)
    source_type: Mapped[Optional[str]] = mapped_column(String)
    competitor_id: Mapped[Optional[str]] = mapped_column(String)
    url: Mapped[Optional[str]] = mapped_column(Text, unique=True)
    author: Mapped[Optional[str]] = mapped_column(String)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    collected_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    summary: Mapped[Optional[str]] = mapped_column(Text)
    raw_text: Mapped[Optional[str]] = mapped_column(Text)
    cover_image: Mapped[Optional[str]] = mapped_column(Text)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)
    keywords: Mapped[Optional[List[str]]] = mapped_column(JSON)
    city: Mapped[Optional[str]] = mapped_column(String)
    business_area: Mapped[Optional[str]] = mapped_column(String)
    category: Mapped[Optional[str]] = mapped_column(String)
    matched_brands: Mapped[Optional[List[str]]] = mapped_column(JSON)
    suitable_for: Mapped[Optional[List[str]]] = mapped_column(JSON)
    heat_score: Mapped[int] = mapped_column(Integer, default=0)
    brand_fit_in77: Mapped[int] = mapped_column(Integer, default=0)
    brand_fit_in88: Mapped[int] = mapped_column(Integer, default=0)
    innovation_score: Mapped[int] = mapped_column(Integer, default=0)
    execution_score: Mapped[int] = mapped_column(Integer, default=0)
    ai_reason: Mapped[Optional[str]] = mapped_column(Text)
    evidence: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
    analysis_version: Mapped[Optional[str]] = mapped_column(String)
    prompt_version: Mapped[Optional[str]] = mapped_column(String)
    brand_brain_version: Mapped[Optional[str]] = mapped_column(String)
    score_version: Mapped[Optional[str]] = mapped_column(String)
    workflow_version: Mapped[Optional[str]] = mapped_column(String)
    analysis_trace: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
    content_status: Mapped[str] = mapped_column(String, default="new")
    analysis_status: Mapped[str] = mapped_column(String, default="pending")
