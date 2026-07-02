# INSight OS Beta Plan

## Beta Scope Freeze

Beta is fixed. Do not add product capabilities outside this sequence before Beta Demo:

1. Trend Engine
2. Idea Engine
3. Weekly Report
4. Dashboard homepage
5. Beta Demo

Do not build Brand Brain, Decision Engine, Memory, or Explainability during Beta. Those are RC scope.

## Beta Sprint 1: Trend Engine

Goal: turn Content Library into trends, not just a content list.

Flow:

```text
Content Library
  ↓
AI Tags
  ↓
Topic Cluster
  ↓
Trend Score
  ↓
Trend Repository
  ↓
Trend API
  ↓
Dashboard
  ↓
Idea Engine
```

Design constraint:

- GPT must not perform Trend statistics during Beta.
- Clustering is done by code using `tags`, `keywords`, and `category`.
- Sorting is done by API/database order.
- Scoring is done by the fixed Trend Score algorithm.
- Lifecycle is determined by fixed rules.
- GPT is used only for Trend Detail insight: why it matters, what to watch, and whether it fits in77 or in88.

Output shape:

```json
{
  "topic": "Citywalk",
  "content_count": 28,
  "growth_rate": 0.42,
  "trend_score": 91,
  "lifecycle": "Rising",
  "related_contents": [],
  "recommended_projects": ["in77"],
  "recommendation_reason": "..."
}
```

Data model:

| Field | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| topic | TEXT | Trend name |
| category | TEXT | Main category |
| tags | TEXT[] | Cluster tags |
| keywords | TEXT[] | Cluster keywords |
| content_count | INT | Related content count |
| growth_rate | FLOAT | Recent window vs previous window |
| trend_score | INT | 0-100 |
| lifecycle | ENUM | Emerging / Rising / Peak / Declining |
| related_contents | UUID[] | Related Content IDs |
| recommended_projects | TEXT[] | in77 / in88 reserved for Idea Engine |
| recommendation_reason | TEXT | Why the topic fits projects |
| generated_at | TIMESTAMP | Generation time |
| analysis_trace | JSONB | Algorithm evidence |

Trend Score:

```text
40% Content Count
30% Growth Rate
20% Source Diversity
10% Recency
```

Lifecycle rules:

| Lifecycle | Rule |
| --- | --- |
| Emerging | Low count but high growth |
| Rising | Count is growing |
| Peak | High/steady count with slower growth |
| Declining | Count is falling |

Topic Cluster:

- Use `tags + keywords + category`.
- Normalize aliases through `packages/config/topic_alias.json`.
- Example: `乐高`, `积木`, and `LEGO` all become `LEGO`.

APIs:

- `GET /trends`
- `POST /trends/generate`
- `GET /trends/{id}`

No additional Trend endpoints before Beta Demo.

Dashboard:

- Today's Trends
- Citywalk
- Night Economy
- Summer
- LEGO
- Exhibition

Trend Detail shows:

- Topic
- Trend Score
- Lifecycle
- Growth
- Content Count
- Related Contents
- Top Competitors
- AI Insight

DoD:

- `POST /trends/generate` runs.
- System automatically generates trends from analyzed content.
- Trend Score is calculated by code.
- Lifecycle is calculated by rules.
- `GET /trends/{id}` returns detail and AI Insight.
- Dashboard displays Top 5 Trends.
- Beta Demo validates against at least 300 real content records.

## Beta Sprint 2: Idea Engine

Input:

- Trend
- Competitor
- Project
- Calendar

Output:

```json
{
  "title": "...",
  "reason": "...",
  "priority": 92,
  "project": "in77",
  "outline": "...",
  "references": []
}
```

APIs:

- `POST /ideas/generate`
- `GET /ideas`

## Beta Sprint 3: Weekly Report

Input: past 7 days of Contents, Trends, and Ideas.

Output:

- TOP Trends
- Competitors
- Insights
- in77 ×5
- in88 ×5

APIs:

- `POST /reports/generate`
- `GET /reports`

Formats:

- Markdown
- JSON

PDF is RC scope.

## Beta Sprint 4: Dashboard

One real homepage, not a complex dashboard.

Sections:

- Overview
- Today's Trend
- Latest Imported
- Top Ideas
- Weekly Report
- Statistics

## Beta Sprint 5: Beta Demo

Use real data only.

Targets:

- WeChat: 300 items
- Xiaohongshu: 300 items
- Competitors: 30+
- Brands: 30+
- Beijing activity calendar: full year

## Beta KPI

| Area | KPI |
| --- | --- |
| Trend accuracy | >80% |
| Idea manual adoption rate | >80% |
| Weekly report generation time | <30 sec |
| Import success rate | >99% |
| Analyze success rate | >95% |

## Beta Success Criteria

Beta is complete only when:

- At least 500 real content items are imported.
- Trend Engine automatically clusters hot topics.
- System generates 10 weekly ideas automatically: in77 ×5 and in88 ×5.
- System generates `Weekly Report` automatically.
- At least 80% of ideas are manually evaluated as useful references.

After this, move to RC.

## RC Scope

RC is fixed:

1. Brand Brain
2. Memory
3. Decision
4. Explainability
