from __future__ import annotations

from typing import Any

from app.services.ai.openai_client import generate_json

from .prompt_loader import load_prompt


def get_idea_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="idea", name="generate")


def generate_idea_copy(project: str, trend, related_contents, priority: int) -> dict[str, Any]:
    payload = {
        "project": project,
        "trend": {
            "topic": trend.topic,
            "category": trend.category,
            "tags": trend.tags,
            "keywords": trend.keywords,
            "trend_score": trend.trend_score,
            "lifecycle": trend.lifecycle,
        },
        "priority": priority,
        "references": [
            {
                "title": content.title,
                "source_name": content.source_name,
                "summary": content.summary,
                "tags": content.tags,
                "keywords": content.keywords,
            }
            for content in related_contents[:5]
        ],
    }
    result = generate_json(get_idea_prompt(), payload)
    if result:
        return {
            "title": result.get("title") or _fallback_title(project, trend),
            "recommendation_reason": result.get("recommendation_reason") or result.get("reason") or _fallback_reason(project, trend),
            "outline": result.get("outline") or _fallback_outline(project, trend),
        }
    return {
        "title": _fallback_title(project, trend),
        "recommendation_reason": _fallback_reason(project, trend),
        "outline": _fallback_outline(project, trend),
    }


def _fallback_title(project: str, trend) -> str:
    if project == "in77":
        return f"{trend.topic} 20分钟城市逃离计划"
    return f"{trend.topic} 今日轻量漫游"


def _fallback_reason(project: str, trend) -> str:
    return f"灵感来自近期 {trend.topic} 相关内容和空间案例的集中出现。"


def _fallback_outline(project: str, trend) -> str:
    return f"执行：用一个日常场景切入 {trend.topic}，组合空间、品牌和可拍摄动线，做成当天可发布的轻内容。"
