from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.idea import Idea
from app.models.report import Report
from app.models.trend import Trend
from app.schemas.dashboard import DashboardActivity, DashboardResponse, DashboardStats


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self) -> DashboardResponse:
        stats = DashboardStats(
            contents=self.db.query(func.count(Content.id)).scalar() or 0,
            trends=self.db.query(func.count(Trend.id)).scalar() or 0,
            ideas=self.db.query(func.count(Idea.id)).scalar() or 0,
            reports=self.db.query(func.count(Report.id)).scalar() or 0,
        )
        top_trends = (
            self.db.query(Trend)
            .order_by(Trend.trend_score.desc(), Trend.content_count.desc(), Trend.generated_at.desc())
            .limit(5)
            .all()
        )
        top_ideas = self.db.query(Idea).order_by(Idea.priority.desc(), Idea.created_at.desc()).limit(10).all()
        latest_report = self.db.query(Report).order_by(Report.created_at.desc()).first()
        return DashboardResponse(
            stats=stats,
            top_trends=top_trends,
            top_ideas=top_ideas,
            latest_report=latest_report,
            recent_activity=self._recent_activity(),
        )

    def _recent_activity(self) -> list[DashboardActivity]:
        activities: list[DashboardActivity] = []
        latest_content = self.db.query(Content).order_by(Content.collected_at.desc()).first()
        if latest_content:
            today_count = self.db.query(func.count(Content.id)).scalar() or 0
            activities.append(
                DashboardActivity(
                    time=latest_content.collected_at,
                    type="imported",
                    label="Imported contents",
                    count=today_count,
                    target_id=latest_content.id,
                )
            )
        latest_trend = self.db.query(Trend).order_by(Trend.generated_at.desc()).first()
        if latest_trend:
            trend_count = self.db.query(func.count(Trend.id)).scalar() or 0
            activities.append(
                DashboardActivity(
                    time=latest_trend.generated_at,
                    type="trend_generated",
                    label="Trend Generated",
                    count=trend_count,
                    target_id=latest_trend.id,
                )
            )
        latest_idea = self.db.query(Idea).order_by(Idea.created_at.desc()).first()
        if latest_idea:
            idea_count = self.db.query(func.count(Idea.id)).scalar() or 0
            activities.append(
                DashboardActivity(
                    time=latest_idea.created_at,
                    type="idea_generated",
                    label="Idea Generated",
                    count=idea_count,
                    target_id=latest_idea.id,
                )
            )
        latest_report = self.db.query(Report).order_by(Report.created_at.desc()).first()
        if latest_report:
            activities.append(
                DashboardActivity(
                    time=latest_report.created_at,
                    type="weekly_report_generated",
                    label="Weekly Report Generated",
                    count=1,
                    target_id=latest_report.id,
                    meta={"status": latest_report.status},
                )
            )
        activities.sort(key=lambda item: item.time or "", reverse=True)
        return activities[:8]
