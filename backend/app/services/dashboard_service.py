from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.idea import Idea
from app.models.report import Report
from app.models.trend import Trend
from app.schemas.dashboard import (
    DailyFeedbackRequest,
    DailyFeedbackResponse,
    DailyIdeaSignal,
    DailyIntelligence,
    DailyOpportunity,
    DailySignal,
    TrendChange,
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
        ranked_trends = sorted(trends, key=self._change_priority, reverse=True)
        return DailyIntelligence(
            todays_signals=[
                DailySignal(
                    item_id=trend.id,
                    title=self._clip(trend.topic, 20),
                    what=self._clip(f"{trend.topic} 出现内容变化。", 50),
                    why_now=self._clip(self._trend_change(trend).reason, 50),
                    opportunity=self._clip(trend.recommendation_reason or f"围绕 {trend.topic} 做成今日观察。", 50),
                    trend_change=self._trend_change(trend),
                    score=trend.trend_score,
                    related_case_count=int((trend.analysis_trace or {}).get("reference_case_count", 0) or 0),
                )
                for trend in ranked_trends[:3]
            ],
            todays_opportunities=[
                DailyOpportunity(
                    item_id=content.id,
                    title=self._clip(content.title, 20),
                    what=self._clip(content.summary or content.title, 50),
                    why_now=self._clip(content.insight or "新鲜且相关度较高，值得进入今日观察。", 50),
                    opportunity=self._clip(content.business_opportunity or "转化为一条轻量内容方向。", 50),
                    score=content.trend_score or content.relevance_score or 0,
                )
                for content in contents[:3]
            ],
            todays_ideas=[
                DailyIdeaSignal(
                    item_id=idea.id,
                    title=self._clip(idea.title, 20),
                    what=self._clip("生成一个今天可讨论的内容方向。", 50),
                    why_now=self._clip(idea.recommendation_reason or "来自今日趋势和内容信号。", 50),
                    opportunity=self._clip(self._first_line(idea.outline) or "执行：做成当天可发布的轻内容。", 50),
                )
                for idea in ideas[:3]
            ],
        )

    def record_feedback(self, request: DailyFeedbackRequest) -> DailyFeedbackResponse:
        adjustment = 5 if request.useful else -8
        model = {"content": Content, "trend": Trend, "idea": Idea}[request.item_type]
        item = self.db.get(model, str(request.item_id))
        if item:
            if request.item_type == "content":
                item.relevance_score = self._bounded_score((item.relevance_score or 0) + adjustment)
            elif request.item_type == "trend":
                item.trend_score = self._bounded_score((item.trend_score or 0) + adjustment)
            elif request.item_type == "idea":
                item.priority = self._bounded_score((item.priority or 0) + adjustment)
            self.db.commit()
        return DailyFeedbackResponse(
            item_type=request.item_type,
            item_id=request.item_id,
            useful=request.useful,
            adjustment=adjustment,
        )

    def _first_line(self, value: str | None) -> str:
        if not value:
            return ""
        return next((line.strip() for line in value.splitlines() if line.strip()), "")

    def _trend_change(self, trend: Trend) -> TrendChange:
        trace = trend.analysis_trace or {}
        previous_count = int(trace.get("previous_count", 0) or 0)
        recent_count = int(trace.get("recent_count", 0) or 0)
        growth_rate = float(trend.growth_rate or 0)
        if previous_count == 0 and recent_count > 0:
            return TrendChange(status="new", reason=f"过去7天突然出现 {recent_count} 条相关内容。", growth_rate=growth_rate)
        if growth_rate >= 0.3:
            return TrendChange(status="rising", reason=f"过去7天相关内容增长 {growth_rate:.0%}。", growth_rate=growth_rate)
        if growth_rate <= -0.2:
            return TrendChange(status="declining", reason=f"过去7天相关内容减少 {abs(growth_rate):.0%}。", growth_rate=growth_rate)
        if recent_count <= 2 and (trace.get("source_diversity", 0) or 0) >= 2:
            return TrendChange(status="unusual", reason="少量内容同时来自多个来源，属于异常信号。", growth_rate=growth_rate)
        return TrendChange(status="stable", reason="主题仍在出现，但变化不明显。", growth_rate=growth_rate)

    def _change_priority(self, trend: Trend) -> int:
        change = self._trend_change(trend)
        weights = {"new": 120, "rising": 100, "unusual": 85, "declining": 70, "stable": 30}
        return weights.get(change.status, 0) + min(trend.trend_score or 0, 100)

    def _bounded_score(self, value: int) -> int:
        return max(0, min(value, 100))

    def _clip(self, value: str, limit: int) -> str:
        clean = " ".join((value or "").split())
        return clean if len(clean) <= limit else f"{clean[:limit]}..."
