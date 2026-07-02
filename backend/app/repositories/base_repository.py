from __future__ import annotations

from typing import Any
from uuid import UUID


class BaseRepository:
    """Shared CRUD helpers for SQLAlchemy repositories."""

    model = None

    def __init__(self, session):
        self.session = session

    def create(self, data: dict[str, Any]):
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get_by_id(self, item_id: UUID):
        return self.session.get(self.model, str(item_id))

    def list(self, offset: int = 0, limit: int = 20):
        return self.session.query(self.model).offset(offset).limit(limit).all()

    def update(self, item_id: UUID, data: dict[str, Any]):
        instance = self.get_by_id(item_id)
        if not instance:
            return None
        for key, value in data.items():
            setattr(instance, key, value)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete(self, item_id: UUID) -> bool:
        instance = self.get_by_id(item_id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True
