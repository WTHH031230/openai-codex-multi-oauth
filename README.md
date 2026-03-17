# OpenAI Codex Multi OAuth

[中文说明](README.zh-CN.md)

Manage and debug multiple Codex OAuth profiles in OpenClaw.

This repo is for people who run OpenClaw and want Codex profile behavior to stay understandable: which profile a chat is using, why usage looks wrong, whether OpenClaw auto-switched after rate limits, and how to compare profiles safely.

## What this repo helps with

Use this repo if you want to:

- keep multiple Codex accounts or identities in one OpenClaw setup
- understand which profile the current chat is actually using
- debug `/status` when the shown usage does not match your expectation
- compare live usage for different profiles
- understand whether two profiles are truly distinct or only look similar
- debug helper commands such as `/codex_profile` or `/codex_usage`
- understand auto-switch / failover behavior after limits or broken tokens

## What you will see in OpenClaw

Depending on the deployment, you may see some of these user-facing surfaces:

| Surface | What it is for |
| --- | --- |
| `/status` | Check the current chat's model, profile semantics, and usage summary |
| `/codex_profile` | In some setups, inspect or switch the Codex profile for the current chat |
| `/codex_usage` | In some setups, compare live usage across Codex profiles |
| automatic profile rotation / failover | OpenClaw may switch profiles after rate limits, token failures, or cooldown logic |

Important:

- `/status` is a normal OpenClaw surface.
- `/codex_profile` and `/codex_usage` are **common deployment patterns**, not guaranteed built-ins in every install.
- This repo explains both how to use these patterns and how to debug them correctly.

## Typical questions this repo answers

- "Why is this chat suddenly using the wrong Codex account?"
- "Why did `/status` show one thing but usage looked like another profile?"
- "Did OpenClaw auto-switch profiles after a rate limit?"
- "These two profiles look identical — are they actually sharing quota, or did the local code fetch the wrong token?"
- "How should `/codex_profile` or `/codex_usage` be implemented so users see the truth?"

## Quick start

### 1) See what profiles exist

```bash
python3 scripts/summarize_codex_profiles.py
```

### 2) Compare live usage for specific profiles

```bash
python3 scripts/codex_usage_report.py --profile secondary --profile tertiary
```

### 3) Dump machine-readable state

```bash
python3 scripts/summarize_codex_profiles.py --agent main --json
```

## Common workflows

### Check whether the current issue is selection, usage, or display

Start with:

```bash
python3 scripts/summarize_codex_profiles.py
python3 scripts/codex_usage_report.py
```

Use the first script to understand stored state, auth order, and session overrides.
Use the second script to fetch live per-profile usage directly from each credential.

### Debug a wrong profile in `/status`

Look at:

- auth order
- the current chat's `authProfileOverride`
- active-slot routing if your setup uses an external router
- whether usage fetching hard-pins the intended profile or only soft-prefers it

### Debug suspiciously identical usage

Compare:

- `user_id`
- `account_id`
- `email`
- reset times

If `account_id` matches but `user_id` differs, the profiles may belong to the same team workspace while still being separate users.

## Why this repo exists

OpenClaw multi-profile Codex setups usually have several different layers that can drift apart:

- stored preference
- auth order
- per-chat override
- effective runtime profile
- usage source
- display label shown to the user

Most confusing bugs come from mixing those layers together.

This repo is meant to make those differences visible instead of implicit.

## Repository layout

- `openai-codex-multi-oauth/` — the actual skill folder
- `openai-codex-multi-oauth/SKILL.md` — agent-facing skill instructions
- `openai-codex-multi-oauth/references/` — detailed references and workflows
- `openai-codex-multi-oauth/scripts/` — reusable diagnostic scripts

If you are a human operator, start with this README.
If you are wiring the skill into an agent workflow, read `openai-codex-multi-oauth/SKILL.md`.

## Example commands

```bash
# inspect profiles and recent sessions
python3 scripts/summarize_codex_profiles.py

# inspect one exact profile
python3 scripts/codex_usage_report.py --profile tertiary

# compare two profiles directly
python3 scripts/codex_usage_report.py --profile quaternary --profile quinary

# inspect a specific session key
python3 scripts/summarize_codex_profiles.py --session-key 'agent:main:<channel>:<scope>:<id>'
```

For external-router setups, pass optional path overrides when needed:

```bash
python3 scripts/summarize_codex_profiles.py \
  --repo-path ~/.openclaw/codex-oauth-profiles.json \
  --helper-path ~/.openclaw/codex_profile \
  --router-path /path/to/workspace/scripts/codex_oauth_router.py
```

## Notes for adapting to your own setup

- session key formats vary by channel and deployment
- helper command names vary by deployment
- some installs keep all profiles in the native auth store
- some installs keep a separate profile repo and copy one profile into an active runtime slot

Use the patterns here as templates, then adapt them to your own deployment.

## Packaging

Package from the skill subdirectory, not from the repository root.

## Scope

This repo keeps reusable workflows, explanations, and scripts.
Do not put secrets, incident logs, or one-off machine patches here.
