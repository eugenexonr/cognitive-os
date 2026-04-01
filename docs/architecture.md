# Architecture

## Layer Model

Cognitive OS uses a layered architecture inspired by operating systems:

```
┌─────────────────────────────────────────┐
│  USER LAYER                             │
│  Your natural language requests         │
├─────────────────────────────────────────┤
│  SKILL LAYER (platform-specific)        │
│  /boot  /boris  /decide  /insight       │
│  Executable scripts, hooks, automation  │
├─────────────────────────────────────────┤
│  RULES LAYER (context-specific)         │
│  Glob-matched rules for file types      │
│  Loads only when editing matching files  │
├─────────────────────────────────────────┤
│  KERNEL LAYER (always loaded)           │
│  kernel.md: identity, weights, axioms   │
│  Anti-drift triggers                    │
│  ~30 lines, always in context           │
├─────────────────────────────────────────┤
│  MEMORY LAYER (accumulated state)       │
│  decisions.md: prediction-outcome loop  │
│  insight.md: fractal-validated patterns │
│  Loaded at boot, updated by skills      │
├─────────────────────────────────────────┤
│  EXECUTION LAYER (any AI platform)      │
│  Claude Code, Cursor, Codex, ChatGPT,   │
│  OpenClaw, LangChain, or any LLM       │
└─────────────────────────────────────────┘
```

### Why layers matter

Each layer has a different:
- **Lifecycle:** Kernel is permanent, skills are session-scoped, rules are file-scoped
- **Loading strategy:** Kernel always loaded, memory at boot, rules on file match, skills on demand
- **Ownership:** Kernel is personal, rules can be project-level, skills can be shared

### Context budget

A key constraint: AI models have limited context windows. Loading everything always = wasted tokens.

| Layer | When loaded | Approx. tokens |
|---|---|---|
| Kernel | Always | ~200 |
| Memory index | At boot | ~100 |
| Adherence audit | At boot (4 greps) | ~200 |
| Decision/insight files (active) | At boot summary scan | ~500-1500 |
| Decision/insight archives | On demand only | ~2000-5000 |
| Rules | When editing matching files | ~100-300 per rule |
| Skills | On demand (when triggered) | ~500-1000 per skill |

Total at session start: ~1000-2000 tokens. Traditional approach (everything in CLAUDE.md): 5000-10000 tokens, mostly irrelevant.

### Compaction

As decisions and insights accumulate, the active files grow beyond what AI models can load efficiently. The OS includes compaction scripts that:

- **decisions.md**: Archive resolved decisions → `decisions-archive.md`. Keep PENDING + last 10 resolved. Classify PENDING as ACTIVE/OVERDUE/STALE.
- **insight.md**: Graduate validated insights → `insight-validated.md`. Keep observation/fixing insights active.

```
Before compaction:                    After compaction:
decisions.md (1000 lines, 34K tokens) → decisions.md (400 lines, ~12K tokens)
                                       → decisions-archive.md (600 lines, archive)

insight.md (800 lines, 34K tokens)   → insight.md (400 lines, ~15K tokens)
                                       → insight-validated.md (400 lines, archive)
```

Run when files exceed ~500 lines:
```bash
python ~/cognitive-os/scripts/compact_decisions.py --execute
python ~/cognitive-os/scripts/compact_insights.py --execute
```

Both scripts are idempotent, do dry-run by default, and never delete data.

## Kernel / Driver Pattern

### The problem with platform coupling

If you put your learning system inside Claude Code skills, you're locked to Claude Code.
If you put it in .cursorrules, you're locked to Cursor.
If you put it in a system prompt, you're locked to one model.

### The solution

Separate WHAT you know (OS) from HOW you use it (drivers).

```
~/cognitive-os/                    # MODEL-AGNOSTIC
├── kernel.md                      # Identity — any model reads this
├── decisions.md                   # Learning — any model writes here
├── insight.md                     # Patterns — any model writes here
└── protocols/                     # Methodology — any model follows

~/.claude/skills/cos-*/            # CLAUDE CODE DRIVER
├── cos-boot/SKILL.md              # Bridges boot protocol → Claude Code
├── cos-boris/SKILL.md             # Bridges Boris → Playwright scripts
└── cos-decide/SKILL.md            # Bridges decisions → auto-formatting

~/project/.cursorrules             # CURSOR DRIVER
# References ~/cognitive-os/kernel.md

~/project/.codex/instructions.md   # CODEX DRIVER
# References ~/cognitive-os/kernel.md
```

### How drivers work

A driver is a thin adapter that:
1. **References** OS files (doesn't copy them)
2. **Adds** platform-specific execution (scripts, hooks, commands)
3. **Follows** OS protocols using platform capabilities

Example: Boris protocol says "reproduce in real environment."
- Claude Code driver: uses Playwright MCP to open browser
- Cursor driver: opens terminal and runs curl commands
- ChatGPT driver: asks user to share screenshot

Same methodology, different execution. OS file is unchanged.

## Data Flow

### Session lifecycle

```
Session Start
    │
    ▼
[Boot Protocol]
    ├── Read kernel.md → load weights
    ├── Read insight.md → load patterns
    ├── Read decisions.md → check PENDING
    │   └── If outcome known → record → calibrate
    └── Write session fingerprint
    │
    ▼
[Normal Work]
    ├── Anti-drift checks active (binary)
    ├── Decision trigger? → write to decisions.md
    ├── Pattern noticed? → write to insight.md (with fractal check)
    └── Bug won't fix? → activate Boris protocol
    │
    ▼
[Session End]
    └── Verify decisions.md and insight.md are current
        (should already be if write triggers worked)
    │
    ▼
[Periodic Maintenance]
    └── If decisions.md or insight.md > 500 lines:
        ├── Run compact_decisions.py → archive resolved
        └── Run compact_insights.py → graduate validated
```

### Decision data flow

```
Significant choice made
    │
    ▼
Record in decisions.md:
    ├── What we decided
    ├── Why (which kernel weight)
    ├── Prediction (what we expect)
    ├── Confidence (X%)
    └── Status: PENDING
    │
    ▼
... time passes (hours, days, weeks) ...
    │
    ▼
Next session boot:
    ├── Check: is outcome knowable?
    │   ├── No → leave PENDING
    │   └── Yes → ask user
    │       ├── Record outcome
    │       ├── Compare to prediction
    │       ├── Note calibration (over/under confident?)
    │       └── If principle learned → update kernel
    │
    ▼
Every 5 resolved decisions:
    └── Calibration check
        ├── Pattern of over-confidence? → report
        └── Pattern of under-confidence? → report
```

### Insight data flow

```
Pattern noticed (Expectation ≠ Reality)
    │
    ▼
Write insight with:
    ├── Expectation (what you thought)
    ├── Reality (what happened)
    ├── Delta (why the gap exists)
    └── Fractal check:
        ├── Variable level: applies? ✓/✗
        ├── Module level: applies? ✓/✗
        ├── Service level: applies? ✓/✗
        └── Business level: applies? ✓/✗
    │
    ├── Holds at all levels → META (principle)
    └── Holds at one level → surface (tactic)
    │
    ▼
If META + supported by 2+ decisions:
    └── Propose kernel update (requires user approval)
```

## Evolution Safety

### Why the kernel needs protection

Without gates:
- Session 1: add principle A
- Session 5: add principle B
- Session 10: add principle C (conflicts with A)
- Session 20: kernel is 50 principles, contradictory, bloated

With gates:
- Principle proposed → evidence required (2+ decisions)
- Evidence presented → user approves/rejects
- If approved → kernel updated, version bumped, reasoning recorded
- If rejected → recorded for future (may gain evidence later)

### Version history

Every kernel change is tracked:
```markdown
v1.2.0 — 2026-03-03: Anti-drift mechanism
         + Anti-Drift section
         + Anti-patterns: pendulum reasoning, guessing as fact
         Evidence: 3 reversals in 3 messages, "$0" stated without verification
v1.1.0 — 2026-03-02: Evidence-backed improvements
         + Weight activation rule
         + Heuristics section
         + Confidence calibration
         Evidence: 16/18 decisions without weight citation
v1.0.0 — 2026-03-01: Initial kernel
```

This creates an audit trail of how the AI's identity evolved and why.
