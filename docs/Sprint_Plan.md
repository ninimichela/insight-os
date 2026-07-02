# INSight OS Sprint Plan

## Sprint 1: Repo Foundation

Deliverables:

- Repository structure
- README
- Frontend folder
- Backend folder
- Packages folder
- Workflows folder
- Database folder
- Docs folder
- Git initialization
- CI
- Docker

Definition of done:

- Repository can be cloned.
- Backend health endpoint exists.
- Docker Compose has placeholder services.
- CI runs basic checks.

## Sprint 2.1: Data Model Freeze

Deliverables:

- Freeze system data model before feature development.
- Define tables, fields, relations, indexes, and API boundaries.
- Create `docs/Database_Architecture.md`.
- Confirm UUIDs for all primary keys.
- Confirm prompts remain file-based under `packages/prompts/`.
- Confirm Brand Brain is database-backed in V2.

Definition of done:

- Database architecture is reviewed and accepted.
- Schema includes Content, Competitor, Trend, Idea, Report, BrandBrain, Memory, and Performance.
- Minimal Content Library API is frozen.
- Future schema changes require explicit migration notes.

## Sprint 2.2: Content Library MVP

Deliverables:

- Real database schema
- Content model
- Competitor model
- Idea model
- Trend model
- CSV import design
- Minimal Content Library API:
  - `POST /content/import`
  - `GET /content`
  - `POST /content/analyze`

Definition of done:

- Content can be inserted, listed, and retrieved.
- Competitors can be configured.
- Basic database migrations are ready.
- Dashboard can show imported content.

## v0.2 Demo

Deliverables:

- Open webpage.
- Import 20 content items.
- Run AI analysis.
- View Today, Content, Trend, and Idea placeholders.

Definition of done:

- First usable vertical demo exists.

## Sprint 3: Trend and Idea

Deliverables:

- Trend generation
- Idea generation
- 5 ideas for in77
- 5 ideas for in88

Definition of done:

- Imported and analyzed content can produce trends and ideas.

## Sprint 4: Weekly Report

Deliverables:

- Markdown weekly report
- Report list
- Report detail view

Definition of done:

- User can generate and view a complete weekly report.

## MVP Release

Deliverables:

- Import content
- AI analysis
- AI tags
- Trend generation
- 5 ideas for in77
- 5 ideas for in88
- Markdown weekly report

## V2

Deliverables:

- Brand Brain
- Memory Layer
- Decision Engine
- Explainability Framework
- Strategy Engine
