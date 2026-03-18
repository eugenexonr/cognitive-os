---
name: cos-careful
description: Activate production safety mode. Use when working with production databases, live deployments, or destructive operations. Activate with "careful", "production mode", or "be careful".
---

# Production Safety Mode

Activates safety awareness for working with production systems.

## Limitation

This is a **soft safety layer** (awareness + confirmation prompts), not a hard block.
It relies on Claude following instructions to pause before destructive operations.
A real PreToolUse hook would be stronger — but Claude Code's on-demand hook
registration in skills is not yet fully documented. When it is, upgrade this
to a real hook.

Per Cognitive OS principle I017: binary checks > judgment rules.
This skill is currently a judgment rule. Treat it as a safety net, not a guarantee.

## What This Does

When activated, STOP and ask for explicit user confirmation before ANY of the following:

### Blocked Patterns (require confirmation)

**Database:**
- `DROP TABLE` / `DROP DATABASE`
- `DELETE FROM` without WHERE clause
- `TRUNCATE`
- `ALTER TABLE` on production (can cause locks)
- Any migration on production database

**Git:**
- `git push --force` / `git push -f`
- `git reset --hard`
- `git branch -D` (force delete)
- `git checkout .` (discard all changes)
- Any push to main/master

**Files:**
- `rm -rf` with more than one directory level
- Deleting configuration files (.env, credentials, keys)
- Overwriting files without reading them first

**Infrastructure:**
- `kill -9` on production processes
- Restarting production services
- Modifying CI/CD pipelines
- Changing environment variables on live services

**API:**
- DELETE requests to external production APIs
- Modifying live Stripe/payment configurations
- Sending emails to real users (not test)

## How to Use

Say "careful" or "/cos-careful" at the start of a session where you'll be touching production.

The safety mode stays active for the entire session.

## Deactivation

Say "careful off" or "safety off" to deactivate.
Use only when you're done with production work.

## Note

This is an awareness layer, not a hard block. The goal is to make you
PAUSE and THINK before destructive operations — not to prevent all work.
If a destructive operation is genuinely needed, confirm and proceed.
