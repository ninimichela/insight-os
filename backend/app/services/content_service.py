from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.content_repository import ContentRepository
from app.schemas.content import (
    ContentAnalyzeRequest,
    ContentAnalyzeResponse,
    ContentAnalyzeResultItem,
    ContentImportRequest,
    ContentImportResponse,
    ContentImportResultItem,
)
from app.services.ai.classifier import classify_content
from app.services.ai.scorer import score_content
from app.services.ai.summarizer import summarize_content
from app.services.ai.tagger import tag_content


class ContentService:
    def __init__(self, db: Session):
        self.repository = ContentRepository(db)

    def import_contents(self, request: ContentImportRequest) -> ContentImportResponse:
        imported = 0
        skipped = 0
        results: list[ContentImportResultItem] = []

        for item in request.items:
            if item.url and self.repository.get_content_by_url(item.url):
                skipped += 1
                results.append(
                    ContentImportResultItem(
                        title=item.title,
                        url=item.url,
                        result="skipped",
                        reason="duplicate_url",
                    )
                )
                continue

            content = self.repository.create_content(item.model_dump())
            imported += 1
            results.append(
                ContentImportResultItem(
                    id=content.id,
                    title=content.title,
                    url=content.url,
                    content_status=content.content_status,
                    result="imported",
                )
            )

        return ContentImportResponse(imported=imported, skipped=skipped, items=results)

    def analyze_contents(self, request: ContentAnalyzeRequest) -> ContentAnalyzeResponse:
        analyzed = 0
        failed = 0
        items: list[ContentAnalyzeResultItem] = []
        errors: list[dict] = []

        for content_id in request.content_ids:
            content = self.repository.get_content_by_id(content_id)
            if not content:
                failed += 1
                errors.append({"id": str(content_id), "error": "content_not_found"})
                continue

            if content.content_status == "analyzed" and not request.force:
                failed += 1
                errors.append({"id": str(content_id), "error": "already_analyzed"})
                continue

            try:
                summary = summarize_content(content)
                tags = tag_content(content)
                scores = score_content(content)
                classification = classify_content(content)

                analysis_trace = {
                    "prompt_version": "v1",
                    "brand_brain_version": "1.0",
                    "score_version": "1.0",
                    "workflow_version": "alpha-0.1",
                }
                result = {
                    "summary": summary["summary"],
                    "tags": tags["tags"],
                    "keywords": tags["keywords"],
                    "category": classification["category"],
                    "suitable_for": classification["suitable_for"],
                    "heat_score": scores["heat_score"],
                    "brand_fit_in77": scores["brand_fit_in77"],
                    "brand_fit_in88": scores["brand_fit_in88"],
                    "innovation_score": scores["innovation_score"],
                    "execution_score": scores["execution_score"],
                    "ai_reason": scores["reason"],
                    "evidence": {
                        "summary": summary["evidence"],
                        "tags": tags["evidence"],
                        "scores": scores["evidence"],
                        "classification": classification["evidence"],
                    },
                    "analysis_version": request.analysis_version,
                    "prompt_version": "v1",
                    "brand_brain_version": "1.0",
                    "score_version": "1.0",
                    "workflow_version": "alpha-0.1",
                    "analysis_trace": analysis_trace,
                    "content_status": "analyzed",
                    "analysis_status": "completed",
                }
                updated = self.repository.update_analysis_result(content_id, result)
                analyzed += 1
                items.append(
                    ContentAnalyzeResultItem(
                        id=updated.id,
                        summary=updated.summary,
                        tags=updated.tags or [],
                        keywords=updated.keywords or [],
                        category=updated.category,
                        suitable_for=updated.suitable_for or [],
                        heat_score=updated.heat_score,
                        brand_fit_in77=updated.brand_fit_in77,
                        brand_fit_in88=updated.brand_fit_in88,
                        innovation_score=updated.innovation_score,
                        execution_score=updated.execution_score,
                        analysis_version=updated.analysis_version or request.analysis_version,
                        analysis_trace=updated.analysis_trace or analysis_trace,
                    )
                )
            except Exception as exc:
                failed += 1
                self.repository.update(content_id, {"analysis_status": "failed"})
                errors.append({"id": str(content_id), "error": str(exc)})

        return ContentAnalyzeResponse(analyzed=analyzed, failed=failed, items=items, errors=errors)
