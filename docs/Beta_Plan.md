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

Goal: turn Trends into content meeting topics that operators can discuss.

Flow:

```text
Trend Engine
  ↓
Project Filter
  ↓
Idea Generator
  ↓
Idea Score
  ↓
Idea Repository
  ↓
Idea API
  ↓
Dashboard
```

Input:

- Trend
- Competitor
- Project
- Calendar
- Project Rules

Brand Brain is not used in Beta. `packages/config/project_rules.json` provides the temporary project keyword rules.

Output:

```json
{
  "title": "...",
  "recommendation_reason": "...",
  "priority": 92,
  "project": "in77",
  "outline": "...",
  "references": [],
  "source_trends": [],
  "source_contents": []
}
```

Data model:

| Field | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| title | TEXT | Idea title |
| project | TEXT | in77 / in88 |
| trend_id | UUID | Primary Trend reference |
| priority | INT | 0-100 |
| outline | TEXT | Content discussion outline |
| references | UUID[] | Reference Content IDs |
| recommendation_reason | TEXT | Why this idea is recommended |
| execution_cost | ENUM | low / medium / high |
| platforms | TEXT[] | Suggested platforms |
| status | ENUM | draft / review / approved / rejected |
| source_trends | UUID[] | Multiple source Trends, reserved for RC |
| source_contents | UUID[] | Multiple source Contents |
| ai_trace | JSONB | Generation trace |
| created_at | TIMESTAMP | Creation time |

Idea Score:

```text
40% Trend Score
30% Project Fit
20% Reference Count
10% Calendar Fit
```

Rules:

- GPT does not score ideas.
- GPT does not sort ideas.
- GPT does not judge priority.
- Code calculates Project Fit through `packages/config/project_rules.json`.
- GPT only generates title, recommendation reason, and outline.

APIs:

- `POST /ideas/generate`
- `GET /ideas`
- `GET /ideas/{id}`

DoD:

- `POST /ideas/generate` runs.
- `GET /ideas` lists generated ideas.
- `GET /ideas/{id}` returns Trend, Reference, Outline, and Recommendation.
- System automatically generates in77 ×5 and in88 ×5.
- Every idea has a Trend Reference.
- Every idea has an Outline.
- Every idea has a Priority.
- Dashboard displays Today's Ideas.
- Beta Demo validates against at least 300 real content records.

## Beta Sprint 3: Weekly Report

Goal: summarize existing Trends and Ideas into a Markdown weekly report.

Input:

- Past 7 days of Contents
- Generated Trends
- Generated Ideas

Output:

- `# 北京商业内容观察｜Week XX`
- `## 1. 本周热点 TOP10`
- `## 2. 竞品内容观察`
- `## 3. 值得参考案例`
- `## 4. in77 本周建议 ×5`
- `## 5. in88 本周建议 ×5`
- `## 6. 下周执行优先级`
- `## 7. 数据说明`

APIs:

- `POST /reports/generate`
- `GET /reports`
- `GET /reports/{id}`

Formats:

- Markdown

PDF is RC scope.

Rules:

- Report does not recalculate Trend Score.
- Report does not recalculate Idea Priority.
- Trend ranking reads `trends.trend_score`.
- Idea ranking reads `ideas.priority`.
- GPT only turns structured data into readable Markdown.
- The first version exports Markdown only, not PDF or PPT.
- Reports must preserve references through `trend_ids`, `idea_ids`, and `content_ids`.

DoD:

- `POST /reports/generate` creates a Markdown weekly report.
- Report is saved to `reports`.
- `GET /reports` lists historical reports.
- `GET /reports/{id}` returns one report.
- Report contains in77 ×5 and in88 ×5.
- Suggestions can be traced to Idea and Trend IDs.
- Tests pass.

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
