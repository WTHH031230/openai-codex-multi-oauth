# Workflows

## 1) Diagnose wrong-profile selection

1. run the summary script
2. inspect stored preferred profile
3. inspect `order.openai-codex`
4. inspect session `authProfileOverride`
5. determine whether runtime selected the wrong profile or performed expected failover
6. patch only the layer that is inconsistent with the intended semantic

## 2) Diagnose soft-pin failover confusion

1. decide whether the product should show preferred profile or effective profile
2. verify whether runtime failover is allowed for soft pins
3. verify what `/status` currently displays
4. verify what usage currently uses as its auth source
5. align naming and persistence semantics to one explicit model

## 3) Recover from a corrupted auth profile

1. back up the auth store
2. identify the damaged profile entry
3. locate another good entry with the same `accountId`, if available
4. restore only that entry
5. re-run summary and smoke-test the profile

## 4) Diagnose local token-parse failures

Symptoms often include errors like `Failed to extract accountId from token`.

1. inspect whether accountId is already known from profile metadata or headers
2. inspect whether local code parses the JWT too early
3. prefer metadata/header accountId first
4. only fall back to JWT parsing when no other source exists

## 5) Diagnose missing usage

1. check whether usage fetch is tied to generic provider order
2. check whether usage fetch should instead use the effective session profile
3. inspect whether auth errors are filtered and silently hidden
4. verify whether the issue is display semantics or upstream usage semantics

## Rollback rule

Before any runtime patch:
- back up the file you change
- keep the patch minimal
- verify syntax or import validity before restart
- re-test one scenario at a time
