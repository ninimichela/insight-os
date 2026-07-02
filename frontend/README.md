# INSight OS Frontend

Frontend target stack:

- Next.js
- React
- Tailwind CSS
- shadcn/ui

Sprint 4 will implement:

- Today
- Trends
- Ideas
- Reports

## Alpha Demo

Before the full Next.js dashboard, Alpha includes a static Content Library demo:

```text
frontend/content-library.html
```

Open it after starting the API at `http://localhost:8000`.

## Pilot PWA

The static frontend includes lightweight Pilot-only PWA support:

- `manifest.json`
- `service-worker.js`
- `icons/icon-192.png`
- `icons/icon-512.png`

PWA install works after serving the frontend from HTTPS or localhost. Opening the file directly with `file://` is useful for local preview, but service workers and install prompts require a served origin.
