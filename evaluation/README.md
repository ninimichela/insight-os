# Evaluation

This directory contains offline Pilot evaluation helpers.

Evaluation is not a product engine and is not part of the runtime API.

## Purpose

Use these scripts during Pilot to compare:

- Trend quality
- Idea adoption
- Human edit rate
- Weekly Report usability

## Files

- `trend_eval.py`: summarize human scores for Top10 Trends.
- `idea_eval.py`: summarize discussion, adoption, and edit rates.
- `report_eval.py`: summarize Weekly Report direct-use quality.

## Input Format

Use CSV exports collected during Pilot. Keep raw evaluation files outside production database workflows.
