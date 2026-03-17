# openai-codex-multi-oauth

[中文说明 / Chinese version](README.zh-CN.md)

OpenClaw skill for managing and debugging multiple OpenAI Codex OAuth profiles.

## What a human operator gets

This is meant for people running OpenClaw, not only for people reading source code.

It helps you understand and explain things like:

- which Codex profile the current chat is using
- whether the chat has its own pinned profile override
- whether OpenClaw auto-switched after rate limits
- whether `/status` usage is reading the profile you expected
- why two profiles may look similar even when they should stay distinct

## Common user-facing commands and surfaces

These are common patterns in real deployments. Some are built in, some are local helper commands added by a deployment:

- `/status` — confirm the current chat's model, selected profile semantics, and usage summary
- `/codex_profile` — optional helper command in some setups for viewing or switching the current Codex profile
- `/codex_usage` — optional helper command in some setups for comparing live usage across profiles

Important: `/codex_profile` and `/codex_usage` are not guaranteed built-ins in every OpenClaw install. This skill explains how to debug and implement them correctly.

## What it covers

- multiple `openai-codex` OAuth logins
- same-email but different account/workspace handling
- profile allocation and selection
- auth-order and session-override debugging
- helper / router switch flows
- `/status` and usage mismatch diagnosis
- per-profile live usage inspection
- same-team-workspace but different-user usage debugging
- broken-token recovery

## Supported setups

It mainly covers two common patterns:

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

## Typical usage flows

### 1) I want to see what profiles exist

```bash
python3 scripts/summarize_codex_profiles.py
```

### 2) I want to compare live usage for two profiles

```bash
python3 scripts/codex_usage_report.py --profile secondary --profile tertiary
```

### 3) I see the wrong profile in `/status`

Use this skill to inspect:

- auth order
- session `authProfileOverride`
- active-slot routing
- whether runtime usage is soft-preferred or hard-pinned

### 4) I suspect OpenClaw auto-switched profiles after a limit

Use this skill to distinguish:

- what the user selected
- what the current chat prefers
- what profile the runtime actually used after failover

## Quick start

```bash
cd openai-codex-multi-oauth
python3 scripts/summarize_codex_profiles.py
python3 scripts/summarize_codex_profiles.py --agent main --json
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
python3 scripts/codex_usage_report.py
python3 scripts/codex_usage_report.py --profile secondary --profile tertiary
```

For external-router setups, pass optional path overrides when needed:

```bash
python3 scripts/summarize_codex_profiles.py \
  --repo-path ~/.openclaw/codex-oauth-profiles.json \
  --helper-path ~/.openclaw/codex_profile \
  --router-path /path/to/workspace/scripts/codex_oauth_router.py
```

Replace the session key with the actual value from your own `sessions.json`. Session key shapes vary by channel and deployment.

If two profiles look suspiciously identical, compare `user_id`, `account_id`, and reset times before concluding the backend merged their quotas. Same team workspace does not automatically mean same per-user usage bucket.

## Packaging

Package the skill from the skill subdirectory, not from the repo root.

## Notes

Keep the repo focused on reusable workflows, examples, and diagnostics. Put local incident notes, secrets, and one-off machine patches somewhere else.
