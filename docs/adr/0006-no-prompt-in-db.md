# ADR 0006: Do Not Store Prompts in Database

## Status

Accepted

## Context

Prompts are product logic and need version control, review, rollback, and reproducibility.

## Decision

Store prompts in Git under:

```text
packages/prompts/v1/
packages/prompts/v2/
```

Do not store prompts in the database.

## Consequences

- Prompt changes are reviewable.
- AI outputs can reference prompt versions.
- Operators can update Brand Brain in data/config, but prompt logic remains controlled by Git.

