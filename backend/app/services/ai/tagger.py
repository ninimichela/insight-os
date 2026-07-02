from .prompt_loader import load_prompt
from .openai_client import generate_json


def get_tag_prompt(version: str = "v1") -> str:
    return load_prompt(version=version, module="analysis", name="tag")


THEME_KEYWORDS = {
    "Citywalk": ["citywalk", "漫游", "路线", "一公里"],
    "艺术展": ["艺术", "展览", "展", "画廊"],
    "科技体验": ["科技", "机器人", "AI", "影像", "数码"],
    "动漫IP": ["动漫", "高达", "漫画", "IP", "潮玩"],
    "餐饮探店": ["餐饮", "咖啡", "餐厅", "美食", "甜品"],
    "首店经济": ["首店", "旗舰店", "上新", "新品", "快闪"],
    "亲子家庭": ["亲子", "儿童", "家庭", "遛娃"],
    "夜经济": ["夜", "下班", "晚上", "跨年"],
}


def tag_content(content) -> dict:
    prompt = get_tag_prompt()
    ai_result = generate_json(
        prompt,
        {"title": content.title, "raw_text": content.raw_text, "platform": content.platform},
    )
    if ai_result and "tags" in ai_result:
        return {
            "tags": ai_result.get("tags", []),
            "keywords": ai_result.get("keywords", []),
            "primary_tag": ai_result.get("primary_tag"),
            "evidence": ai_result.get("evidence", [content.title]),
        }

    text = f"{content.title} {content.raw_text or ''}".lower()
    tags = []
    for tag, keywords in THEME_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            tags.append(tag)
    if not tags:
        tags = ["商业内容"]

    keywords = []
    for candidate in ["北京", "王府井", "CBD", "周末", "夏天", "商场", "小红书", "公众号"]:
        if candidate.lower() in text:
            keywords.append(candidate)
    keywords.extend(tags[:3])

    return {
        "tags": list(dict.fromkeys(tags)),
        "keywords": list(dict.fromkeys(keywords)),
        "primary_tag": tags[0],
        "evidence": [content.title],
    }
