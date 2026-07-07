from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReferenceCase:
    title: str
    category: str
    source: str
    date: str
    summary: str
    why_it_matters: str
    reference: str
    tags: list[str]
    score: int


class ReferenceDataStore:
    """Internal casebook lookup. Not exposed as a user-facing library."""

    def __init__(self, cases: list[ReferenceCase]):
        self.cases = cases

    def find_matches(self, text: str, tags: list[str] | None = None, limit: int = 3) -> list[ReferenceCase]:
        query_terms = self._terms(text)
        query_terms.update(term.lower() for term in tags or [] if term)
        scored: list[tuple[int, ReferenceCase]] = []
        for case in self.cases:
            case_terms = self._terms(" ".join([case.title, case.summary, case.why_it_matters, case.reference, *case.tags]))
            overlap = len(query_terms & case_terms)
            if overlap:
                scored.append((overlap * 10 + case.score, case))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [case for _, case in scored[:limit]]

    def count_matches(self, text: str, tags: list[str] | None = None) -> int:
        return len(self.find_matches(text, tags=tags, limit=100))

    def _terms(self, text: str) -> set[str]:
        value = (text or "").lower()
        words = set(re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]{2,}", value))
        return {word for word in words if len(word) >= 2}


@lru_cache(maxsize=1)
def get_reference_data() -> ReferenceDataStore:
    data_path = Path(__file__).resolve().parents[3] / "packages" / "reference_data" / "casebook_2024_2026.json"
    if not data_path.exists():
        return ReferenceDataStore([])
    raw_cases: list[dict[str, Any]] = json.loads(data_path.read_text(encoding="utf-8"))
    cases = [
        ReferenceCase(
            title=item.get("title", ""),
            category=item.get("category", ""),
            source=item.get("source", ""),
            date=item.get("date", ""),
            summary=item.get("summary", ""),
            why_it_matters=item.get("why_it_matters", ""),
            reference=item.get("reference", ""),
            tags=item.get("tags", []) or [],
            score=int(item.get("score", 0) or 0),
        )
        for item in raw_cases
    ]
    return ReferenceDataStore(cases)
