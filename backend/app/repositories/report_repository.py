from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from app.models.report import Report

from .base_repository import BaseRepository


class ReportRepository(BaseRepository):
    """Database access for report records."""

    model = Report

    def create_report(self, data: dict[str, Any]) -> Report:
        data.setdefault("status", "completed")
        return self.create(data)

    def list_reports(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> tuple[list[Report], int]:
        query = self.session.query(Report)
        if status:
            query = query.filter(Report.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Report.created_at.desc()).offset(offset).limit(page_size).all()
        return items, total

    def get_report_by_id(self, report_id: UUID) -> Optional[Report]:
        return self.get_by_id(report_id)
