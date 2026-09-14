Run the unit test suite (49 tests over CLI/web pure functions, data tracker,
output paths). No gateway or network is needed.

```bash
pytest tests/ -q
```

`pytest.ini` sets `--import-mode=importlib`; tests import `web/app.py` as
`app` and a `paper-explainer` script by path, so run from the project root.
Also run `python skills/shared/scripts/content_guard.py selftest` when
`content_guard.py` changed.
