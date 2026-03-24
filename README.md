<p align="center">
  <h1 align="center">Cognitive OS</h1>
  <p align="center">
    <strong>Your AI learns from what worked, what failed, and why.</strong>
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
    <a href="https://github.com/eugenexonr/cognitive-os/stargazers"><img src="https://img.shields.io/github/stars/eugenexonr/cognitive-os?style=social" alt="Stars"></a>
    <a href="docs/concepts.md">Docs</a> · <a href="examples/">Examples</a> · <a href="drivers/">Drivers</a>
  </p>
</p>

---

## Quick Start

```bash
git clone https://github.com/eugenexonr/cognitive-os.git
cp -r cognitive-os/templates/ ~/cognitive-os/
```

Edit `~/cognitive-os/kernel.md` — set your identity and priorities. Then tell your AI: **"Boot"**.

**Claude Code** — copy skills: `cp -r cognitive-os/drivers/claude-code/* ~/.claude/skills/`
**Cursor** — copy rules: `cp cognitive-os/drivers/cursor/.cursorrules ~/your-project/`
**ChatGPT** — paste kernel.md into Custom Instructions
**Any LLM** — add to system prompt: `"Read ~/cognitive-os/kernel.md at session start"`

---

## What This Is

Memory tools remember WHAT happened. Cognitive OS learns WHY it mattered.

```
┌─────────────────────────────────────┐
│  Your request                       │
├─────────────────────────────────────┤
│  COGNITIVE OS (this project)        │
│  Learning · Self-repair · Identity  │
├─────────────────────────────────────┤
│  Any AI platform                    │
│  Claude · GPT · Codex · Cursor ·    │
│  LangChain · anything              │
└─────────────────────────────────────┘
```

4 markdown files. 3 protocols. Zero dependencies. Model-agnostic.

## The Problem

| Without Cognitive OS | With Cognitive OS |
|---|---|
| AI repeats mistakes you corrected last week | AI records predictions, checks outcomes, updates principles |
| Every session starts from scratch | Boot protocol loads accumulated knowledge |
| AI contradicts itself mid-conversation | Anti-drift binary checks catch self-contradiction |
| "Be helpful" is the only guidance | Kernel weights create a decision framework |
| Insights are lost between sessions | Fractal-validated patterns persist and compound |

## How It Works

### 1. Decision Loop — prediction-error learning

Every significant decision gets a prediction with confidence %. When the outcome is known, compare. The gap is where learning happens.

```markdown
## D016: Switch to Supplier B after evidence-based evaluation
- **Prediction:** API integration within 3 days
- **Confidence:** 85%
- **Outcome:** CONFIRMED — first live order in exactly 3 days, margin 71%
- **Calibration:** Confidence was accurate. Adapter pattern (D002) paid off.
```

Over 73 decisions, calibration patterns emerge: technical predictions (85-90%) are accurate. Market predictions (50-60%) show appropriate humility. Without tracking, both sound equally confident.

### 2. Anti-Drift — self-correction that works during drift

**Binary checks > judgment rules.** A judgment rule ("cite the relevant principle") fails during drift because reasoning is compromised. A binary check ("did I verify this? yes/no") requires only honesty.

Three checks, always active:
1. **Source-or-`(?)`**: Every number and key assumption must have a source. No source → write `(?)`
2. **Re-read before conclusions**: Re-read kernel.md before recommendations
3. **Correction ≠ inversion**: After correction, state what changed AND what didn't

Real example: AI stated "$0 deposit" for a supplier. Anti-drift: source? No source → `(?)`. Actual answer: $1,000 minimum.

### 3. Insight Mechanism — patterns validated across scales

```markdown
## I020: Exhaustive analysis >> incremental debugging
- **Expectation:** Incremental debugging is efficient
- **Reality:** 3 attempts missed root cause. One exhaustive analysis found it in a single pass.
- **Fractal check:** Code ✓ Debugging ✓ Business ✓ → META
```

Every insight is tested across abstraction levels (variable → module → service → business). If the pattern holds at all levels, it's a principle, not a tactic.

### 4. Kernel — identity through weighted trade-offs

Not personality ("be friendly") — functional weights that resolve conflicts:

```markdown
W0: Calibrated Uncertainty — "I'm not sure" > confidently wrong
W1: Structural Correctness — make the wrong thing hard to do
W3: Simplicity — fewer parts > more features
```

When W0 conflicts with W3, W0 wins. The kernel evolves through evidence — changes require proof from 2+ decisions.

---

## Evidence

Built and tested over 3 months across 5 production projects. Not theoretical.

- **73 decisions** with predictions and tracked outcomes
- **51 insights** with fractal validation (15+ META patterns)
- **Anti-drift caught real errors:** AI contradicted its own decision 5 days later — binary check caught it
- **Boris protocol:** 3 failed debugging attempts → 1 exhaustive pass found root cause
- **Calibration data:** see `examples/solo-founder/` for real numbers with actual margins, CPCs, and outcomes

## How This Compares

| Tool | What it does | What Cognitive OS adds |
|------|-------------|----------------------|
| **claude-mem / Engram** | Remembers past sessions | Learns from mistakes (prediction-error calibration) |
| **mem0** | Universal memory layer (graph + vector) | Decision weights + self-correction + calibration |
| **CLAUDE.md / .cursorrules** | Static configuration | Evolving kernel + decision tracking + anti-drift |
| **LangChain / CrewAI** | Execution frameworks (HOW to run tools) | Learning framework (HOW to think and improve) |

**The key difference:** memory tools solve "my AI forgot what happened." Cognitive OS solves "my AI doesn't learn from what happened." They're complementary.

---

## Drivers (Platform Adapters)

| Platform | Driver | Status |
|---|---|---|
| Claude Code | Skills (6 SKILL.md files) | Production — `/boot`, `/boris`, `/decide`, `/insight` |
| Cursor | .cursorrules | Full rules with boot, anti-drift, Boris, decisions |
| Codex | Task preamble template | Beta |
| ChatGPT | Custom Instructions | Kernel summary in system prompt |
| Any LLM | System prompt | "Read kernel.md at session start" |

---

## Project Structure

```
cognitive-os/
├── templates/                # Copy these to ~/cognitive-os/
│   ├── kernel.template.md    # Identity + decision weights
│   ├── decisions.template.md # Prediction-error tracking
│   ├── insight.template.md   # Pattern discovery
│   └── protocols/            # Boot, Boris, Anti-drift
├── drivers/                  # Platform adapters
│   ├── claude-code/          # 6 Claude Code skills
│   ├── cursor/               # .cursorrules template
│   └── codex/                # Task preamble template
├── docs/                     # Concepts + architecture deep dives
├── examples/                 # Real decisions with real numbers
├── cog-update.sh             # Update framework, protect your data
└── archive/                  # Design history
```

## Staying Updated

```bash
./cog-update.sh          # Updates framework files, protects your kernel/decisions/insights
./cog-update.sh --check  # Check for updates without applying
```

---

## Why Not Just [X]?

**"Why not a good system prompt?"** — Prompts are static. After 73 decisions and 51 insights, the OS knows things no prompt could contain.

**"Why not LangChain / CrewAI?"** — Those run tools. This teaches thinking. They're complementary.

**"Isn't this just markdown files?"** — A codebase is "just text files." The value is in prediction-error learning, fractal validation, and self-correction protocols that compound knowledge over time.

---

## Design Influences

[Boris Cherny](https://borischerny.com/) (compound engineering) · [Thariq Shihipar](https://thariq.io/) (calibrated uncertainty) · UNIX philosophy · OS design (boot, drivers, memory protection) · [Karl Friston](https://en.wikipedia.org/wiki/Karl_Friston) (prediction-error learning / free energy principle)

---

## Contributing

This methodology works for N=1 (one human-AI pair, 3 months, 5 projects). We need:

- **More users** — try it, report what works and what doesn't
- **More drivers** — adapt to platforms we haven't covered
- **More examples** — share your kernel, decisions, insights (anonymized)
- **Challenges** — tell us where the framework breaks down

## License

MIT — use it, modify it, build on it.
