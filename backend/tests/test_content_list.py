def test_content_list_supports_search_filter_and_pagination(client):
    client.post(
        "/content/import",
        json={
            "items": [
                {
                    "title": "北京夏日室内漫游指南",
                    "platform": "wechat",
                    "source_name": "北京LOOK",
                    "content_source": "article",
                    "url": "https://example.com/list-a",
                    "raw_text": "王府井 室内 漫游",
                },
                {
                    "title": "CBD午间放空路线",
                    "platform": "xiaohongshu",
                    "source_name": "小红书",
                    "content_source": "post",
                    "url": "https://example.com/list-b",
                    "raw_text": "CBD 公园 松弛",
                },
            ]
        },
    )

    response = client.get("/content", params={"q": "王府井", "platform": "wechat", "page": 1, "page_size": 10})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "北京夏日室内漫游指南"

