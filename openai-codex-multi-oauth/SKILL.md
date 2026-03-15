---
name: openai-codex-multi-oauth
description: Manage and debug multiple OpenAI Codex OAuth profiles inside OpenClaw, including same-email different-account or different-workspace logins, profile allocation, profile selection, soft-pin failover behavior, broken-token recovery, auth profile persistence, and status or usage mismatches. Use when working on openai-codex OAuth internals, Codex profile selection, model overrides targeting a specific openai-codex profile, auth.order behavior, or Codex status and usage cards.
---

# OpenAI Codex Multi OAuth

Support and debug more than one `openai-codex` OAuth login inside OpenClaw.

## Start here

1. Run `python3 scripts/summarize_codex_profiles.py`.
2. Classify the problem before patching anything.
3. Change the smallest wrong layer.
4. Re-test after every change.

Do not change storage, runtime failover, and status semantics in one pass unless the bug clearly spans all three.

## Mental model

Treat these as separate state layers:

- **stored preferred profile** — saved local preference such as `codex_profile_id`
- **auth order** — `order.openai-codex` in the auth store
- **session override** — `authProfileOverride` for the current session
- **effective runtime profile** — the profile that actually succeeded after failover
- **usage source** — the token/accountId used by usage-fetch logic

Do not assume they always match.

## Decision tree

### A. The wrong account is selected

Check in this order:
1. stored preferred profile
2. `order.openai-codex`
3. session `authProfileOverride`
4. whether runtime is performing allowed failover

### B. A profile works sometimes but not always

Check:
1. cooldown / last-good logic
2. token expiry
3. whether the profile is soft-pinned or hard-pinned
4. whether failover is expected behavior or a bug

### C. A token was corrupted during testing

Check:
1. whether the same `accountId` exists in another local auth store
2. whether only one profile entry can be restored surgically
3. whether local token parsing is failing before request dispatch

### D. `/status` and usage do not match real behavior

Check:
1. stored preferred profile
2. auth order
3. session override
4. actual effective runtime profile
5. whether usage is fetched from generic provider order instead of the effective profile

### E. Local request fails before remote auth handling

Check the transport/provider layer first, especially local accountId extraction and request header construction.

## Standard workflows

### 1) Add support for multiple Codex OAuth accounts

- Key profile allocation by `accountId` before email when possible.
- Preserve different workspaces/accounts as separate profiles even when email matches.
- Use stable profile ids such as:
  - `openai-codex:default`
  - `openai-codex:secondary`
  - `openai-codex:tertiary`
  - `openai-codex:account-N`

### 2) Debug soft-pin behavior

Use this semantic model:
- a user-selected profile is preferred first
- if it is unavailable, cooldowned, broken, or rejected, runtime may fail over to another working Codex profile
- status output must be explicit about whether it shows the preferred profile or the effective one

Do not blur “preferred” and “effective” semantics.

### 3) Repair a broken token safely

- Back up the auth store first.
- Restore only the matching profile entry.
- Avoid rewriting unrelated profiles.
- Prefer restoring by matching `accountId`.

### 4) Debug `Failed to extract accountId from token`

Preferred direction:
- use known `chatgpt-account-id` or stored `accountId` first when available
- only parse the JWT when no profile/header account id exists

### 5) Debug `/status` or usage mismatches

Decide which semantic the UI should represent:
- preferred profile
- effective runtime profile
- usage source profile

Then verify every layer against that semantic before patching.

If usage disappears entirely, inspect whether the loader silently filters auth errors such as `No token`, `No auth`, or `Not logged in`.

## Validation checklist

After each change, verify all of these:

1. preferred profile state is what you expect
2. auth order is what you expect
3. current session override is what you expect
4. the runtime actually uses the intended profile
5. `/status` displays the intended semantic
6. usage either matches the intended semantic or is explicitly known to differ

## Bundled resources

- Read `references/runtime-files.md` for the file families that usually matter.
- Read `references/workflows.md` for concrete repair workflows and rollback points.

## Guardrails

- Back up auth files before editing them.
- Prefer surgical patches over broad rewrites.
- Keep version-specific assumptions explicit.
- Do not restart the gateway unless the user asked.
- Commit workspace documentation or skill changes after edits.
