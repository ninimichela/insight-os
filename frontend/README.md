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

Open it after starting the API at `http://127.0.0.1:8000`.

The API base URL is configurable for mobile testing:

1. Open Notebook.
2. Tap the `...` button.
3. Open API Settings.
4. Paste a backend URL, such as a Cloudflare Tunnel URL.

The frontend reads:

1. `localStorage.getItem("INSIGHT_API_BASE")`
2. `window.INSIGHT_API_BASE`
3. `http://127.0.0.1:8000`

## Pilot PWA

The static frontend includes lightweight Pilot-only PWA support:

- `manifest.json`
- `service-worker.js`
- `icons/icon-192.png`
- `icons/icon-512.png`

PWA install works after serving the frontend from HTTPS or localhost. Opening the file directly with `file://` is useful for local preview, but service workers and install prompts require a served origin.

## Vercel

This folder can be deployed directly as a static Vercel project:

- Root Directory: `frontend`
- Framework Preset: Other / Static
- Main page: `content-library.html`

`vercel.json` rewrites app routes back to `content-library.html` so direct refreshes work.
