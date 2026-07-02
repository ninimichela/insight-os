from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import DateTime, Float, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Trend(Base):
    __tablename__ = "trends"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    category: Mapped[Optional[str]] = mapped_column(String, index=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)
    keywords: Mapped[Optional[List[str]]] = mapped_column(JSON)
    content_count: Mapped[int] = mapped_column(Integer, default=0)
    growth_rate: Mapped[float] = mapped_column(Float, default=0.0)
    trend_score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    lifecycle: Mapped[str] = mapped_column(String, default="Emerging", index=True)
    related_contents: Mapped[Optional[List[str]]] = mapped_column(JSON)
    recommended_projects: Mapped[Optional[List[str]]] = mapped_column(JSON)
    recommendation_reason: Mapped[Optional[str]] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    analysis_trace: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
