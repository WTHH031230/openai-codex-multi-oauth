# openai-codex-multi-oauth

[中文说明 / Chinese version](README.zh-CN.md)

OpenClaw skill for managing and debugging multiple OpenAI Codex OAuth profiles.

## What it covers

- multiple `openai-codex` OAuth logins
- same-email but different account/workspace handling
- profile allocation and selection
- auth-order and session-override debugging
- helper / router switch flows
- `/status` and usage mismatch diagnosis
- broken-token recovery

## Supported setups

This repository is intended to stay generic and publishable.

It covers two common patterns:

1. **native auth-store setup**
   - multiple `openai-codex:*` profiles live directly in `auth-profiles.json`
2. **external-router setup**
   - a separate repo of Codex OAuth identities exists, and a helper/router copies one selected profile into an active runtime slot

Use the patterns here as templates, then adapt paths, helper names, and router details to your own deployment.

## Repository layout

- `openai-codex-multi-oauth/` — the actual skill folder
- `openai-codex-multi-oauth/SKILL.md` — main skill instructions
- `openai-codex-multi-oauth/references/` — supporting references
- `openai-codex-multi-oauth/scripts/` — helper scripts

## Quick start

```bash
cd openai-codex-multi-oauth
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

For external-router setups, pass optional path overrides when needed:

```bash
python3 scripts/summarize_codex_profiles.py \
  --repo-path ~/.openclaw/codex-oauth-profiles.json \
  --helper-path ~/.openclaw/codex_profile \
  --router-path /path/to/workspace/scripts/codex_oauth_router.py
```

Replace the session key with the actual value from your own `sessions.json`. Session key shapes vary by channel and deployment.

## Packaging

Package the skill from the skill subdirectory, not from the repo root.

## Notes

Keep machine-specific patches, secrets, and local incident notes out of this repo.
