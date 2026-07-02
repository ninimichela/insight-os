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
Content
  ↓
Tag Cluster
  ↓
Topic Cluster
  ↓
Trend Score
  ↓
Trend Output
```

Output shape:

```json
{
  "topic": "Citywalk",
  "count": 28,
  "growth_rate": 0.42,
  "trend_score": 91,
  "lifecycle": "Rising",
  "related_contents": []
}
```

APIs:

- `GET /trends`
- `POST /trends/generate`
- `GET /trends/{id}`

Dashboard:

- Today's Trends
- Citywalk
- Night Economy
- Summer
- LEGO
- Exhibition

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

