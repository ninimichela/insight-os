from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.content_repository import ContentRepository
from app.schemas.content import (
    ContentAnalyzeRequest,
    ContentAnalyzeResponse,
    ContentImportRequest,
    ContentImportResponse,
    ContentListResponse,
)
from app.services.content_service import ContentService

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/import", response_model=ContentImportResponse)
def import_content(request: ContentImportRequest, db: Session = Depends(get_db)):
    return ContentService(db).import_contents(request)


@router.get("", response_model=ContentListResponse)
def list_content(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    q: Optional[str] = None,
    platform: Optional[str] = None,
    source_name: Optional[str] = None,
    content_status: Optional[str] = None,
    sort: str = "collected_at",
    order: str = "desc",
):
    repository = ContentRepository(db)
    items, total = repository.list_contents(
        page=page,
        page_size=page_size,
        q=q,
        platform=platform,
        source_name=source_name,
        content_status=content_status,
        sort=sort,
        order=order,
    )
    return ContentListResponse(page=page, page_size=page_size, total=total, items=items)


@router.post("/analyze", response_model=ContentAnalyzeResponse)
def analyze_content(request: ContentAnalyzeRequest, db: Session = Depends(get_db)):
    return ContentService(db).analyze_contents(request)
