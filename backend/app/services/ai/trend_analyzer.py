from __future__ import annotations

from typing import Any

from app.services.ai.openai_client import generate_json

from .prompt_loader import load_prompt


def get_trend_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="analysis", name="trend")


def generate_trend_insight(trend, contents, top_competitors: list[str]) -> dict[str, Any]:
    payload = {
        "topic": trend.topic,
        "trend_score": trend.trend_score,
        "lifecycle": trend.lifecycle,
        "content_count": trend.content_count,
        "growth_rate": trend.growth_rate,
        "recommended_projects": trend.recommended_projects or [],
        "top_competitors": top_competitors,
        "contents": [
            {
                "title": content.title,
                "source_name": content.source_name,
                "summary": content.summary,
                "tags": content.tags,
                "keywords": content.keywords,
            }
            for content in contents[:10]
        ],
    }
    result = generate_json(get_trend_prompt(), payload)
    if result:
        return {
            "why_hot": result.get("why_hot") or result.get("summary") or _fallback_why_hot(trend),
            "watch_points": result.get("watch_points") or result.get("watch") or _fallback_watch_points(trend),
            "suitable_for": result.get("suitable_for") or trend.recommended_projects or ["in77", "in88"],
        }
    return {
        "why_hot": _fallback_why_hot(trend),
        "watch_points": _fallback_watch_points(trend),
        "suitable_for": trend.recommended_projects or ["in77", "in88"],
    }


def _fallback_why_hot(trend) -> str:
    return (
        f"{trend.topic} 在当前内容库中出现 {trend.content_count} 次，"
        f"增长率为 {trend.growth_rate:.0%}，Trend Score 为 {trend.trend_score}。"
    )


def _fallback_watch_points(trend) -> list[str]:
    return [
        f"观察 {trend.topic} 是否继续进入更多来源。",
        f"关注生命周期从 {trend.lifecycle} 是否进入 Peak 或 Declining。",
        "进入 Idea Engine 前优先核对相关内容的执行成本和品牌契合度。",
    ]
