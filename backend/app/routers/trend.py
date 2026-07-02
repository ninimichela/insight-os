from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.trend_repository import TrendRepository
from app.schemas.trend import TrendDetailResponse, TrendGenerateRequest, TrendGenerateResponse, TrendListResponse
from app.services.trend_service import TrendService

router = APIRouter(prefix="/trends", tags=["trends"])


@router.get("", response_model=TrendListResponse)
def list_trends(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    lifecycle: Optional[str] = None,
    category: Optional[str] = None,
):
    repository = TrendRepository(db)
    items, total = repository.list_trends(
        page=page,
        page_size=page_size,
        lifecycle=lifecycle,
        category=category,
    )
    return TrendListResponse(page=page, page_size=page_size, total=total, items=items)


@router.get("/{trend_id}", response_model=TrendDetailResponse)
def get_trend(trend_id: UUID, db: Session = Depends(get_db)):
    detail = TrendService(db).get_trend_detail(trend_id)
    if not detail:
        raise HTTPException(status_code=404, detail="trend_not_found")
    return detail


@router.post("/generate", response_model=TrendGenerateResponse)
def generate_trends(request: TrendGenerateRequest, db: Session = Depends(get_db)):
    return TrendService(db).generate_trends(request)
