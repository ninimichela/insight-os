# INSight OS Seed Data

Seed data makes the MVP immediately usable after database setup.

Target flow:

```text
docker compose up
  -> seed database
  -> import sample content
  -> run AI analysis
  -> open dashboard
```

Files:

- `competitors.csv`: commercial projects and media accounts.
- `brands.csv`: first brand/style/reference profiles.
- `calendar.csv`: Beijing commercial and content nodes.
- `holidays.csv`: yearly holidays and content opportunities.
- `topics.csv`: topic taxonomy.
- `projects.csv`: in77 / in88 project config.
- `trend_keywords.csv`: keywords for monitoring and clustering.
- `zz_seed_core.sql`: seeds existing MVP tables from CSV files after `schema.sql` runs.

Current automatic seed scope:

- `competitors.csv` -> `competitors`
- `projects.csv` -> `brand_brains`

Other seed files are available for Sprint 2.2 import/config work without expanding the database schema before Alpha.
