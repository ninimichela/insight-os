"""Offline Idea evaluation helper for Pilot.

Expected CSV columns:
idea_id,title,project,entered_discussion,adopted,title_edited,outline_edited,reason_edited,score,notes
"""

from __future__ import annotations

import csv
import sys


def _rate(rows: list[dict[str, str]], key: str) -> float:
    if not rows:
        return 0
    yes_count = sum(1 for row in rows if row.get(key, "").strip().lower() in {"yes", "true", "1"})
    return round(yes_count / len(rows), 4)


def evaluate(path: str) -> dict[str, object]:
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {
        "generated": len(rows),
        "discussion_rate": _rate(rows, "entered_discussion"),
        "adoption_rate": _rate(rows, "adopted"),
        "title_edit_rate": _rate(rows, "title_edited"),
        "outline_edit_rate": _rate(rows, "outline_edited"),
        "reason_edit_rate": _rate(rows, "reason_edited"),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python idea_eval.py idea_scores.csv")
    print(evaluate(sys.argv[1]))
