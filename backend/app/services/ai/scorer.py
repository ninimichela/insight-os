from .prompt_loader import load_prompt
from .openai_client import generate_json
from app.core.features import features


def get_score_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="analysis", name="score")


def score_content(content) -> dict:
    prompt = get_score_prompt()
    ai_result = generate_json(
        prompt,
        {"title": content.title, "raw_text": content.raw_text, "platform": content.platform},
    )
    if ai_result and "scores" in ai_result:
        scores = ai_result.get("scores", {})
        return {
            "heat_score": scores.get("heat_score", 0),
            "brand_fit_in77": scores.get("brand_fit_in77", 0),
            "brand_fit_in88": scores.get("brand_fit_in88", 0),
            "innovation_score": scores.get("innovation_score", 0),
            "execution_score": scores.get("execution_score", 0),
            "reason": ai_result.get("reason", ""),
            "evidence": ai_result.get("evidence", [content.title]),
        }

    if not features.enable_local_analysis:
        raise RuntimeError("Local analysis fallback is disabled")

    text = f"{content.title} {content.raw_text or ''}"
    length_bonus = min(len(text) // 100, 20)
    heat_score = min(60 + length_bonus, 95)
    in77_fit = 50
    in88_fit = 50

    if any(word in text for word in ["CBD", "公园", "自然", "艺术", "松弛"]):
        in77_fit += 30
    if any(word in text for word in ["王府井", "科技", "动漫", "高达", "机器人", "室内"]):
        in88_fit += 30

    return {
        "heat_score": min(heat_score, 100),
        "brand_fit_in77": min(in77_fit, 100),
        "brand_fit_in88": min(in88_fit, 100),
        "innovation_score": 75 if any(word in text for word in ["首店", "快闪", "AI", "机器人"]) else 65,
        "execution_score": 82 if any(word in text for word in ["路线", "清单", "指南", "攻略"]) else 70,
        "reason": "基于标题、正文关键词、品牌契合方向和执行难度的 Alpha 规则评分。",
        "evidence": [content.title],
    }
