from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from typing import Any, Iterable, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.models.content import Content
from app.services.reference_data import ReferenceCase, get_reference_data


TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "spm",
    "from",
    "share_from",
    "share_source",
    "timestamp",
}

COMMERCIAL_TERMS = [
    "商场",
    "商业",
    "品牌",
    "首店",
    "快闪",
    "活动",
    "展览",
    "艺术",
    "餐饮",
    "咖啡",
    "citywalk",
    "city walk",
    "王府井",
    "cbd",
    "国贸",
    "消费",
    "生活方式",
]

NOVELTY_TERMS = ["首店", "首发", "首次", "快闪", "限定", "新品", "开幕", "AI", "机器人", "联名", "IP", "高达", "乐高"]


@dataclass(frozen=True)
class DuplicateCheck:
    status: str
    matched_content_id: Optional[str] = None
    similarity: float = 0.0

    @property
    def is_duplicate(self) -> bool:
        return self.status in {"exact_url", "near_duplicate"}


class ContentIntelligenceEngine:
    """Deterministic content intelligence helpers for the v1 pipeline."""

    similarity_threshold = 0.88

    def __init__(self):
        self.reference_data = get_reference_data()

    def normalize_import_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(payload)
        normalized["title"] = self.clean_title(normalized.get("title") or "")
        if normalized.get("url"):
            normalized["url"] = self.normalize_url(normalized["url"])
        return normalized

    def normalize_url(self, url: str) -> str:
        value = (url or "").strip()
        if not value:
            return value
        parts = urlsplit(value)
        scheme = (parts.scheme or "https").lower()
        netloc = parts.netloc.lower()
        path = re.sub(r"/+$", "", parts.path or "")
        query_items = [
            (key, val)
            for key, val in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in TRACKING_PARAMS and not key.lower().startswith("utm_")
        ]
        query = urlencode(query_items, doseq=True)
        return urlunsplit((scheme, netloc, path, query, ""))

    def clean_title(self, title: str) -> str:
        clean = re.sub(r"\s+", " ", title or "").strip()
        clean = re.sub(r"[｜|]\s*(公众号|小红书|新闻|资讯)\s*$", "", clean, flags=re.IGNORECASE)
        clean = re.sub(r"^[#＃]+", "", clean).strip()
        return clean

    def check_duplicate(self, candidate: dict[str, Any], existing_contents: Iterable[Content]) -> DuplicateCheck:
        candidate_url = candidate.get("url")
        candidate_signature = self._similarity_signature(candidate.get("title"), candidate.get("raw_text"))
        best_match = DuplicateCheck(status="unique")

        for content in existing_contents:
            if candidate_url and content.url == candidate_url:
                return DuplicateCheck(status="exact_url", matched_content_id=str(content.id), similarity=1.0)
            if not candidate_signature:
                continue
            similarity = SequenceMatcher(
                None,
                candidate_signature,
                self._similarity_signature(content.title, content.raw_text),
            ).ratio()
            if similarity > best_match.similarity:
                best_match = DuplicateCheck(
                    status="near_duplicate" if similarity >= self.similarity_threshold else "unique",
                    matched_content_id=str(content.id),
                    similarity=round(similarity, 4),
                )

        if best_match.status != "near_duplicate":
            return DuplicateCheck(status="unique", similarity=round(best_match.similarity, 4))
        return best_match

    def score_content(self, content: Content, summary: str, tags: list[str], keywords: list[str], category: Optional[str]) -> dict[str, Any]:
        text = self._text_blob(content, tags, keywords, category)
        reference_matches = self.reference_data.find_matches(text, tags=tags, limit=3)
        freshness_score = self._freshness_score(content.published_at or content.collected_at)
        relevance_score = self._relevance_score(text, category, content.suitable_for or [], reference_matches)
        novelty_score = self._novelty_score(text, content.duplicate_status)
        content_trend_score = round(
            0.35 * freshness_score
            + 0.35 * relevance_score
            + 0.2 * novelty_score
            + 0.1 * min(content.heat_score or 0, 100)
        )
        return {
            "freshness_score": freshness_score,
            "relevance_score": relevance_score,
            "novelty_score": novelty_score,
            "trend_score": max(0, min(content_trend_score, 100)),
            "insight": self._why_it_matters(content, summary, tags, category, reference_matches),
            "business_opportunity": self._how_to_use(relevance_score, novelty_score, tags, keywords, reference_matches),
            "reference_cases": [case.title for case in reference_matches],
        }

    def is_idea_eligible(self, content: Content) -> bool:
        return (
            (content.freshness_score or 0) > 60
            and (content.relevance_score or 0) > 70
            and (content.duplicate_status or "unique") == "unique"
        )

    def _similarity_signature(self, title: Optional[str], raw_text: Optional[str]) -> str:
        text = f"{title or ''} {raw_text or ''}".lower()
        text = re.sub(r"https?://\S+", "", text)
        text = re.sub(r"\W+", "", text, flags=re.UNICODE)
        return text[:800]

    def _text_blob(self, content: Content, tags: list[str], keywords: list[str], category: Optional[str]) -> str:
        return " ".join(
            [
                content.title or "",
                content.raw_text or "",
                category or "",
                " ".join(tags or []),
                " ".join(keywords or []),
            ]
        ).lower()

    def _freshness_score(self, published_at: Optional[datetime]) -> int:
        if not published_at:
            return 50
        value = published_at.replace(tzinfo=None) if published_at.tzinfo else published_at
        age_days = max((datetime.utcnow() - value).days, 0)
        if age_days <= 1:
            return 100
        if age_days <= 3:
            return 88
        if age_days <= 7:
            return 74
        if age_days <= 14:
            return 58
        if age_days <= 30:
            return 42
        return 25

    def _relevance_score(self, text: str, category: Optional[str], suitable_for: list[str], reference_matches: list[ReferenceCase]) -> int:
        score = 42
        matches = sum(1 for term in COMMERCIAL_TERMS if term.lower() in text)
        score += min(matches * 7, 42)
        if category in {"商业地产", "艺术文化", "餐饮", "科技"}:
            score += 10
        if suitable_for:
            score += 6
        if reference_matches:
            score += min(len(reference_matches) * 4, 12)
        return max(0, min(score, 100))

    def _novelty_score(self, text: str, duplicate_status: Optional[str]) -> int:
        if duplicate_status == "near_duplicate":
            return 35
        score = 58
        matches = sum(1 for term in NOVELTY_TERMS if term.lower() in text)
        score += min(matches * 8, 34)
        return max(0, min(score, 100))

    def _why_it_matters(
        self,
        content: Content,
        summary: str,
        tags: list[str],
        category: Optional[str],
        reference_matches: list[ReferenceCase],
    ) -> str:
        if reference_matches and reference_matches[0].why_it_matters:
            return self._short_sentence(reference_matches[0].why_it_matters)
        primary_tag = tags[0] if tags else category or "商业内容"
        return self._short_sentence(f"{primary_tag} 正在从单点内容变成可持续的城市生活信号。")

    def _how_to_use(
        self,
        relevance_score: int,
        novelty_score: int,
        tags: list[str],
        keywords: list[str],
        reference_matches: list[ReferenceCase],
    ) -> str:
        if reference_matches and reference_matches[0].reference:
            return self._short_sentence(reference_matches[0].reference)
        signals = " / ".join([*(tags or [])[:2], *(keywords or [])[:2]]) or "内容信号"
        if relevance_score >= 78 and novelty_score >= 72:
            return self._short_sentence(f"围绕 {signals} 做成今日轻量内容提案。")
        if relevance_score >= 70:
            return self._short_sentence(f"结合 {signals} 做低成本内容延展。")
        return "作为背景素材观察，暂不直接转为选题。"

    def _short_sentence(self, text: str, limit: int = 48) -> str:
        clean = re.sub(r"\s+", " ", text or "").strip()
        return clean if len(clean) <= limit else f"{clean[:limit]}..."
