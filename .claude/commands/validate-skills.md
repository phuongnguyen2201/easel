Validate every SKILL.md and the commands it quotes.

```bash
python scripts/validate_skills.py
python scripts/validate_skill_commands.py
```

Fix each reported error in the named `skills/openclaw/<skill>/SKILL.md`:
frontmatter keys, `description` length 80–300 with a trigger phrase,
`name` == folder, output-dir and publish-safety contracts, and Python
command flags that drift from the script's argparse. Re-run until both exit 0,
then run `/sync-skills`.
