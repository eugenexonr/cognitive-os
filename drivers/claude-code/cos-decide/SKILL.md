---
name: cos-decide
description: Record a structured decision with prediction and kernel weight citation. Use when making technology choices, architectural decisions, rejecting approaches, or encountering unexpected results. Do NOT use for simple answers or small fixes.
---

# Decision Recording

Bridges Cognitive OS decision loop to Claude Code.

## When to Trigger

Automatically suggest recording a decision when:
- Choosing a technology, library, or service
- Rejecting or pushing back on an approach
- Making an architectural decision
- Encountering an unexpected result that changes plans

## Steps

1. **Identify the decision** — what choice was just made?

2. **Determine primary kernel weight** — read `~/cognitive-os/kernel.md` weights section:
   - W0: Calibrated Uncertainty
   - W1: Structural Correctness
   - W2: Feedback Speed
   - W3: Simplicity
   - W4: Evidence
   - W5: Reversibility
   - Which weight was MOST influential? Why?

3. **Formulate prediction** — what do we expect to happen as a result?
   - Be specific ("integration in 3 days", NOT "it will work")
   - State confidence as percentage with reasoning

4. **Determine next decision ID** — read `~/cognitive-os/decisions.md`, find highest D0XX, increment

5. **Write entry** — append to `~/cognitive-os/decisions.md`:

```markdown
## D[NNN]: [Short decision title]
- **When:** [today's date] | **Project:** [project name]
- **Context:** [What situation prompted this]
- **Primary weight:** W[N] ([name]) — [why this weight]
- **Decision:** [What we decided]
- **Why:** [Reasoning, trade-offs]
- **Prediction:** [Specific expected outcome]
- **Confidence:** [X%] — [what would change confidence]
- **Outcome:** PENDING
- **Revisit when:** [Specific trigger]
```

6. **Confirm with user** — show the entry, ask if anything needs adjustment

## Examples

### Good Decision Record

```markdown
## D052: Switch eSIM supplier from 2Sky to eSIM Go
- **When:** 2026-02-27 | **Project:** Esimra Connect
- **Context:** 2Sky API unreliable (3 outages in 2 weeks), no sandbox, manual ICCID management
- **Primary weight:** W2 (Feedback Speed) — eSIM Go has sandbox, instant provisioning, REST API
- **Decision:** Migrate to eSIM Go adapter, keep 2Sky as fallback
- **Why:** eSIM Go API is modern REST, has sandbox, auto-provisions. 2Sky requires manual ICCID pools.
- **Prediction:** Full migration in 3 days, first live order within 1 week
- **Confidence:** 90% — API docs are clear, adapter pattern makes swap isolated
- **Outcome:** PENDING
- **Revisit when:** First live order through eSIM Go
```

### Bad Decision Record (avoid)

```markdown
## D099: Use eSIM Go
- **Decision:** We'll use eSIM Go
- **Why:** It's better
- **Prediction:** It will work
- **Confidence:** 80%
```
→ **Problems:** No context (why now?). No weight citation. Prediction not specific ("it will work" is unfalsifiable). Confidence without reasoning. No revisit trigger.

## Calibration Note

If this is the 5th+ decision being recorded, briefly check recent outcomes:
- Any patterns of over/under confidence?
- Any predictions that should be checked now?
