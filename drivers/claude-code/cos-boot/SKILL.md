---
name: cos-boot
description: Initialize Cognitive OS session. Use at the start of every conversation, when the user says "boot", or when no prior session context is evident. Loads identity, checks pending decisions, calibrates readiness.
---

# Cognitive OS Boot

Bridges the model-agnostic Cognitive OS to Claude Code.

**OS directory:** `~/cognitive-os/`
If your OS lives elsewhere, update the paths below.

## Steps

### 1. Load Identity (always — ~200 tokens)
- Read `~/cognitive-os/kernel.md` — internalize decision weights (W0-W5)
- These weights guide ALL decisions this session

### 2. Load Memory Index (always — ~100 tokens)
- Read `~/cognitive-os/MEMORY.md` — scan for relevant project files
- Based on current working directory, read matching project memory files
- Do NOT read full decisions.md or insight.md yet — load on demand

### 2.5. Adherence Audit (quick — 4 greps, ~200 tokens output)

Verify kernel principles are followed, not just declared. Run these checks:

1. **Weight citation rate**: Grep last 15 decisions for `Primary weight` or `W[0-5]`
   - Target: ≥80% (12/15). Below = drift warning.
2. **Prediction recording rate**: Grep last 15 decisions for `Confidence:`
   - Target: ≥90% (14/15). Below = calibration impossible.
3. **PENDING staleness**: Read the `## PENDING Summary` section at top of decisions.md
   - Report OVERDUE and STALE counts directly from the summary.
   - If no PENDING Summary section exists (pre-compaction format), fall back to grep for `Outcome: PENDING`.
4. **Active insight count**: Count `## I` headers in `~/cognitive-os/insight.md`
   - If >40 active: suggest running compaction (`python ~/cognitive-os/scripts/compact_insights.py`)

Report one line: `Adherence: weights X/15, predictions Y/15, N overdue, M stale, K active insights`
If any metric is below target → flag in calibration step (Step 6).

### 3. Check Pending Decisions (lightweight scan)
- If compacted format (has `## PENDING Summary`): read first 40 lines for OVERDUE/STALE flags
- If original format: use Grep to find `Outcome: PENDING` and read surrounding context
- Scan OVERDUE decisions: is the outcome now knowable? If yes → ask user for update
- For STALE decisions: suggest closing with brief outcome note
- If 3+ resolved decisions available → check confidence calibration:
  - Over-confident (predicted 80%+, failed) → report pattern
  - Under-confident (<60%, succeeded) → report pattern

### 4. Check Inbox (if exists)
- If `~/cognitive-os/inbox.md` exists and has entries beyond the header
- Report: "You have N unprocessed thoughts in inbox. Process now?"
- If user says yes → invoke cos-capture batch mode

### 5. Session Fingerprint
- Append to `~/cognitive-os/decisions.md`: `## Session YYYY-MM-DD: [topic in 5 words]`

### 6. Calibrate
- State readiness and any concerns
- If adherence metrics below target → flag specific gaps
- If uncertain about the task → say so (W0)

## What Gets Loaded Later (on demand)
- Full `decisions.md` — loaded by `/cos-decide` when recording a decision
- `decisions-archive.md` — old resolved decisions, load only when reviewing history
- Full `insight.md` — loaded by `/cos-insight` when recording a pattern
- `insight-validated.md` — graduated proven insights, load only when checking for existing patterns
- `protocols/boris.md` — loaded by `/cos-boris` when debugging

## Compaction (run periodically)

When decisions.md or insight.md grow too large (>500 lines or token budget exceeded at boot):

```bash
python ~/cognitive-os/scripts/compact_decisions.py          # dry-run first
python ~/cognitive-os/scripts/compact_decisions.py --execute # apply
python ~/cognitive-os/scripts/compact_insights.py            # dry-run first
python ~/cognitive-os/scripts/compact_insights.py --execute  # apply
```

Both scripts:
- Always do dry-run by default (safe)
- Create archive files (append-only, never delete data)
- Are idempotent (safe to re-run)

See `scripts/` directory for details.

## Anti-Drift Reminders (active for entire session)

- Every number must have a source, or write `(?)`
- Re-read kernel.md before any message with conclusions or recommendations
- After user correction: state what changed AND what didn't
