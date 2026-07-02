# API Changelog

API changes are append-only from RC onward. Do not silently change response shapes.

## beta-v0.9

Status: Beta Feature Complete

### Added

- `POST /content/import`
- `GET /content`
- `POST /content/analyze`
- `GET /trends`
- `GET /trends/{id}`
- `POST /trends/generate`
- `GET /ideas`
- `GET /ideas/{id}`
- `POST /ideas/generate`
- `GET /reports`
- `GET /reports/{id}`
- `POST /reports/generate`
- `GET /dashboard`

### Freeze Rules

- API changes after `beta-v0.9` require a changelog entry.
- Breaking changes require a version note.
- Dashboard remains a read-only aggregation API.
