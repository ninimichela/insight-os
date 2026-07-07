def test_content_analyze_writes_analysis_fields(client):
    imported = client.post(
        "/content/import",
        json={
            "items": [
                {
                    "title": "北京夏日室内漫游指南",
                    "platform": "wechat",
                    "source_name": "北京LOOK",
                    "content_source": "article",
                    "url": "https://example.com/analyze-a",
                    "raw_text": "王府井 科技 动漫 高达 室内路线 商场 周末",
                }
            ]
        },
    ).json()
    content_id = imported["items"][0]["id"]

    response = client.post(
        "/content/analyze",
        json={"content_ids": [content_id], "analysis_version": "gpt55-v1", "force": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["analyzed"] == 1
    item = data["items"][0]
    assert item["summary"]
    assert item["tags"]
    assert item["keywords"]
    assert item["category"]
    assert item["suitable_for"]
    assert item["freshness_score"] > 60
    assert item["relevance_score"] > 70
    assert item["novelty_score"] > 0
    assert item["trend_score"] > 0
    assert item["duplicate_status"] == "unique"
    assert item["insight"]
    assert item["business_opportunity"]
    assert item["analysis_trace"]["provider"] == "mock"
    assert item["analysis_trace"]["fallback"] is True

    listed = client.get("/content", params={"content_status": "analyzed"}).json()
    assert listed["total"] == 1
    assert listed["items"][0]["analysis_status"] == "completed"
    assert listed["items"][0]["business_opportunity"]
