# Evaluation Plan

Evaluation is not a product engine.

It is a Pilot and RC support module used to compare AI output quality across prompt, rule, and data changes.

## Evaluation Targets

### Trend Evaluation

Input:

- Top10 Trends
- Human scores from 1 to 5

Output:

- Average trend score
- Low-score topics
- Notes for rule adjustment

### Idea Evaluation

Input:

- Generated ideas
- Human discussion/adoption result
- Human edit flags

Output:

- Discussion rate
- Adoption rate
- Title edit rate
- Outline edit rate
- Recommendation reason edit rate

### Report Evaluation

Input:

- Weekly Report
- Human usability score

Output:

- Direct-use rate
- Light-edit rate
- Heavy-rewrite rate
- Notes for report prompt adjustment

## Success Metric

The success of INSight OS is measured by content adoption, not content generation.

INSight OS 的成功，不是生成了多少内容，而是有多少 AI 建议真正被团队采用。

## Directory

```text
evaluation/
├── README.md
├── trend_eval.py
├── idea_eval.py
└── report_eval.py
```

These tools are offline evaluation helpers. They must not be part of the product runtime.
