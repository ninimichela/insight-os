from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    week_start: Mapped[Optional[date]] = mapped_column(Date)
    week_end: Mapped[Optional[date]] = mapped_column(Date)
    markdown_content: Mapped[Optional[str]] = mapped_column(Text)
    trend_ids: Mapped[Optional[List[str]]] = mapped_column(JSON)
    idea_ids: Mapped[Optional[List[str]]] = mapped_column(JSON)
    content_ids: Mapped[Optional[List[str]]] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String, default="completed", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
