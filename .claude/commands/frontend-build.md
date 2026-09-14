Build the React frontend into `web/frontend/dist`, which `web/app.py` serves
when present.

```bash
cd web/frontend
npm ci --no-audit --no-fund
npm run lint
npm run build
```

`build` runs `tsc -b && vite build`. For live editing use `npm run dev`
(Vite dev server) and point it at the API on port 7860.
