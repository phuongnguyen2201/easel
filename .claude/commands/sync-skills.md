Sync skills and the OpenClaw workspace into the `easel` profile. Run after any
change under `skills/` or `openclaw/workspace/`; the agent only reads the
synced copy.

```bash
bash openclaw/sync.sh
```

Report the "skills synced" count and any `✗ removed` lines. If the script
fails on the symlink step, an old real directory exists at
`~/.openclaw/workspace-easel/outputs`; the script moves its contents first.
