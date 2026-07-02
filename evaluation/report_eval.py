"""Offline Weekly Report evaluation helper for Pilot.

Expected CSV columns:
report_id,week,direct_use,light_edit,heavy_rewrite,score,notes
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
        "reports": len(rows),
        "direct_use_rate": _rate(rows, "direct_use"),
        "light_edit_rate": _rate(rows, "light_edit"),
        "heavy_rewrite_rate": _rate(rows, "heavy_rewrite"),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python report_eval.py report_scores.csv")
    print(evaluate(sys.argv[1]))
