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


def _prepare_dashboard_data(client):
    _import_and_analyze(
        client,
        "CBD Citywalk 夏日路线",
        "北京LOOK",
        "https://example.com/dashboard-citywalk-a",
        "CBD citywalk 城市漫游 夏天 公园 艺术",
    )
    _import_and_analyze(
        client,
        "王府井乐高快闪",
        "THE BOX",
        "https://example.com/dashboard-lego-a",
        "王府井 乐高 LEGO 积木 科技 动漫 高达",
    )
    _import_and_analyze(
        client,
        "北京周末展览和夜生活",
        "Timeout Beijing",
        "https://example.com/dashboard-weekend-a",
        "北京 周末 展览 夜生活 商场 夏天",
    )
    client.post("/trends/generate", json={"lookback_days": 7, "min_content_count": 1})
    client.post("/ideas/generate", json={"projects": ["in77", "in88"], "ideas_per_project": 5})
    client.post("/reports/generate", json={})


def test_dashboard_returns_overview_sections(client):
    _prepare_dashboard_data(client)

    response = client.get("/dashboard")

    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["contents"] == 3
    assert data["stats"]["trends"] > 0
    assert data["stats"]["ideas"] == 10
    assert data["stats"]["reports"] == 1
    assert len(data["top_trends"]) <= 5
    assert len(data["top_ideas"]) == 10
    assert len(data["daily_intelligence"]["todays_signals"]) <= 3
    assert len(data["daily_intelligence"]["todays_opportunities"]) <= 3
    assert len(data["daily_intelligence"]["todays_ideas"]) <= 3
    assert data["daily_intelligence"]["todays_signals"][0]["what"]
    assert data["daily_intelligence"]["todays_signals"][0]["why_now"]
    assert data["daily_intelligence"]["todays_signals"][0]["opportunity"]
    assert data["daily_intelligence"]["todays_signals"][0]["trend_change"]["status"] in [
        "new",
        "rising",
        "declining",
        "unusual",
        "stable",
    ]
    assert data["daily_intelligence"]["todays_opportunities"][0]["why_now"]
    assert data["daily_intelligence"]["todays_ideas"][0]["opportunity"]
    assert data["latest_report"]["markdown_content"]
    assert data["recent_activity"]


def test_dashboard_empty_state(client):
    response = client.get("/dashboard")

    assert response.status_code == 200
    data = response.json()
    assert data["stats"] == {"contents": 0, "trends": 0, "ideas": 0, "reports": 0}
    assert data["top_trends"] == []
    assert data["top_ideas"] == []
    assert data["daily_intelligence"] == {"todays_signals": [], "todays_opportunities": [], "todays_ideas": []}
    assert data["latest_report"] is None
    assert data["recent_activity"] == []


def test_daily_intelligence_feedback_adjusts_scores(client):
    _prepare_dashboard_data(client)
    dashboard = client.get("/dashboard").json()
    item = dashboard["daily_intelligence"]["todays_opportunities"][0]
    before = item["score"]

    response = client.post(
        "/daily-intelligence/feedback",
        json={"item_type": "content", "item_id": item["item_id"], "useful": True},
    )

    assert response.status_code == 200
    assert response.json()["adjustment"] == 5
    next_opportunities = client.get("/dashboard").json()["daily_intelligence"]["todays_opportunities"]
    after = next(row for row in next_opportunities if row["item_id"] == item["item_id"])["score"]
    assert after >= before
