from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Content(Base):
    __tablename__ = "contents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content_source: Mapped[str] = mapped_column(String, default="article")
    platform: Mapped[str | None] = mapped_column(String)
    source_name: Mapped[str | None] = mapped_column(String)
    source_type: Mapped[str | None] = mapped_column(String)
    competitor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("competitors.id"))
    url: Mapped[str | None] = mapped_column(Text, unique=True)
    author: Mapped[str | None] = mapped_column(String)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    collected_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    summary: Mapped[str | None] = mapped_column(Text)
    raw_text: Mapped[str | None] = mapped_column(Text)
    cover_image: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    keywords: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    city: Mapped[str | None] = mapped_column(String)
    business_area: Mapped[str | None] = mapped_column(String)
    category: Mapped[str | None] = mapped_column(String)
    matched_brands: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    suitable_for: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    heat_score: Mapped[int] = mapped_column(Integer, default=0)
    brand_fit_in77: Mapped[int] = mapped_column(Integer, default=0)
    brand_fit_in88: Mapped[int] = mapped_column(Integer, default=0)
    innovation_score: Mapped[int] = mapped_column(Integer, default=0)
    execution_score: Mapped[int] = mapped_column(Integer, default=0)
    ai_reason: Mapped[str | None] = mapped_column(Text)
    evidence: Mapped[dict | None] = mapped_column(JSONB)
    analysis_version: Mapped[str | None] = mapped_column(String)
    prompt_version: Mapped[str | None] = mapped_column(String)
    brand_brain_version: Mapped[str | None] = mapped_column(String)
    score_version: Mapped[str | None] = mapped_column(String)
    workflow_version: Mapped[str | None] = mapped_column(String)
    analysis_trace: Mapped[dict | None] = mapped_column(JSONB)
    content_status: Mapped[str] = mapped_column(String, default="new")
    analysis_status: Mapped[str] = mapped_column(String, default="pending")
