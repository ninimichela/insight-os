# Pilot Plan

Pilot is the formal validation stage between Beta and RC.

## Status

Planned.

## Principle

Do not enter RC directly after Beta.

Pilot is not a development phase. It is a real operating phase.

Stop product design during Pilot.

Frozen during Pilot:

- New Engine
- New Database
- New Workflow
- New Prompt category
- New Dashboard module
- New API

Allowed during Pilot:

- Bug fixes
- Data import
- AI quality evaluation
- Prompt micro-tuning
- Benchmark updates
- Pilot validation

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

- `docs/Pilot_Log.md`
- `docs/Pilot_Review.md`
- `docs/Beta_Review.md`
- `docs/Benchmark.md`
- `docs/RC_Checklist.md`
- `evaluation/` results

## Final Checklist

Execute in order:

- [ ] Import 300-500 WeChat content records
- [ ] Import 300-500 Xiaohongshu content records
- [ ] Complete Beta Dataset v1
- [ ] Use INSight OS continuously for 2 weeks
- [ ] Maintain `docs/Pilot_Log.md` every day
- [ ] Complete `docs/Benchmark.md`
- [ ] Complete Trend / Idea / Report evaluation
- [ ] Complete `docs/Pilot_Review.md`
- [ ] Decide whether to enter RC based on Pilot Review
