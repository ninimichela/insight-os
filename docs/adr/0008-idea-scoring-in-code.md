# ADR 0008: Keep Idea Scoring in Code

## Status

Accepted

## Context

Beta Sprint 2 introduces Idea Engine. The product needs ideas that can be discussed by a content team, but priority must remain stable and explainable.

## Decision

Idea Engine will use GPT only for:

- Title generation
- Recommendation reason
- Outline

Code owns:

- Project filtering
- Project Fit
- Priority
- Sorting
- Source Trend and Content references

## Consequences

- The same Trend dataset produces stable idea rankings.
- Each idea remains traceable to Trends and reference Contents.
- Brand Brain, Decision Engine, Memory, and Explainability remain RC scope.
