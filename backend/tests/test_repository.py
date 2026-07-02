from app.repositories.content_repository import ContentRepository


def test_content_repository_crud_and_analysis_update(db_session):
    repo = ContentRepository(db_session)
    content = repo.create_content(
        {
            "title": "Repository Test",
            "platform": "wechat",
            "source_name": "北京LOOK",
            "content_source": "article",
            "url": "https://example.com/repository",
            "raw_text": "王府井 室内 漫游",
        }
    )

    assert repo.get_content_by_id(content.id).title == "Repository Test"
    assert repo.get_content_by_url("https://example.com/repository").id == content.id

    updated = repo.update_analysis_result(
        content.id,
        {
            "summary": "摘要",
            "tags": ["Citywalk"],
            "keywords": ["王府井"],
            "content_status": "analyzed",
            "analysis_status": "completed",
        },
    )

    assert updated.summary == "摘要"
    assert updated.content_status == "analyzed"

    items, total = repo.list_contents(q="Repository")
    assert total == 1
    assert items[0].id == content.id

