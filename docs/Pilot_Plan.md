# Pilot Plan

Pilot is the formal validation stage between Beta and RC.

## Status

Planned.

## Principle

Do not enter RC directly after Beta.

Pilot is not a development phase. It is a real operating phase.

## Duration

2 weeks.

## Daily Workflow

```text
09:00
Import yesterday's competitor and market content
  -> Analyze
  -> Generate Trends
  -> Generate Ideas
  -> Generate Weekly Report
  -> Team review / content meeting
```

Rules:

- Do not manually edit database rows during the workflow.
- Do not add product features during Pilot.
- Only fix critical bugs that block the workflow.
- Record human feedback every day.

## Pilot Metrics

### 1. Idea Adoption Rate

Track:

```text
Generated ideas
  -> Entered discussion
  -> Adopted
```

Example:

```text
Generated: 10
Discussed: 6
Adopted: 3
Adoption Rate: 30%
```

This is the most important Pilot metric.

### 2. Human Edit Rate

Track whether operators edited:

- Title
- Outline
- Recommendation reason
- Platform suggestion

This identifies where AI is weakest.

### 3. Time Saved

Track baseline vs INSight OS:

| Task | Before | Pilot |
| --- | ---: | ---: |
| Competitor analysis | 2 hours | TBD |
| Trend summary | 1 hour | TBD |
| Idea planning | 1.5 hours | TBD |
| Weekly report | 2 hours | TBD |

### 4. Trend Accuracy

Operators score Top10 Trends from 1 to 5.

### 5. Weekly Report Usability

Track:

- Can be sent to leadership directly: YES / NO
- Needs light edits: YES / NO
- Needs heavy rewrite: YES / NO

## Pilot Exit Criteria

Pilot is complete only when:

- 2 weeks of real workflow are completed.
- Beta Dataset is used.
- Idea adoption rate is recorded.
- Trend Top10 has human scores.
- Weekly Report usability is recorded.
- Benchmark is updated with real data.
- Critical workflow blockers = 0.

## Pilot Output

At the end of Pilot, update:

- `docs/Beta_Review.md`
- `docs/Benchmark.md`
- `docs/RC_Checklist.md`
- `evaluation/` results
