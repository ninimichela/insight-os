# Contributing to INSight OS

## Product Principle

Every feature must improve a content decision. If it only generates more content but does not improve a decision, it does not belong in INSight OS.

Before adding any feature, ask:

```text
Does this help the user make a better content decision,
or does it only add another AI capability?
```

## Feature Freeze Rule

### No New Engine Before MVP

Before `v1.0`, do not add:

- New Engine
- New Database
- New Workflow
- New Prompt category

Allowed work:

- Improve existing modules
- Fix bugs
- Improve user experience
- Improve accuracy
- Improve speed
- Improve explainability inside existing modules

## Architecture Pattern

Use this flow:

```text
Router
  -> Service
  -> Repository
  -> Database
```

Do not put SQL directly in routers.

## AI Service Pattern

Do not grow one large `ai_service.py`.

Use:

```text
backend/app/services/ai/
├── summarizer.py
├── tagger.py
├── scorer.py
├── classifier.py
├── idea_generator.py
└── report_generator.py
```

## Prompt Versioning

Prompts are code-like product logic. They must stay in Git.

Use:

```text
packages/prompts/v1/
```

Future versions should use:

```text
packages/prompts/v2/
```

Do not store prompts in the database.

## Demo Day Rule

After Sprint 2, do not rush into Sprint 3.

Run a v0.2 Demo Day:

- Import 20 content items.
- Run AI analysis.
- Open dashboard.
- Review Today, Content, Trend, and Idea.

Ask:

- If I were an in77 operator, would I open this every day?
- Is it faster than Notion + ChatGPT?
- If we removed half the features, would it still help users make better content decisions?

