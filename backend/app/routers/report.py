from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportGenerateRequest, ReportGenerateResponse, ReportListResponse, ReportResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=ReportListResponse)
def list_reports(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = None,
):
    repository = ReportRepository(db)
    items, total = repository.list_reports(page=page, page_size=page_size, status=status)
    return ReportListResponse(page=page, page_size=page_size, total=total, items=items)


@router.post("/generate", response_model=ReportGenerateResponse)
def generate_report(request: ReportGenerateRequest, db: Session = Depends(get_db)):
    return ReportService(db).generate_report(request)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: UUID, db: Session = Depends(get_db)):
    report = ReportRepository(db).get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="report_not_found")
    return report
