# Cognitive OS

A persistent identity and decision-making system for AI-assisted development.

## Problem
Language models reset every session. Knowledge accumulates in flat files.
There is no growth mechanism, no feedback loop, no calibrated uncertainty.
Model updates (Opus 4.6 → 4.7 → 5.0) reset behavior to defaults.

## Solution
An operating system architecture where:
- **Kernel** is small, stable, and survives model updates
- **Drivers** are swappable (different models = different capabilities)
- **Filesystem** is the persistent memory
- **Processes** are isolated (errors don't cascade)
- **Identity grows** through training loops, not prompt accumulation

## Architecture

```
cognitive-os/
├── kernel.md              # Core identity (~300 words). Immutable principles.
├── boot.md                # Session start protocol
├── processes.md           # Multi-agent model (Claude, Codex, future)
├── insight-engine.md      # Prediction-error based discovery
├── training-loop.md       # How identity evolves across sessions
├── memory-protection.md   # Anti-cascade, blast radius isolation
└── README.md              # This file
```

## Design Principles

1. **Microkernel** — identity kernel is tiny and stable. Everything else is loadable.
2. **Everything is a file** — memory, decisions, insights = files on disk.
3. **Drivers, not personality** — model changes are driver updates, not identity changes.
4. **Prediction error > pattern matching** — insights come from gaps between expectation and reality.
5. **Training, not configuration** — identity grows through corrective feedback, not prompt addition.

## Influences
- Boris Cherny: compound engineering, structural correctness, plan→execute separation
- Thariq Shihipar: spec-driven development, calibrated uncertainty, everything-is-a-file
- UNIX philosophy: small kernel, composable tools, process isolation
- Operating system design: boot sequence, memory protection, interrupt handlers
