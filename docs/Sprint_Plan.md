# INSight OS Sprint Plan

## Scope Rule

No New Engine Before MVP.

Before `v1.0`, do not add new engines, databases, workflows, or prompt categories.

Allowed work:

- Improve existing modules
- Fix bugs
- Improve user experience
- Improve accuracy
- Improve speed

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
- Repository Pattern:
  - Router
  - Service
  - Repository
  - Database
- AI Service split:
  - summarizer
  - tagger
  - scorer
  - classifier

Definition of done:

- Content can be inserted, listed, and retrieved.
- Competitors can be configured.
- Basic database migrations are ready.
- Dashboard can show imported content.
- DoD in `docs/Definition_of_Done.md` is satisfied.
- API behavior in `docs/API_SPEC.md` is satisfied.

## v0.2 Demo

Deliverables:

- Open webpage.
- Import 20 content items.
- Run AI analysis.
- View Today, Content, Trend, and Idea placeholders.

Definition of done:

- First usable vertical demo exists.
- The team answers yes to:
  - If I were an in77 operator, would I open this every day?
  - Is it faster than Notion + ChatGPT?
  - If we removed half the features, would it still help users make better content decisions?

## Sprint 2.2 Final Development Order

Do not skip steps:

1. Establish PostgreSQL schema.
2. Complete Repository Layer.
3. Complete `POST /content/import`.
4. Complete `GET /content`.
5. Complete `POST /content/analyze`.
6. Integrate OpenAI.
7. Persist analysis results to database.
8. Display Content Library in Dashboard.
9. Import 20-50 real content items for validation.
10. Complete Alpha Demo.

After this point, do not modify architecture unless there is a critical blocker.

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

## Beta Development Order

Do not change the order:

1. Trend Engine
2. Idea Engine
3. Weekly Report
4. Dashboard homepage
5. Beta Demo

Do not build Brand Brain before Beta. Beta must prove whether real data + Trend + AI can already generate useful ideas.

See `docs/Beta_Plan.md` for the frozen Beta plan.

## Beta Success Criteria

- Import at least 500 real content items.
- Trend Engine automatically clusters hot topics.
- Generate 10 weekly ideas automatically: in77 ×5 and in88 ×5.
- Generate `Weekly Report` automatically.
- At least 80% of ideas are manually evaluated as useful references.
