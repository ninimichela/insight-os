# INSight OS

**AI Content Operating System for Commercial Real Estate**

> INSight OS helps commercial real estate teams make better content decisions, not just generate more content.
>
> INSight OS 的目标不是帮助商业地产团队生成更多内容，而是帮助他们做出更好的内容决策。

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

This repository is at `v0.1` scaffold stage.

## API Documentation

When the backend is running:

- Swagger: `http://127.0.0.1:8000/api/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Release Milestones

- Alpha: Content Library, import, AI analysis ✅
- Beta: Trend, idea, weekly report
- RC: Brand Brain, Decision, Memory, Explainability
- 1.0: Commercial release

Beta plan is frozen in `docs/Beta_Plan.md`.
