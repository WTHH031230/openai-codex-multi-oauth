# Runtime files and inspection points

These are common defaults for a standard local OpenClaw install. Confirm the target agent id, state directory, and package path before patching.

## State files

- stored preferred Codex profile:
  - `~/.openclaw/codex_profile_id`
- auth profile store for agent `main`:
  - `~/.openclaw/agents/main/agent/auth-profiles.json`
- session registry for agent `main`:
  - `~/.openclaw/agents/main/sessions/sessions.json`
- session transcript for a specific chat:
  - `~/.openclaw/agents/main/sessions/<session-id>.jsonl`

For non-`main` agents, replace `main` in the path.

## Runtime bundles that often matter

- OpenClaw bundled auth/runtime logic:
  - `~/.npm-global/lib/node_modules/openclaw/dist/auth-profiles-*.js`
  - `~/.npm-global/lib/node_modules/openclaw/dist/provider-auth-helpers-*.js`
- Codex provider transport:
  - `~/.npm-global/lib/node_modules/openclaw/node_modules/@mariozechner/pi-ai/dist/providers/openai-codex-responses.js`

Adjust paths if OpenClaw is installed elsewhere.

## What each layer usually controls

### `auth-profiles.json`
- profile records
- `order.openai-codex`
- `usageStats`
- `lastGood`

### `sessions.json`
- per-session model/provider selection
- `authProfileOverride`
- whether the current chat is pinned or auto-overridden to a specific auth profile

### `auth-profiles-*.js`
- auth profile order resolution
- cooldown/failover behavior
- status card rendering
- usage loading

### `openai-codex-responses.js`
- request header construction
- local accountId extraction
- bearer token handling before request dispatch

## Fast inspection checklist

1. inspect stored preferred profile state
2. inspect `order.openai-codex` in the relevant auth store
3. inspect `authProfileOverride` in the relevant session registry
4. inspect whether runtime failover is expected or accidental
5. if usage is wrong or missing, inspect the status-card usage loader path
6. if calls fail before remote auth handling, inspect `openai-codex-responses.js`

## Portability note

This skill documents workflows for investigating multiple Codex OAuth profiles. Exact patch locations can change between OpenClaw versions. Confirm the target version and code path before reusing a patch literally.
