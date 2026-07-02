"""Offline Trend evaluation helper for Pilot.

Expected CSV columns:
trend_id,topic,human_score,notes
"""

from __future__ import annotations

import csv
import sys
from statistics import mean


def evaluate(path: str) -> dict[str, object]:
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    scores = [float(row["human_score"]) for row in rows if row.get("human_score")]
    low_score_topics = [
        {"trend_id": row.get("trend_id"), "topic": row.get("topic"), "score": row.get("human_score")}
        for row in rows
        if row.get("human_score") and float(row["human_score"]) < 4
    ]
    return {
        "total": len(rows),
        "average_score": round(mean(scores), 2) if scores else 0,
        "low_score_topics": low_score_topics,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python trend_eval.py trend_scores.csv")
    print(evaluate(sys.argv[1]))
