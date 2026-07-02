from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.telemetry import telemetry
from app.models.content import Content
from app.models.trend import Trend
from app.repositories.content_repository import ContentRepository
from app.repositories.idea_repository import IdeaRepository
from app.repositories.trend_repository import TrendRepository
from app.schemas.idea import IdeaDetailResponse, IdeaGenerateRequest, IdeaGenerateResponse
from app.services.ai.idea_generator import generate_idea_copy


class IdeaService:
    algorithm_version = "idea-rules-v1"
    score_weights = {
        "trend_score": 0.4,
        "project_fit": 0.3,
        "reference_count": 0.2,
        "calendar_fit": 0.1,
    }

    def __init__(self, db: Session):
        self.db = db
        self.idea_repository = IdeaRepository(db)
        self.trend_repository = TrendRepository(db)
        self.content_repository = ContentRepository(db)
        self.project_rules = self._load_project_rules()

    def generate_ideas(self, request: IdeaGenerateRequest) -> IdeaGenerateResponse:
        telemetry.increment("api.ideas_generate.calls")
        start = time.perf_counter()
        trends, _ = self.trend_repository.list_trends(page=1, page_size=100)
        idea_payloads = []
        for project in request.projects:
            candidates = self._rank_project_trends(project, trends)
            if not candidates:
                continue
            for index in range(request.ideas_per_project):
                trend, project_fit = candidates[index % len(candidates)]
                related_contents = self._related_contents(trend)
                priority = self._priority(trend, project, project_fit, related_contents)
                copy = generate_idea_copy(project, trend, related_contents, priority)
                source_contents = [str(content.id) for content in related_contents[:8]]
                idea_payloads.append(
                    {
                        "title": copy["title"],
                        "project": project,
                        "trend_id": str(trend.id),
                        "priority": priority,
                        "outline": copy["outline"],
                        "references": source_contents,
                        "recommendation_reason": copy["recommendation_reason"],
                        "execution_cost": self._execution_cost(trend, related_contents),
                        "platforms": self._platforms(project),
                        "status": "draft",
                        "source_trends": [str(trend.id)],
                        "source_contents": source_contents,
                        "ai_trace": {
                            "algorithm_version": self.algorithm_version,
                            "no_gpt_scoring": True,
                            "score_weights": self.score_weights,
                            "project_fit": project_fit,
                            "reference_count": len(related_contents),
                            "calendar_fit": self._calendar_fit(trend),
                            "gpt_scope": ["title", "recommendation_reason", "outline"],
                        },
                    }
                )

        idea_payloads.sort(key=lambda item: (item["project"], -item["priority"]))
        ideas = self.idea_repository.replace_ideas(idea_payloads)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        telemetry.record_timing("api.ideas_generate.time_ms", elapsed_ms)
        telemetry.increment("api.ideas_generate.generated", len(ideas))
        return IdeaGenerateResponse(generated=len(ideas), items=ideas)

    def get_idea_detail(self, idea_id: UUID) -> Optional[IdeaDetailResponse]:
        idea = self.idea_repository.get_idea_by_id(idea_id)
        if not idea:
            return None
        trend = self.trend_repository.get_trend_by_id(UUID(str(idea.trend_id))) if idea.trend_id else None
        reference_items = []
        for content_id in idea.source_contents or idea.references or []:
            content = self.content_repository.get_content_by_id(UUID(str(content_id)))
            if content:
                reference_items.append(content)
        return IdeaDetailResponse(
            id=idea.id,
            title=idea.title,
            project=idea.project,
            trend_id=idea.trend_id,
            priority=idea.priority,
            outline=idea.outline,
            references=idea.references,
            recommendation_reason=idea.recommendation_reason,
            execution_cost=idea.execution_cost,
            platforms=idea.platforms,
            status=idea.status,
            source_trends=idea.source_trends,
            source_contents=idea.source_contents,
            ai_trace=idea.ai_trace,
            created_at=idea.created_at,
            trend=trend,
            reference_items=reference_items,
        )

    def _rank_project_trends(self, project: str, trends: list[Trend]) -> list[tuple[Trend, int]]:
        scored = []
        for trend in trends:
            project_fit = self._project_fit(project, trend)
            if project_fit <= 0 and project not in (trend.recommended_projects or []):
                continue
            scored.append((trend, project_fit))
        if not scored:
            scored = [(trend, 0) for trend in trends]
        scored.sort(key=lambda item: (self._priority(item[0], project, item[1], self._related_contents(item[0])), item[0].trend_score), reverse=True)
        return scored

    def _priority(self, trend: Trend, project: str, project_fit: int, related_contents: list[Content]) -> int:
        trend_component = trend.trend_score
        reference_component = min(len(related_contents) / 10, 1.0) * 100
        calendar_component = self._calendar_fit(trend)
        score = (
            self.score_weights["trend_score"] * trend_component
            + self.score_weights["project_fit"] * project_fit
            + self.score_weights["reference_count"] * reference_component
            + self.score_weights["calendar_fit"] * calendar_component
        )
        return max(0, min(round(score), 100))

    def _project_fit(self, project: str, trend: Trend) -> int:
        rules = self.project_rules.get(project, {})
        keywords = [keyword.lower() for keyword in rules.get("keywords", [])]
        signals = " ".join(
            [
                trend.topic or "",
                trend.category or "",
                *[tag or "" for tag in trend.tags or []],
                *[keyword or "" for keyword in trend.keywords or []],
            ]
        ).lower()
        matches = sum(1 for keyword in keywords if keyword in signals)
        if project in (trend.recommended_projects or []):
            matches += 2
        return max(0, min(round((matches / max(len(keywords), 1)) * 100), 100))

    def _calendar_fit(self, trend: Trend) -> int:
        signals = " ".join([trend.topic or "", *[tag or "" for tag in trend.tags or []], *[keyword or "" for keyword in trend.keywords or []]])
        seasonal_terms = ["夏天", "夏日", "Summer", "周末", "暑期", "夜生活", "展览"]
        if any(term.lower() in signals.lower() for term in seasonal_terms):
            return 90
        return 60

    def _related_contents(self, trend: Trend) -> list[Content]:
        items = []
        for content_id in trend.related_contents or []:
            content = self.content_repository.get_content_by_id(UUID(str(content_id)))
            if content:
                items.append(content)
        return items

    def _execution_cost(self, trend: Trend, related_contents: list[Content]) -> str:
        text = " ".join([trend.topic or "", *[tag or "" for tag in trend.tags or []], *[keyword or "" for keyword in trend.keywords or []]]).lower()
        if any(term in text for term in ["快闪", "展览", "演出", "活动"]):
            return "high"
        if len(related_contents) >= 5:
            return "low"
        return "medium"

    def _platforms(self, project: str) -> list[str]:
        return self.project_rules.get(project, {}).get("platforms", ["wechat", "xiaohongshu"])

    def _load_project_rules(self) -> dict[str, Any]:
        config_path = Path(__file__).resolve().parents[3] / "packages" / "config" / "project_rules.json"
        if not config_path.exists():
            return {}
        return json.loads(config_path.read_text(encoding="utf-8"))
