# INSight OS Benchmark

## Alpha Benchmark

Environment:

- Date: 2026-07-02
- Provider: mock
- Database: local SQLite test database
- Dataset: 20 synthetic benchmark content items
- OpenAI token/cost: N/A, because mock provider was used

| Metric | Current |
| --- | ---: |
| Import speed | 866.32 items/sec |
| AI analysis average time | 0.0012 sec/item |
| AI analysis total time | 23.02 ms / 20 items |
| Token | N/A |
| Cost | N/A |
| Success rate | 100% |

## Notes

- Alpha benchmark validates API and local fallback speed, not real LLM latency.
- Beta benchmark must be rerun with real provider, real data, token usage, cost, and 500+ content items.
- Future benchmark rows should record provider, model, prompt version, and analysis trace version.

