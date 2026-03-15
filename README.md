# openai-codex-multi-oauth

[中文说明 / Chinese version](README.zh-CN.md)

OpenClaw skill for managing and debugging multiple OpenAI Codex OAuth profiles.

## Repository layout

- `openai-codex-multi-oauth/` — the actual skill folder
- `openai-codex-multi-oauth/SKILL.md` — main skill instructions
- `openai-codex-multi-oauth/references/` — supporting references
- `openai-codex-multi-oauth/scripts/` — helper scripts

## What it covers

- multiple `openai-codex` OAuth logins
- same-email but different account/workspace handling
- profile allocation and selection
- soft-pin failover semantics
- broken-token recovery
- auth profile persistence
- `/status` and usage mismatch diagnosis

## Quick start

```bash
cd openai-codex-multi-oauth
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

Replace the session key with the actual value from your `sessions.json`. The exact format depends on the channel and session type. **This workflow has only been validated on Telegram sessions so far**; for other channels, treat the example as a placeholder and use the real key structure from the target environment.

## Packaging

Package the skill from the skill subdirectory, not from the repo root.

## Notes

This repository is intended to stay generic and publishable. Keep machine-specific patches, secrets, and local incident notes out of the repo.
