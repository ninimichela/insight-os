from .prompt_loader import load_prompt
from .openai_client import generate_json
from app.core.features import features


def get_summary_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="analysis", name="summarize")


def summarize_content(content) -> dict:
    prompt = get_summary_prompt()
    ai_result = generate_json(
        prompt,
        {"title": content.title, "raw_text": content.raw_text, "platform": content.platform},
    )
    if ai_result and "summary" in ai_result:
        return {
            "summary": ai_result.get("summary"),
            "key_points": ai_result.get("key_points", []),
            "evidence": ai_result.get("evidence", [content.title]),
        }

    if not features.enable_local_analysis:
        raise RuntimeError("Local analysis fallback is disabled")

    text = content.raw_text or content.title
    clean = " ".join(text.split())
    summary = clean[:100]
    if len(clean) > 100:
        summary += "..."
    return {
        "summary": summary,
        "key_points": [content.title],
        "evidence": [content.title, clean[:80]],
    }
