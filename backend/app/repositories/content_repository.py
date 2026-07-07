from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from sqlalchemy import or_

from app.models.content import Content

from .base_repository import BaseRepository


class ContentRepository(BaseRepository):
    """Database access for content records."""

    model = Content

    def create_content(self, data: dict[str, Any]) -> Content:
        data.setdefault("content_status", "new")
        data.setdefault("analysis_status", "pending")
        data.setdefault("duplicate_status", "unique")
        return self.create(data)

    def bulk_create_contents(self, items: list[dict[str, Any]]) -> list[Content]:
        contents = []
        for item in items:
            item.setdefault("content_status", "new")
            item.setdefault("analysis_status", "pending")
            item.setdefault("duplicate_status", "unique")
            contents.append(Content(**item))
        self.session.add_all(contents)
        self.session.commit()
        for content in contents:
            self.session.refresh(content)
        return contents

    def list_contents(
        self,
        page: int = 1,
        page_size: int = 20,
        q: Optional[str] = None,
        platform: Optional[str] = None,
        source_name: Optional[str] = None,
        content_status: Optional[str] = None,
        sort: str = "collected_at",
        order: str = "desc",
    ) -> tuple[list[Content], int]:
        query = self.session.query(Content)

        if q:
            pattern = f"%{q}%"
            query = query.filter(or_(Content.title.ilike(pattern), Content.raw_text.ilike(pattern)))
        if platform:
            query = query.filter(Content.platform == platform)
        if source_name:
            query = query.filter(Content.source_name == source_name)
        if content_status:
            query = query.filter(Content.content_status == content_status)

        total = query.count()
        if sort == "created_at":
            sort = "collected_at"
        sort_column = getattr(Content, sort, Content.collected_at)
        if order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        offset = (page - 1) * page_size
        return query.offset(offset).limit(page_size).all(), total

    def get_content_by_id(self, content_id: UUID) -> Optional[Content]:
        return self.get_by_id(content_id)

    def get_content_by_url(self, url: str) -> Optional[Content]:
        return self.session.query(Content).filter(Content.url == url).first()

    def list_all_contents(self) -> list[Content]:
        return self.session.query(Content).all()

    def list_idea_eligible_contents(self) -> list[Content]:
        return (
            self.session.query(Content)
            .filter(Content.freshness_score > 60)
            .filter(Content.relevance_score > 70)
            .filter(Content.duplicate_status == "unique")
            .all()
        )

    def update_analysis_result(self, content_id: UUID, result: dict[str, Any]) -> Optional[Content]:
        return self.update(content_id, result)
