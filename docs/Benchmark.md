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
- Telemetry is available at `/telemetry` while the backend is running.

## Beta Benchmark

Status: pending real dataset.

Dataset target:

- WeChat: 300
- Xiaohongshu: 300
- Competitors: 30+
- Brands: 30+

| Metric | Current | Notes |
| --- | ---: | --- |
| Import average time | TBD | Real dataset required |
| Analyze average time | TBD | Real provider required |
| Trend average time | TBD | 300+ content required |
| Idea average time | TBD | Trends required |
| Weekly Report average time | TBD | Ideas required |
| Dashboard first load | TBD | Target <2 sec |
| Memory | TBD | Record during benchmark |
| Token | TBD | Real provider required |
| Cost | TBD | Real provider required |
| Success rate | TBD | Real dataset required |
