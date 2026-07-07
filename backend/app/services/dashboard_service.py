from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.idea import Idea
from app.models.report import Report
from app.models.trend import Trend
from app.schemas.dashboard import (
    DailyContentSignal,
    DailyIdeaSignal,
    DailyIntelligence,
    DailyTrendSignal,
    DashboardActivity,
    DashboardResponse,
    DashboardStats,
)


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
        todays_signals = (
            self.db.query(Content)
            .filter(Content.content_status == "analyzed")
            .filter(Content.duplicate_status == "unique")
            .order_by(Content.trend_score.desc(), Content.freshness_score.desc(), Content.collected_at.desc())
            .limit(10)
            .all()
        )
        todays_opportunities = (
            self.db.query(Content)
            .filter(Content.freshness_score > 60)
            .filter(Content.relevance_score > 70)
            .filter(Content.duplicate_status == "unique")
            .order_by(Content.relevance_score.desc(), Content.novelty_score.desc(), Content.collected_at.desc())
            .limit(10)
            .all()
        )
        return DashboardResponse(
            stats=stats,
            daily_intelligence=self._daily_intelligence(top_trends, todays_opportunities, top_ideas),
            todays_signals=todays_signals,
            todays_opportunities=todays_opportunities,
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

    def _daily_intelligence(self, trends: list[Trend], contents: list[Content], ideas: list[Idea]) -> DailyIntelligence:
        return DailyIntelligence(
            todays_trends=[
                DailyTrendSignal(
                    name=trend.topic,
                    explanation=trend.recommendation_reason or f"{trend.topic} 正在成为值得观察的内容信号。",
                    related_case_count=int((trend.analysis_trace or {}).get("reference_case_count", 0) or 0),
                )
                for trend in trends[:3]
            ],
            todays_signals=[
                DailyContentSignal(
                    title=content.title,
                    why_it_matters=content.insight or content.summary or "这条内容正在释放新的商业内容信号。",
                    how_to_use=content.business_opportunity or "可作为今日内容灵感观察。",
                    score=content.trend_score or content.relevance_score or 0,
                )
                for content in contents[:3]
            ],
            todays_ideas=[
                DailyIdeaSignal(
                    title=idea.title,
                    inspiration=idea.recommendation_reason or "来自今日趋势和内容信号。",
                    execution=self._first_line(idea.outline) or "执行：做成当天可发布的轻内容。",
                )
                for idea in ideas[:3]
            ],
        )

    def _first_line(self, value: str | None) -> str:
        if not value:
            return ""
        return next((line.strip() for line in value.splitlines() if line.strip()), "")
