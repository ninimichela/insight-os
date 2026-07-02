from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from app.models.idea import Idea

from .base_repository import BaseRepository


class IdeaRepository(BaseRepository):
    """Database access for idea records."""

    model = Idea

    def replace_ideas(self, ideas: list[dict[str, Any]]) -> list[Idea]:
        self.session.query(Idea).delete()
        items = [Idea(**idea) for idea in ideas]
        self.session.add_all(items)
        self.session.commit()
        for item in items:
            self.session.refresh(item)
        return items

    def list_ideas(
        self,
        page: int = 1,
        page_size: int = 20,
        project: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[list[Idea], int]:
        query = self.session.query(Idea)
        if project:
            query = query.filter(Idea.project == project)
        if status:
            query = query.filter(Idea.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        items = (
            query.order_by(Idea.priority.desc(), Idea.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return items, total

    def get_idea_by_id(self, idea_id: UUID) -> Optional[Idea]:
        return self.get_by_id(idea_id)
