from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.idea_repository import IdeaRepository
from app.schemas.idea import IdeaDetailResponse, IdeaGenerateRequest, IdeaGenerateResponse, IdeaListResponse
from app.services.idea_service import IdeaService

router = APIRouter(prefix="/ideas", tags=["ideas"])


@router.get("", response_model=IdeaListResponse)
def list_ideas(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    project: Optional[str] = None,
    status: Optional[str] = None,
):
    repository = IdeaRepository(db)
    items, total = repository.list_ideas(page=page, page_size=page_size, project=project, status=status)
    return IdeaListResponse(page=page, page_size=page_size, total=total, items=items)


@router.get("/{idea_id}", response_model=IdeaDetailResponse)
def get_idea(idea_id: UUID, db: Session = Depends(get_db)):
    detail = IdeaService(db).get_idea_detail(idea_id)
    if not detail:
        raise HTTPException(status_code=404, detail="idea_not_found")
    return detail


@router.post("/generate", response_model=IdeaGenerateResponse)
def generate_ideas(request: IdeaGenerateRequest, db: Session = Depends(get_db)):
    return IdeaService(db).generate_ideas(request)
