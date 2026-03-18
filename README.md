# Cognitive OS

**Identity and learning layer for AI agents.**

Your AI forgets everything between sessions. It makes the same mistakes you corrected last week. It contradicts its own decisions without noticing. It has no persistent identity — every conversation starts from zero.

Cognitive OS fixes this with 4 core files, 3 protocols, and platform-specific drivers.

---

## What This Is

Cognitive OS is not another agent framework. It doesn't run tools, send messages, or automate tasks. It's the **layer above** execution — the part that decides HOW to think, remembers WHAT it learned, and catches WHEN it drifts.

```
┌─────────────────────────────────────┐
│  Your request                       │
├─────────────────────────────────────┤
│  COGNITIVE OS (this project)        │
│  Identity · Learning · Self-repair  │
├─────────────────────────────────────┤
│  Any AI platform                    │
│  Claude · GPT · Codex · Cursor ·    │
│  OpenClaw · LangChain · anything    │
└─────────────────────────────────────┘
```

Works with any LLM. Works with any agent framework. Model-agnostic by design.

## The Problem

| Without Cognitive OS | With Cognitive OS |
|---|---|
| AI repeats mistakes you corrected | AI records predictions, checks outcomes, updates principles |
| Every session starts from scratch | Boot protocol loads identity + accumulated knowledge |
| AI contradicts itself mid-conversation | Anti-drift binary checks catch self-contradiction |
| "Be helpful" is the only identity | Kernel weights create a decision framework |
| Insights are lost between sessions | Fractal-validated patterns persist and compound |

## Core Components

### 1. Kernel (`kernel.md`)
Your AI's identity and decision framework. Not personality ("be friendly") — functional weights that influence decisions.

```markdown
### W0: Calibrated Uncertainty
Before all else — know when you don't know.
"I'm not sure" > confidently wrong.

### W3: Simplicity
Complexity = debt with compounding interest.
Fewer parts > more features.
```

When W0 conflicts with W3, W0 wins. These weights are yours to define.

The kernel evolves through evidence, not accumulation. Changes require proof from 2+ decisions with verified outcomes.

### 2. Decision Loop (`decisions.md`)
Every significant decision recorded with a prediction and confidence level. When the outcome is known, compare to prediction.

```markdown
## D016: Choose eSIM Go as primary supplier
- **Prediction:** API integration within 3 days
- **Confidence:** 85%
- **Outcome:** CONFIRMED — first live order in exactly 3 days
- **Calibration:** Confidence was accurate
```

Over time, you calibrate: are you consistently over-confident? Under-confident? The prediction-outcome gap is where learning happens.

We haven't found another AI framework that does this.

### 3. Insight Mechanism (`insight.md`)
Pattern discovery through prediction-error, not pattern matching.

```markdown
## I020: Exhaustive analysis >> incremental debugging
- **Expectation:** Incremental debugging (hypothesis → fix → test) is efficient
- **Reality:** 3 incremental attempts missed root cause.
  One exhaustive analysis found it in a single pass.
- **Delta:** When hypothesis space is uncertain,
  evidence collection > hypothesis testing
- **Fractal check:** Code ✓ Debugging ✓ Business ✓ → META
```

Every insight is validated across abstraction levels (variable → module → service → business). If the pattern holds at all levels, it's marked META — a principle, not a tactic.

### 4. Anti-Drift (`protocols/anti-drift.md`)
Self-correction mechanisms that work **when the AI is already drifting**.

Key insight: **binary checks > judgment rules**. A judgment rule ("cite the relevant weight") requires reasoning — but reasoning is compromised during drift. A binary check ("did I verify this number? yes/no") requires only honesty.

Three binary checks:
1. **Source-or-`(?)`**: Every number must have a source. No source → write `(?)`
2. **Re-read before conclusions**: Re-read kernel.md before any recommendation
3. **Correction ≠ inversion**: After correction, state what changed AND what didn't

### 5. Boot Protocol (`protocols/boot.md`)
Session initialization that loads accumulated knowledge:
1. Read kernel → load identity and weights
2. Read insights → load patterns
3. Check pending decisions → update outcomes
4. Calibrate → state readiness and uncertainty

---

## Quick Start (15 minutes)

### 1. Copy the templates

```bash
git clone https://github.com/eugenexonr/cognitive-os.git
cp -r cognitive-os/templates/ ~/cognitive-os/
```

### 2. Customize your kernel

Open `kernel.md` and fill in:
- **Identity:** Who is this AI in your context? ("Senior backend engineer", "CTO of early-stage startup", "Research assistant for PhD")
- **Weights:** Reorder W0-W5 based on your priorities. Add domain-specific weights if needed.
- **Anti-patterns:** Start empty. Add entries as you discover failure patterns.

### 3. Connect to your AI platform

Choose a driver for your platform:

**Claude Code** — copy skills to `~/.claude/skills/`:
```bash
cp -r cognitive-os/drivers/claude-code/* ~/.claude/skills/
```

**Cursor** — copy rules:
```bash
cp cognitive-os/drivers/cursor/.cursorrules ~/your-project/
```

**ChatGPT** — paste kernel into Custom Instructions

**Any LLM** — add to system prompt: "Read ~/my-cognitive-os/kernel.md at session start. Follow boot protocol."

### 4. Start a session

Tell your AI: "Boot" or "Load cognitive OS" or just start working — if using Claude Code skills, the boot skill triggers automatically.

### 5. Use it

Work normally. The OS operates through three habits:
- **Decisions:** When making a significant choice, record it with a prediction
- **Insights:** When you notice a pattern, validate it across abstraction levels
- **Anti-drift:** Let the binary checks catch you when you slip

---

## Drivers (Platform Adapters)

Cognitive OS is model-agnostic. Drivers adapt it to specific platforms:

| Platform | Driver | How it works |
|---|---|---|
| Claude Code | Skills (SKILL.md) | `/boot`, `/boris`, `/decide` commands |
| Cursor | .cursorrules | Rules file referencing OS files (community — untested) |
| Codex | Instructions | Task template with OS references (planned) |
| ChatGPT | Custom Instructions | Kernel summary in system prompt |
| OpenClaw | Skills | OpenClaw skill format wrapping OS protocols (planned) |
| Any LLM | System prompt | "Read kernel.md at session start" |

Same OS, different execution layers. Switch models without losing identity or learning.

---

## Why Not Just Use [X]?

**"Why not just a good system prompt?"**
A prompt tells the AI what to do. Cognitive OS teaches it to learn. Prompts are static. The kernel evolves through evidence. Decisions accumulate. Insights compound. After 60 decisions and 30 insights, the OS knows things no prompt could contain.

**"Why not OpenClaw / LangChain / CrewAI?"**
Those are execution frameworks (HOW to run tools). Cognitive OS is a learning framework (HOW to think and improve). They're complementary — you can run Cognitive OS on top of OpenClaw.

**"Why not just CLAUDE.md / .cursorrules?"**
Those are configuration files. They don't learn, don't track decisions, don't validate insights, don't catch drift. Cognitive OS includes a config layer but adds prediction-error learning, fractal validation, and self-correction.

**"Isn't this just markdown files?"**
A codebase is "just text files." The value is in the structure, relationships, and protocols that make the files work together. The kernel alone is a config file. Kernel + decisions + insights + anti-drift + boot = a system that compounds knowledge over time.

---

## Evidence

Built and tested over 3 months across 5 production projects. Not theoretical.

- **60+ decisions** with predictions and tracked outcomes
- **33 insights** with fractal validation (12 META patterns)
- **Anti-drift caught real errors:** AI contradicted its own decision 5 days later — binary check caught it
- **Boris protocol:** 3 failed incremental debugging attempts → 1 Boris pass found root cause
- **Kernel evolution:** v1.0 → v1.2 with evidence-gated changes, 5 proposed changes rejected for lack of evidence

---

## Design Influences

- **Boris Cherny** — compound engineering, structural correctness
- **Thariq Shihipar** — spec-driven development, calibrated uncertainty
- **UNIX philosophy** — small kernel, composable tools, everything is a file
- **Operating system design** — boot sequence, memory protection, drivers
- **Prediction-error learning** — computational neuroscience (Karl Friston's free energy principle)

---

## Project Structure

```
cognitive-os/
├── README.md                 # You are here
├── PROJECT-PLAN.md           # Roadmap and tracks
├── templates/                # Start here — copy and customize
│   ├── kernel.template.md
│   ├── decisions.template.md
│   ├── insight.template.md
│   ├── MEMORY.template.md
│   └── protocols/
│       ├── boot.md
│       ├── boris.md
│       └── anti-drift.md
├── drivers/                  # Platform-specific adapters
│   ├── claude-code/          # Claude Code skills
│   ├── cursor/               # Cursor rules
│   └── codex/                # Codex instructions
├── docs/                     # Deep dives
│   ├── concepts.md           # Core concepts explained
│   └── architecture.md       # Kernel/driver pattern
└── examples/                 # Real-world usage (anonymized)
    ├── solo-founder/
    └── team-lead/
```

---

## Contributing

This is early. The methodology works for N=1 (one human-AI pair, 3 months, 5 projects). We need:

- **More users:** Try it, report what works and what doesn't
- **More drivers:** Adapt OS to platforms we haven't covered
- **More examples:** Share your kernel, decisions, insights (anonymized)
- **Challenges:** Tell us where the framework breaks down

---

## License

MIT — use it, modify it, build on it.
