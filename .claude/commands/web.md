Start the web workbench on port 7860 (override with `--port`). Requires a
running gateway.

```bash
easel gateway status || easel gateway start
easel web --port 7860
```

The server binds all interfaces without authentication; only use it on a
trusted network. If the React build is missing, the legacy
`web/static/index.html` is served — run `/frontend-build` first.
