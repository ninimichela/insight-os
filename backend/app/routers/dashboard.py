from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dashboard import DailyFeedbackRequest, DailyFeedbackResponse, DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    return DashboardService(db).get_dashboard()


@router.post("/daily-intelligence/feedback", response_model=DailyFeedbackResponse)
def record_daily_intelligence_feedback(request: DailyFeedbackRequest, db: Session = Depends(get_db)):
    return DashboardService(db).record_feedback(request)
