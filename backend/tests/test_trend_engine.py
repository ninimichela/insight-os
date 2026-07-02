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


def test_trend_generate_clusters_aliases_and_scores(client):
    _import_and_analyze(
        client,
        "CBD Citywalk 夏日路线",
        "北京LOOK",
        "https://example.com/trend-citywalk-a",
        "CBD citywalk 城市漫游 夏天 公园 艺术",
    )
    _import_and_analyze(
        client,
        "城市漫游和公园商业",
        "Timeout Beijing",
        "https://example.com/trend-citywalk-b",
        "city walk 城市 公园 周末 北京商场",
    )
    _import_and_analyze(
        client,
        "王府井乐高快闪",
        "THE BOX",
        "https://example.com/trend-lego",
        "王府井 乐高 LEGO 积木 快闪 动漫",
    )

    response = client.post("/trends/generate", json={"lookback_days": 7, "min_content_count": 1})

    assert response.status_code == 200
    data = response.json()
    assert data["generated"] > 0
    topics = {item["topic"]: item for item in data["items"]}
    assert "Citywalk" in topics
    assert "LEGO" in topics
    assert topics["Citywalk"]["content_count"] >= 2
    assert 0 <= topics["Citywalk"]["trend_score"] <= 100
    assert topics["Citywalk"]["lifecycle"] in ["Emerging", "Rising", "Peak", "Declining"]
    assert topics["Citywalk"]["analysis_trace"]["no_gpt_statistics"] is True


def test_trend_list_and_detail(client):
    _import_and_analyze(
        client,
        "王府井室内动漫漫游",
        "北京SKP",
        "https://example.com/trend-detail",
        "王府井 室内 动漫 高达 漫画 科技",
    )
    generated = client.post("/trends/generate", json={"lookback_days": 7, "min_content_count": 1}).json()
    trend_id = generated["items"][0]["id"]

    listed = client.get("/trends", params={"page": 1, "page_size": 5})
    assert listed.status_code == 200
    assert listed.json()["total"] > 0

    detail = client.get(f"/trends/{trend_id}")
    assert detail.status_code == 200
    data = detail.json()
    assert data["topic"]
    assert data["related_content_items"]
    assert data["top_competitors"]
    assert data["ai_insight"]["why_hot"]
    assert data["ai_insight"]["suitable_for"]
