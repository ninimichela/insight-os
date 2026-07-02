from .prompt_loader import load_prompt
from .openai_client import generate_json
from app.core.features import features


def get_classifier_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="analysis", name="classify")


def classify_content(content) -> dict:
    prompt = get_classifier_prompt()
    ai_result = generate_json(
        prompt,
        {"title": content.title, "raw_text": content.raw_text, "platform": content.platform},
    )
    if ai_result and "category" in ai_result:
        return {
            "category": ai_result.get("category"),
            "city": ai_result.get("city"),
            "suitable_for": ai_result.get("suitable_for", []),
            "evidence": ai_result.get("evidence", [content.title]),
        }

    if not features.enable_local_analysis:
        raise RuntimeError("Local analysis fallback is disabled")

    text = f"{content.title} {content.raw_text or ''}"
    category = "商业地产"
    if any(word in text for word in ["艺术", "展览", "画廊"]):
        category = "艺术文化"
    elif any(word in text for word in ["咖啡", "餐厅", "美食"]):
        category = "餐饮"
    elif any(word in text for word in ["科技", "机器人", "AI", "数码"]):
        category = "科技"

    suitable_for = []
    if any(word in text for word in ["CBD", "公园", "自然", "松弛", "艺术"]):
        suitable_for.append("in77")
    if any(word in text for word in ["王府井", "科技", "动漫", "高达", "机器人", "室内"]):
        suitable_for.append("in88")
    if not suitable_for:
        suitable_for = ["in77", "in88"]

    return {
        "category": category,
        "city": "北京" if "北京" in text else None,
        "suitable_for": suitable_for,
        "evidence": [content.title],
    }
