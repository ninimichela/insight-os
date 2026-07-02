from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from app.models.trend import Trend

from .base_repository import BaseRepository


class TrendRepository(BaseRepository):
    """Database access for trend records."""

    model = Trend

    def replace_trends(self, trends: list[dict[str, Any]]) -> list[Trend]:
        self.session.query(Trend).delete()
        items = [Trend(**trend) for trend in trends]
        self.session.add_all(items)
        self.session.commit()
        for item in items:
            self.session.refresh(item)
        return items

    def list_trends(
        self,
        page: int = 1,
        page_size: int = 20,
        lifecycle: Optional[str] = None,
        category: Optional[str] = None,
    ) -> tuple[list[Trend], int]:
        query = self.session.query(Trend)
        if lifecycle:
            query = query.filter(Trend.lifecycle == lifecycle)
        if category:
            query = query.filter(Trend.category == category)

        total = query.count()
        offset = (page - 1) * page_size
        items = (
            query.order_by(Trend.trend_score.desc(), Trend.content_count.desc(), Trend.generated_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return items, total

    def get_trend_by_id(self, trend_id: UUID) -> Optional[Trend]:
        return self.get_by_id(trend_id)
