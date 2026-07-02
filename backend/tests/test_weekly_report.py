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


def _prepare_weekly_data(client):
    _import_and_analyze(
        client,
        "CBD Citywalk 夏日路线",
        "北京LOOK",
        "https://example.com/report-citywalk-a",
        "CBD citywalk 城市漫游 夏天 公园 艺术",
    )
    _import_and_analyze(
        client,
        "王府井乐高快闪",
        "THE BOX",
        "https://example.com/report-lego-a",
        "王府井 乐高 LEGO 积木 科技 动漫 高达",
    )
    _import_and_analyze(
        client,
        "北京周末展览和夜生活",
        "Timeout Beijing",
        "https://example.com/report-weekend-a",
        "北京 周末 展览 夜生活 商场 夏天",
    )
    client.post("/trends/generate", json={"lookback_days": 7, "min_content_count": 1})
    client.post("/ideas/generate", json={"projects": ["in77", "in88"], "ideas_per_project": 5})


def test_weekly_report_generate_saves_markdown_and_references(client):
    _prepare_weekly_data(client)

    response = client.post("/reports/generate", json={})

    assert response.status_code == 200
    data = response.json()
    assert data["generated"] == 1
    report = data["item"]
    markdown = report["markdown_content"]
    assert "# 北京商业内容观察｜Week" in markdown
    assert "## 1. 本周热点 TOP10" in markdown
    assert "## 4. in77 本周建议 ×5" in markdown
    assert "## 5. in88 本周建议 ×5" in markdown
    assert "Trend IDs" in markdown
    assert len(report["trend_ids"]) > 0
    assert len(report["idea_ids"]) == 10
    assert len(report["content_ids"]) == 3


def test_weekly_report_list_and_detail(client):
    _prepare_weekly_data(client)
    generated = client.post("/reports/generate", json={}).json()
    report_id = generated["item"]["id"]

    listed = client.get("/reports", params={"page": 1, "page_size": 10})
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    detail = client.get(f"/reports/{report_id}")
    assert detail.status_code == 200
    assert detail.json()["id"] == report_id
    assert detail.json()["status"] == "completed"
