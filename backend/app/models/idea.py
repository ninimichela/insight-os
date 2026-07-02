from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import DateTime, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    project: Mapped[str] = mapped_column(String, nullable=False, index=True)
    trend_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    priority: Mapped[int] = mapped_column(Integer, default=0, index=True)
    outline: Mapped[Optional[str]] = mapped_column(Text)
    references: Mapped[Optional[List[str]]] = mapped_column(JSON)
    recommendation_reason: Mapped[Optional[str]] = mapped_column(Text)
    execution_cost: Mapped[str] = mapped_column(String, default="medium", index=True)
    platforms: Mapped[Optional[List[str]]] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String, default="draft", index=True)
    source_trends: Mapped[Optional[List[str]]] = mapped_column(JSON)
    source_contents: Mapped[Optional[List[str]]] = mapped_column(JSON)
    ai_trace: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
