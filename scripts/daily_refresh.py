from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from uuid import UUID


ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.database import SessionLocal  # noqa: E402
from app.models.content import Content  # noqa: E402
from app.schemas.content import ContentAnalyzeRequest, ContentImportRequest  # noqa: E402
from app.schemas.idea import IdeaGenerateRequest  # noqa: E402
from app.schemas.trend import TrendGenerateRequest  # noqa: E402
from app.services.content_service import ContentService  # noqa: E402
from app.services.dashboard_service import DashboardService  # noqa: E402
from app.services.idea_service import IdeaService  # noqa: E402
from app.services.trend_service import TrendService  # noqa: E402


def load_items(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data.get("items", [])
        return data
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            return [{key: value or None for key, value in row.items()} for row in csv.DictReader(file)]
    raise ValueError("Only .json and .csv imports are supported.")


def pending_content_ids(db) -> list[UUID]:
    rows = (
        db.query(Content)
        .filter(Content.analysis_status.in_(["pending", "failed"]))
        .filter(Content.duplicate_status == "unique")
        .all()
    )
    return [UUID(str(row.id)) for row in rows]


def run_daily_refresh(args: argparse.Namespace) -> dict:
    db = SessionLocal()
    try:
        content_service = ContentService(db)
        imported = 0
        skipped = 0

        if args.import_file:
            items = load_items(Path(args.import_file))
            result = content_service.import_contents(ContentImportRequest(items=items))
            imported = result.imported
            skipped = result.skipped

        ids = pending_content_ids(db)
        analyzed = 0
        failed = 0
        if ids:
            result = content_service.analyze_contents(
                ContentAnalyzeRequest(
                    content_ids=ids,
                    analysis_version=args.analysis_version,
                    force=args.force,
                )
            )
            analyzed = result.analyzed
            failed = result.failed

        trend_result = TrendService(db).generate_trends(
            TrendGenerateRequest(
                lookback_days=args.lookback_days,
                min_content_count=args.min_content_count,
            )
        )

        idea_count = 0
        if not args.skip_ideas:
            idea_result = IdeaService(db).generate_ideas(
                IdeaGenerateRequest(projects=args.projects, ideas_per_project=args.ideas_per_project)
            )
            idea_count = idea_result.generated
        daily_intelligence = DashboardService(db).get_dashboard().daily_intelligence

        return {
            "imported": imported,
            "skipped": skipped,
            "analyzed": analyzed,
            "failed": failed,
            "trends": trend_result.generated,
            "ideas": idea_count,
            "daily_intelligence": daily_intelligence.model_dump(mode="json"),
        }
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run INSight OS daily content intelligence refresh.")
    parser.add_argument("--import-file", help="Optional JSON or CSV file containing content import items.")
    parser.add_argument("--analysis-version", default="intelligence-v1")
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--min-content-count", type=int, default=1)
    parser.add_argument("--projects", nargs="+", default=["in77", "in88"])
    parser.add_argument("--ideas-per-project", type=int, default=5)
    parser.add_argument("--skip-ideas", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    print(json.dumps(run_daily_refresh(parse_args()), ensure_ascii=False, indent=2))
