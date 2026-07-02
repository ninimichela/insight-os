def test_content_import_skips_duplicate_url(client):
    payload = {
        "items": [
            {
                "title": "北京夏日室内漫游指南",
                "platform": "wechat",
                "source_name": "北京LOOK",
                "content_source": "article",
                "url": "https://example.com/a",
                "published_at": "2026-07-02T10:00:00",
                "raw_text": "王府井 科技 动漫 高达 室内路线 商场 周末",
            },
            {
                "title": "重复内容",
                "platform": "wechat",
                "source_name": "北京LOOK",
                "content_source": "article",
                "url": "https://example.com/a",
                "published_at": "2026-07-02T10:00:00",
                "raw_text": "重复 URL",
            },
        ]
    }

    response = client.post("/content/import", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["imported"] == 1
    assert data["skipped"] == 1
    assert data["items"][0]["content_status"] == "new"
    assert data["items"][1]["result"] == "skipped"

