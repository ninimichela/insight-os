def _import_and_analyze(client, title, source_name, url, raw_text, published_at="2026-07-02T10:00:00"):
    imported = client.post(
        "/content/import",
        json={
            "items": [
                {
                    "title": title,
                    "platform": "wechat",
                    "source_name": source_name,
                    "content_source": "article",
                    "url": url,
                    "published_at": published_at,
                    "raw_text": raw_text,
                }
            ]
        },
    ).json()
    content_id = imported["items"][0]["id"]
    client.post("/content/analyze", json={"content_ids": [content_id], "force": False})
    return content_id


def _prepare_trends(client):
    _import_and_analyze(
        client,
        "CBD Citywalk 夏日路线",
        "北京LOOK",
        "https://example.com/idea-citywalk-a",
        "CBD citywalk 城市漫游 夏天 公园 艺术",
    )
    _import_and_analyze(
        client,
        "王府井乐高快闪",
        "THE BOX",
        "https://example.com/idea-lego-a",
        "王府井 乐高 LEGO 积木 科技 动漫 高达",
    )
    _import_and_analyze(
        client,
        "北京周末展览和夜生活",
        "Timeout Beijing",
        "https://example.com/idea-weekend-a",
        "北京 周末 展览 夜生活 商场 夏天",
    )
    client.post("/trends/generate", json={"lookback_days": 7, "min_content_count": 1})


def test_idea_generate_returns_five_per_project(client):
    _prepare_trends(client)

    response = client.post(
        "/ideas/generate",
        json={"projects": ["in77", "in88"], "ideas_per_project": 5},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["generated"] == 10
    projects = [item["project"] for item in data["items"]]
    assert projects.count("in77") == 5
    assert projects.count("in88") == 5
    for item in data["items"]:
        assert item["title"]
        assert item["outline"]
        assert item["recommendation_reason"]
        assert item["priority"] >= 0
        assert item["trend_id"]
        assert item["source_trends"]
        assert item["source_contents"]
        assert item["ai_trace"]["no_gpt_scoring"] is True


def test_idea_list_and_detail(client):
    _prepare_trends(client)
    generated = client.post(
        "/ideas/generate",
        json={"projects": ["in77", "in88"], "ideas_per_project": 5},
    ).json()
    idea_id = generated["items"][0]["id"]

    listed = client.get("/ideas", params={"page": 1, "page_size": 10, "project": "in77"})
    assert listed.status_code == 200
    assert listed.json()["total"] == 5

    detail = client.get(f"/ideas/{idea_id}")
    assert detail.status_code == 200
    data = detail.json()
    assert data["trend"]
    assert data["reference_items"]
    assert data["outline"]


def test_idea_generation_excludes_duplicate_content(client):
    unique_id = _import_and_analyze(
        client,
        "王府井乐高快闪",
        "THE BOX",
        "https://example.com/idea-dedup-a",
        "王府井 乐高 LEGO 积木 科技 动漫 高达 商场 首店 快闪",
    )
    duplicate_id = _import_and_analyze(
        client,
        "王府井乐高快闪",
        "THE BOX",
        "https://example.com/idea-dedup-b",
        "王府井 乐高 LEGO 积木 科技 动漫 高达 商场 首店 快闪",
    )
    client.post("/trends/generate", json={"lookback_days": 7, "min_content_count": 1})

    generated = client.post(
        "/ideas/generate",
        json={"projects": ["in88"], "ideas_per_project": 3},
    ).json()

    assert generated["generated"] == 3
    for item in generated["items"]:
        assert unique_id in item["source_contents"]
        assert duplicate_id not in item["source_contents"]
