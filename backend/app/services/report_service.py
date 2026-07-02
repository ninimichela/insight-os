from __future__ import annotations

import time
from collections import Counter
from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.telemetry import telemetry
from app.models.content import Content
from app.models.idea import Idea
from app.models.trend import Trend
from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportGenerateRequest, ReportGenerateResponse
from app.services.ai.report_generator import generate_weekly_report_markdown


class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.report_repository = ReportRepository(db)

    def generate_report(self, request: ReportGenerateRequest) -> ReportGenerateResponse:
        telemetry.increment("api.reports_generate.calls")
        start = time.perf_counter()
        week_start, week_end = self._week_range(request.week_start, request.week_end)
        contents = self._weekly_contents(week_start, week_end)
        trends = self._top_trends()
        ideas = self._top_ideas()
        markdown = self._fallback_markdown(week_start, week_end, contents, trends, ideas)
        markdown = generate_weekly_report_markdown(
            {
                "week_start": week_start.isoformat(),
                "week_end": week_end.isoformat(),
                "contents": [self._content_payload(content) for content in contents],
                "trends": [self._trend_payload(trend) for trend in trends],
                "ideas": [self._idea_payload(idea) for idea in ideas],
                "rules": {
                    "no_rescoring": True,
                    "trend_order": "trends.trend_score desc",
                    "idea_order": "ideas.priority desc",
                    "output_format": "markdown",
                },
            },
            markdown,
        )
        title = f"北京商业内容观察｜Week {week_start.isocalendar()[1]:02d}"
        report = self.report_repository.create_report(
            {
                "title": title,
                "week_start": week_start,
                "week_end": week_end,
                "markdown_content": markdown,
                "trend_ids": [str(trend.id) for trend in trends],
                "idea_ids": [str(idea.id) for idea in ideas],
                "content_ids": [str(content.id) for content in contents],
                "status": "completed",
            }
        )
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        telemetry.record_timing("api.reports_generate.time_ms", elapsed_ms)
        telemetry.increment("api.reports_generate.generated")
        return ReportGenerateResponse(generated=1, item=report)

    def _week_range(self, requested_start: Optional[date], requested_end: Optional[date]) -> tuple[date, date]:
        if requested_start and requested_end:
            return requested_start, requested_end
        anchor = self._anchor_date()
        week_end = requested_end or anchor
        week_start = requested_start or (week_end - timedelta(days=6))
        return week_start, week_end

    def _anchor_date(self) -> date:
        latest_content = self.db.query(Content).order_by(Content.published_at.desc()).first()
        if latest_content and latest_content.published_at:
            return latest_content.published_at.date()
        return datetime.utcnow().date()

    def _weekly_contents(self, week_start: date, week_end: date) -> list[Content]:
        items = []
        for content in self.db.query(Content).all():
            content_date = None
            if content.published_at:
                content_date = content.published_at.date()
            elif content.collected_at:
                content_date = content.collected_at.date()
            if content_date and week_start <= content_date <= week_end:
                items.append(content)
        items.sort(key=lambda content: (content.heat_score, content.published_at or content.collected_at), reverse=True)
        return items

    def _top_trends(self) -> list[Trend]:
        return (
            self.db.query(Trend)
            .order_by(Trend.trend_score.desc(), Trend.content_count.desc(), Trend.generated_at.desc())
            .limit(10)
            .all()
        )

    def _top_ideas(self) -> list[Idea]:
        return self.db.query(Idea).order_by(Idea.priority.desc(), Idea.created_at.desc()).all()

    def _fallback_markdown(self, week_start: date, week_end: date, contents: list[Content], trends: list[Trend], ideas: list[Idea]) -> str:
        week_number = week_start.isocalendar()[1]
        in77_ideas = [idea for idea in ideas if idea.project == "in77"][:5]
        in88_ideas = [idea for idea in ideas if idea.project == "in88"][:5]
        source_counter = Counter(content.source_name or content.platform or "未知来源" for content in contents)
        reference_cases = contents[:5]
        lines = [
            f"# 北京商业内容观察｜Week {week_number:02d}",
            "",
            "## 1. 本周热点 TOP10",
        ]
        lines.extend(self._trend_lines(trends))
        lines.extend(
            [
                "",
                "## 2. 竞品内容观察",
            ]
        )
        if source_counter:
            lines.extend([f"- {source}：{count} 条内容" for source, count in source_counter.most_common(10)])
        else:
            lines.append("- 暂无本周内容数据。")
        lines.extend(
            [
                "",
                "## 3. 值得参考案例",
            ]
        )
        lines.extend(self._case_lines(reference_cases))
        lines.extend(
            [
                "",
                "## 4. in77 本周建议 ×5",
            ]
        )
        lines.extend(self._idea_lines(in77_ideas))
        lines.extend(
            [
                "",
                "## 5. in88 本周建议 ×5",
            ]
        )
        lines.extend(self._idea_lines(in88_ideas))
        lines.extend(
            [
                "",
                "## 6. 下周执行优先级",
            ]
        )
        lines.extend(self._priority_lines(ideas[:10]))
        lines.extend(
            [
                "",
                "## 7. 数据说明",
                f"- 周期：{week_start.isoformat()} 至 {week_end.isoformat()}",
                f"- 内容数量：{len(contents)}",
                f"- Trend IDs：{', '.join(str(trend.id) for trend in trends) or '无'}",
                f"- Idea IDs：{', '.join(str(idea.id) for idea in ideas) or '无'}",
                f"- Content IDs：{', '.join(str(content.id) for content in contents) or '无'}",
                "- 规则：Trend 排名读取 `trends.trend_score`；Idea 排名读取 `ideas.priority`；Report 不重新计算分数。",
            ]
        )
        return "\n".join(lines)

    def _trend_lines(self, trends: list[Trend]) -> list[str]:
        if not trends:
            return ["- 暂无已生成热点。"]
        return [
            f"{index}. {trend.topic}｜Score {trend.trend_score}｜{trend.lifecycle}｜内容 {trend.content_count} 条"
            for index, trend in enumerate(trends[:10], start=1)
        ]

    def _case_lines(self, contents: list[Content]) -> list[str]:
        if not contents:
            return ["- 暂无可引用案例。"]
        return [
            f"- {content.title}｜{content.source_name or content.platform or '未知来源'}｜{content.summary or '待补充摘要'}"
            for content in contents
        ]

    def _idea_lines(self, ideas: list[Idea]) -> list[str]:
        if not ideas:
            return ["- 暂无已生成选题。"]
        return [
            f"{index}. {idea.title}｜Priority {idea.priority}｜Trend {idea.trend_id}｜{idea.recommendation_reason or '待补充理由'}"
            for index, idea in enumerate(ideas, start=1)
        ]

    def _priority_lines(self, ideas: list[Idea]) -> list[str]:
        if not ideas:
            return ["- 暂无执行优先级。"]
        return [
            f"- {idea.project}｜{idea.title}｜Priority {idea.priority}｜Cost {idea.execution_cost}"
            for idea in ideas
        ]

    def _content_payload(self, content: Content) -> dict:
        return {
            "id": str(content.id),
            "title": content.title,
            "source_name": content.source_name,
            "summary": content.summary,
            "tags": content.tags,
            "keywords": content.keywords,
        }

    def _trend_payload(self, trend: Trend) -> dict:
        return {
            "id": str(trend.id),
            "topic": trend.topic,
            "trend_score": trend.trend_score,
            "lifecycle": trend.lifecycle,
            "content_count": trend.content_count,
        }

    def _idea_payload(self, idea: Idea) -> dict:
        return {
            "id": str(idea.id),
            "title": idea.title,
            "project": idea.project,
            "priority": idea.priority,
            "trend_id": idea.trend_id,
            "recommendation_reason": idea.recommendation_reason,
            "outline": idea.outline,
        }
