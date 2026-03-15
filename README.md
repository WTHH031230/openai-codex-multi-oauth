# openai-codex-multi-oauth

[中文说明 / Chinese version](README.zh-CN.md)

OpenClaw skill for managing and debugging multiple OpenAI Codex OAuth profiles.

## What it covers

- multiple `openai-codex` OAuth logins
- same-email but different account/workspace handling
- profile allocation and selection
- soft-pin failover semantics
- broken-token recovery
- auth profile persistence
- `/status` and usage mismatch diagnosis

## Skill layout

- `SKILL.md` — main skill instructions
- `references/runtime-files.md` — file locations and layer map
- `references/workflows.md` — standard workflows and rollback points
- `scripts/summarize_codex_profiles.py` — inspection helper

## Quick start

```bash
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

Replace the session key with the actual value from your `sessions.json`. The format depends on the channel and session type, so do not assume Telegram-specific keys.

## Package

The packaged skill file is generated with the OpenClaw skill packager.

## Notes

This repository is intended to stay generic and publishable. Keep machine-specific patches, secrets, and local incident notes out of the repo.
