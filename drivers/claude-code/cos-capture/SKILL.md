---
name: cos-capture
description: Capture raw thoughts, ideas, or observations and route them to the right place in Cognitive OS. Use when the user says "capture", "запиши", "braindump", "мысль", or shares an unstructured thought that needs to be classified and stored. Do NOT use for structured requests like "record decision" or "write insight" — those have dedicated skills.
---

# Cognitive OS Capture Pipeline

Bridges unstructured thinking to structured OS storage.

**Problem this solves:** Ideas arrive unstructured. Without a capture pipeline, they either get lost or clutter the wrong file. This skill classifies first, then routes.

## When to Trigger

- User says "capture", "запиши", "braindump", "мысль", "запомни это"
- User shares a raw thought, observation, or idea without clear structure
- During boot, if `~/cognitive-os/inbox.md` has unprocessed entries

## The Pipeline

### 1. Capture — Write It Down
Append the raw thought to `~/cognitive-os/inbox.md` with timestamp:

```markdown
## [YYYY-MM-DD HH:MM] — Raw capture
[exact user input, unedited]
```

If `inbox.md` doesn't exist, create it with header:
```markdown
# Cognitive OS — Inbox
Unprocessed thoughts. Classify and route, then delete from here.
```

### 2. Classify — What Type Is This?

Read the captured thought and classify:

| Signal | Route to | Via skill |
|--------|----------|-----------|
| Choice between alternatives, tech decision, approach selection | **Decision** | `/cos-decide` |
| Pattern across 2+ contexts, unexpected result, reusable principle | **Insight** | `/cos-insight` |
| Fact about user, preference, project state, external reference | **Memory** | Write to `~/.claude/projects/.../memory/` |
| Action item, task, thing to do | **Task** | State it back to user (OS doesn't manage tasks) |
| Vague/unclear | **Keep in inbox** | Ask user to clarify |

### 3. Route — Send to Destination

- If **decision**: invoke cos-decide flow (ask user to confirm prediction + weight)
- If **insight**: invoke cos-insight flow (ask user to confirm expectation + delta)
- If **memory**: write memory file with proper frontmatter, update MEMORY.md index
- If **task**: tell the user "This sounds like a task: [restate]. Want to act on it now?"
- If **unclear**: keep in inbox, ask "Can you tell me more? Is this a decision, observation, or something to remember?"

### 4. Clean — Remove from Inbox

After successful routing, delete the entry from `inbox.md`.
If inbox is empty after cleanup, leave only the header.

## Batch Mode

When called during boot or explicitly ("process inbox"):
1. Read all entries in `~/cognitive-os/inbox.md`
2. Classify each
3. Present classification to user: "I see 3 items: 1 decision, 1 insight, 1 memory. Process them?"
4. Route each after user confirms
5. Clean processed entries

## Examples

### Good Capture → Route

**User says:** "мысль: каждый раз когда мы используем mock в тестах connect, баг проходит в прод. уже третий раз"

**Classification:** Insight — pattern across 2+ incidents, prediction-error (expected mocks to catch bugs, reality: they don't)

**Action:** Invoke cos-insight with pre-filled:
- Expectation: mocks catch integration bugs
- Reality: 3 bugs passed mocks, failed in prod
- Delta: mock/prod divergence is systematic, not accidental

### Good Capture → Memory

**User says:** "запомни — Railway worker env vars отдельные от API env vars"

**Classification:** Memory (project fact, Connect-specific)

**Action:** Write to memory file, type: project, update MEMORY.md

### Bad Capture (avoid)

**User says:** "fix the login bug"

**This is NOT a capture** — it's a direct instruction. Do not route through inbox. Execute directly.

**User says:** "hmm interesting"

**Too vague.** Ask: "What's interesting? Can you describe the observation?"
