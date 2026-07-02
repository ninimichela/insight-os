# INSight OS Architecture

## System Architecture

```text
User
  ↓
Frontend Dashboard
  ↓
FastAPI Backend
  ↓
PostgreSQL
  ↓
AI Service
  ↓
Structured JSON
  ↓
Reports / Ideas / Trends
```

## MVP Architecture

```text
CSV Import
  ↓
Content Library
  ↓
AI Analyzer
  ↓
Trend Engine
  ↓
Idea Engine
  ↓
Weekly Report Generator
```

## V2 Intelligence Architecture

```text
Input
  ↓
Brand Brain
  ↓
Trend Engine
  ↓
Memory Layer
  ↓
Performance Database
  ↓
Decision Engine
  ↓
Explainability Framework
  ↓
Idea / Strategy Engine
```

## Main Components

- `frontend/`: Web dashboard
- `backend/`: FastAPI app
- `database/`: SQL schema and migrations
- `packages/`: Shared config and prompts
- `workflows/`: Automation workflows
- `brand_brain/`: Brand DNA seed files
- `docs/`: Product, architecture, and roadmap documents

