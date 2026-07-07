from __future__ import annotations

import json
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.telemetry import telemetry
from app.models.content import Content
from app.repositories.content_repository import ContentRepository
from app.repositories.trend_repository import TrendRepository
from app.schemas.trend import TrendDetailResponse, TrendGenerateRequest, TrendGenerateResponse, TrendInsight
from app.services.ai.trend_analyzer import generate_trend_insight


@dataclass
class TrendCluster:
    topic: str
    contents: list[Content] = field(default_factory=list)
    tags: Counter[str] = field(default_factory=Counter)
    keywords: Counter[str] = field(default_factory=Counter)
    categories: Counter[str] = field(default_factory=Counter)


class TrendService:
    algorithm_version = "trend-rules-v1"
    score_weights = {
        "content_count": 0.4,
        "growth_rate": 0.3,
        "source_diversity": 0.2,
        "recency": 0.1,
    }

    def __init__(self, db: Session):
        self.db = db
        self.trend_repository = TrendRepository(db)
        self.content_repository = ContentRepository(db)
        self.aliases = self._load_aliases()

    def generate_trends(self, request: TrendGenerateRequest) -> TrendGenerateResponse:
        telemetry.increment("api.trends_generate.calls")
        start = time.perf_counter()
        contents = (
            self.db.query(Content)
            .filter(Content.content_status == "analyzed")
            .filter(Content.analysis_status == "completed")
            .filter(Content.duplicate_status == "unique")
            .all()
        )
        if not contents:
            contents = self.db.query(Content).all()

        anchor = self._anchor_datetime(contents)
        clusters = self._cluster_contents(contents)
        trend_payloads = []
        for cluster in clusters.values():
            if len(cluster.contents) < request.min_content_count:
                continue
            trend_payloads.append(self._build_trend_payload(cluster, anchor, request.lookback_days))

        trend_payloads.sort(key=lambda item: (item["trend_score"], item["content_count"]), reverse=True)
        trends = self.trend_repository.replace_trends(trend_payloads)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        telemetry.record_timing("api.trends_generate.time_ms", elapsed_ms)
        telemetry.increment("api.trends_generate.generated", len(trends))
        return TrendGenerateResponse(generated=len(trends), items=trends)

    def get_trend_detail(self, trend_id: UUID) -> Optional[TrendDetailResponse]:
        trend = self.trend_repository.get_trend_by_id(trend_id)
        if not trend:
            return None
        related_items = []
        for content_id in trend.related_contents or []:
            content = self.content_repository.get_content_by_id(UUID(str(content_id)))
            if content:
                related_items.append(content)
        top_competitors = self._top_sources(related_items)
        ai_insight = generate_trend_insight(trend, related_items, top_competitors)
        return TrendDetailResponse(
            id=trend.id,
            topic=trend.topic,
            category=trend.category,
            tags=trend.tags,
            keywords=trend.keywords,
            content_count=trend.content_count,
            growth_rate=trend.growth_rate,
            trend_score=trend.trend_score,
            lifecycle=trend.lifecycle,
            related_contents=trend.related_contents,
            recommended_projects=trend.recommended_projects,
            recommendation_reason=trend.recommendation_reason,
            generated_at=trend.generated_at,
            analysis_trace=trend.analysis_trace,
            related_content_items=related_items,
            top_competitors=top_competitors,
            ai_insight=TrendInsight(**ai_insight),
        )

    def _cluster_contents(self, contents: list[Content]) -> dict[str, TrendCluster]:
        clusters: dict[str, TrendCluster] = {}
        for content in contents:
            for signal in self._topic_signals(content):
                topic = self._normalize_topic(signal)
                if not topic:
                    continue
                cluster = clusters.setdefault(topic, TrendCluster(topic=topic))
                if content not in cluster.contents:
                    cluster.contents.append(content)
                for tag in content.tags or []:
                    cluster.tags[tag] += 1
                for keyword in content.keywords or []:
                    cluster.keywords[keyword] += 1
                if content.category:
                    cluster.categories[content.category] += 1
        return clusters

    def _build_trend_payload(self, cluster: TrendCluster, anchor: datetime, lookback_days: int) -> dict[str, Any]:
        previous_count, recent_count = self._window_counts(cluster.contents, anchor, lookback_days)
        growth_rate = self._growth_rate(previous_count, recent_count)
        source_diversity = self._source_diversity(cluster.contents)
        recency = self._recency_score(cluster.contents, anchor)
        content_count = len(cluster.contents)
        count_score = min(content_count / 30, 1.0)
        growth_score = min(max((growth_rate + 1) / 2, 0), 1.0)
        source_diversity_score = min(source_diversity / 5, 1.0)
        trend_score = round(
            100
            * (
                self.score_weights["content_count"] * count_score
                + self.score_weights["growth_rate"] * growth_score
                + self.score_weights["source_diversity"] * source_diversity_score
                + self.score_weights["recency"] * recency
            )
        )
        lifecycle = self._lifecycle(content_count, growth_rate)
        recommended_projects, recommendation_reason = self._recommend_projects(cluster)
        return {
            "topic": cluster.topic,
            "category": self._most_common(cluster.categories),
            "tags": self._top_items(cluster.tags),
            "keywords": self._top_items(cluster.keywords),
            "content_count": content_count,
            "growth_rate": round(growth_rate, 4),
            "trend_score": max(0, min(trend_score, 100)),
            "lifecycle": lifecycle,
            "related_contents": [str(content.id) for content in cluster.contents[:20]],
            "recommended_projects": recommended_projects,
            "recommendation_reason": recommendation_reason,
            "analysis_trace": {
                "algorithm_version": self.algorithm_version,
                "no_gpt_statistics": True,
                "score_weights": self.score_weights,
                "signals": ["tags", "keywords", "category"],
                "lookback_days": lookback_days,
                "previous_count": previous_count,
                "recent_count": recent_count,
                "source_diversity": source_diversity,
                "recency_score": round(recency, 4),
                "generated_from": content_count,
            },
        }

    def _topic_signals(self, content: Content) -> list[str]:
        signals = []
        signals.extend(content.tags or [])
        signals.extend(content.keywords or [])
        if content.category:
            signals.append(content.category)
        return [signal for signal in signals if signal]

    def _normalize_topic(self, value: str) -> str:
        key = value.strip()
        if not key:
            return ""
        return self.aliases.get(key) or self.aliases.get(key.lower()) or key

    def _window_counts(self, contents: list[Content], anchor: datetime, lookback_days: int) -> tuple[int, int]:
        recent_start = anchor - timedelta(days=lookback_days)
        previous_start = recent_start - timedelta(days=lookback_days)
        recent_count = 0
        previous_count = 0
        for content in contents:
            published_at = self._strip_timezone(content.published_at or content.collected_at or anchor)
            if recent_start <= published_at <= anchor:
                recent_count += 1
            elif previous_start <= published_at < recent_start:
                previous_count += 1
        return previous_count, recent_count

    def _growth_rate(self, previous_count: int, recent_count: int) -> float:
        if previous_count == 0:
            return 1.0 if recent_count > 0 else 0.0
        return (recent_count - previous_count) / previous_count

    def _source_diversity(self, contents: list[Content]) -> int:
        return len({content.source_name or content.platform or "unknown" for content in contents})

    def _recency_score(self, contents: list[Content], anchor: datetime) -> float:
        if not contents:
            return 0.0
        recent_start = anchor - timedelta(days=3)
        recent = 0
        for content in contents:
            published_at = self._strip_timezone(content.published_at or content.collected_at or anchor)
            if recent_start <= published_at <= anchor:
                recent += 1
        return recent / len(contents)

    def _lifecycle(self, content_count: int, growth_rate: float) -> str:
        if content_count <= 3 and growth_rate >= 0.5:
            return "Emerging"
        if growth_rate > 0.15:
            return "Rising"
        if growth_rate >= -0.1:
            return "Peak"
        return "Declining"

    def _recommend_projects(self, cluster: TrendCluster) -> tuple[list[str], str]:
        text = " ".join([cluster.topic, *list(cluster.tags), *list(cluster.keywords)]).lower()
        in77_terms = ["cbd", "citywalk", "city walk", "城市", "公园", "艺术", "自然", "松弛", "国贸"]
        in88_terms = ["王府井", "科技", "动漫", "漫画", "lego", "乐高", "高达", "室内", "游戏"]
        projects = []
        if any(term.lower() in text for term in in77_terms):
            projects.append("in77")
        if any(term.lower() in text for term in in88_terms):
            projects.append("in88")
        if not projects:
            projects = ["in77", "in88"]
        return projects, f"{cluster.topic} 与 {', '.join(projects)} 的内容语境匹配，可进入 Idea Engine 继续生成选题。"

    def _anchor_datetime(self, contents: list[Content]) -> datetime:
        dates = [self._strip_timezone(content.published_at) for content in contents if content.published_at]
        dates.extend(self._strip_timezone(content.collected_at) for content in contents if content.collected_at)
        return max(dates) if dates else datetime.utcnow()

    def _strip_timezone(self, value: datetime) -> datetime:
        if value.tzinfo:
            return value.replace(tzinfo=None)
        return value

    def _top_items(self, counter: Counter[str], limit: int = 8) -> list[str]:
        return [item for item, _ in counter.most_common(limit)]

    def _most_common(self, counter: Counter[str]) -> Optional[str]:
        if not counter:
            return None
        return counter.most_common(1)[0][0]

    def _top_sources(self, contents: list[Content], limit: int = 5) -> list[str]:
        counter = Counter(content.source_name or content.platform or "unknown" for content in contents)
        return [item for item, _ in counter.most_common(limit)]

    def _load_aliases(self) -> dict[str, str]:
        config_path = Path(__file__).resolve().parents[3] / "packages" / "config" / "topic_alias.json"
        if not config_path.exists():
            return {}
        data = json.loads(config_path.read_text(encoding="utf-8"))
        aliases = {}
        for key, value in data.items():
            aliases[key] = value
            aliases[key.lower()] = value
        return aliases
