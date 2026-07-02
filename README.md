# INSight OS

**AI Content Operating System for Commercial Real Estate**

> INSight OS helps commercial real estate teams make better content decisions, not just generate more content.
>
> INSight OS 的目标不是帮助商业地产团队生成更多内容，而是帮助他们做出更好的内容决策。
>
> The success of INSight OS is measured by content adoption, not content generation.
>
> INSight OS 的成功，不是生成了多少内容，而是有多少 AI 建议真正被团队采用。

INSight OS is an AI content operating system for commercial real estate teams. It helps teams collect market content, analyze competitors, detect trends, generate content ideas, and produce weekly reports.

## Product Principle

Every feature must improve a content decision. If it only generates more content but does not improve a decision, it does not belong in INSight OS.

## Scope Control

**No New Engine Before MVP.**

Before `v1.0`, do not add new engines, databases, workflows, or prompt categories. Only improve existing modules, fix bugs, improve experience, and improve accuracy.

Initial projects:

- Beijing in77
- Beijing Wangfujing Intime in88

## MVP Goal

```text
Import content
  -> AI analysis
  -> AI tags and scores
  -> trend generation
  -> 5 ideas for in77
  -> 5 ideas for in88
  -> Markdown weekly report
```

## Repository Structure

```text
insight-os/
├── docs/
├── frontend/
├── backend/
├── database/
├── packages/
├── workflows/
├── prompts/
├── brand_brain/
└── tests/
```

## Sprint Plan

- Sprint 1: Repo, CI, Docker, project structure
- Sprint 2.1: Data Model Freeze
- Sprint 2.2: Content Library MVP
- Sprint 3: Trend and Idea
- Sprint 4: Weekly Report
- V2: Brand Brain, Memory, Decision, Explainability, Strategy

## Current Status

This repository is **Beta Feature Complete**.

Implemented Beta chain:

```text
Content Library
  -> Analyze
  -> Trend Engine
  -> Idea Engine
  -> Weekly Report
  -> Dashboard
```

Beta is not yet accepted. The project is at **Beta Gate**:

- Validate real dataset
- Run benchmark
- Complete AI quality review
- Run full Beta Demo
- Complete `docs/Beta_Review.md`

Do not enter RC directly after Beta. The next stage is **Pilot**: two weeks of real daily operation and evaluation.

## API Documentation

When the backend is running:

- Swagger: `http://127.0.0.1:8000/api/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Release Milestones

- Alpha: Content Library, import, AI analysis ✅
- Beta: Trend, idea, weekly report, dashboard ✅ Feature Complete
- Pilot: real operation, real feedback, adoption evaluation
- RC: Brand Brain, Decision, Memory, Explainability
- 1.0: Commercial release

Beta plan is frozen in `docs/Beta_Plan.md`.
Pilot plan is frozen in `docs/Pilot_Plan.md`.

## RC Feature Freeze

Do not enter RC until `docs/RC_Checklist.md` is complete.

RC scope is frozen:

1. Evaluation
2. Brand Brain
3. Decision Engine
4. Memory
5. Explainability

No additional engines, databases, workflows, or prompt categories may be added during RC.

RC sprint order:

1. RC Sprint 1: Evaluation
2. RC Sprint 2: Brand Brain
3. RC Sprint 3: Decision Engine
4. RC Sprint 4: Memory
5. RC Sprint 5: Explainability
6. RC Demo
