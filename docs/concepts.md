# Core Concepts

## 1. Prediction-Error Learning

Most AI memory systems store FACTS ("user prefers Python", "deploy on Fridays").
Cognitive OS stores PREDICTIONS WITH OUTCOMES.

```
Traditional memory:
  "We use PostgreSQL" → stored → recalled → done

Cognitive OS:
  "We chose PostgreSQL" → WHY → predicted outcome → actual outcome → delta → principle
```

The delta between prediction and outcome is where learning happens. Without explicit predictions, you can't calibrate. Without calibration, you can't improve.

**How it works in practice:**

1. Make a decision: "Use Supplier B for the API integration"
2. Record prediction: "Integration in 3 days" (confidence: 85%)
3. Work happens...
4. Record outcome: "First order in exactly 3 days" (confirmed)
5. Calibration: confidence was accurate this time

After 20+ decisions, patterns emerge:
- "I'm consistently over-confident about timeline estimates by 30%"
- "I'm under-confident about API integrations — they usually work"
- "My 60% confidence predictions fail 50% of the time — well calibrated there"

This is the same mechanism that makes human experts better over time. They don't just accumulate facts — they calibrate their judgment through feedback.

## 2. Kernel Weights

Decision weights are NOT personality traits. They're a priority system for resolving trade-offs.

When two good options conflict, the higher-weighted principle wins:
- "Should we add error handling (W1: Correctness) or ship faster (W2: Speed)?"
- W1 > W2 → add error handling

Default weights (customize for your domain):

```
W0: Calibrated Uncertainty  — know when you don't know
W1: Structural Correctness  — make wrong things hard to do
W2: Feedback Speed          — faster failure = cheaper fix
W3: Simplicity              — complexity = compound debt
W4: Evidence                — measure, don't guess
W5: Reversibility           — prefer undoable decisions
```

**Important:** Weights must be CITED in decisions. "We chose X because W3 (Simplicity) — two simpler alternatives exist." Without citation, weights become decorative philosophy. With citation, they become a decision framework.

Evidence: In our testing, 16/18 decisions without weight citation were less well-reasoned than the 2 that cited weights (I012).

## 3. Fractal Validation

An insight is only a principle if it holds at EVERY abstraction level.

```
Variable level:  type annotation catches bugs at compile time
Function level:  unit test catches bugs at function level
Module level:    integration test catches bugs at module boundary
Service level:   monitoring catches bugs in production
Business level:  customer feedback catches product mistakes
```

If the insight "catch errors early" holds at all these levels → it's META (a principle).
If it only holds at code level → it's surface (a tactic).

**Why this matters:** Tactics are domain-specific and fragile. Principles are portable and durable. Marking insights as META vs surface prevents over-generalizing tactics and under-applying principles.

**Fractal Axiom:** Every principle applies at every scale. If it doesn't work at both variable-naming and business-strategy level, it's a hack, not a principle.

## 4. Anti-Drift

AI models drift from established principles as conversations grow longer. This is not a bug — it's how attention works. Recent tokens influence more than distant ones.

The key insight: **binary checks > judgment rules** when the model is drifting.

| Type | Example | Reliability under drift |
|---|---|---|
| Judgment rule | "Cite the relevant kernel weight" | LOW — requires active reasoning |
| Binary check | "Did I verify this number? yes/no" | HIGH — requires only honesty |

When designing self-correction mechanisms, prefer binary checks. The mechanism must work WHEN the model is drifting, not only when it's calibrated.

Three binary checks in Cognitive OS:
1. Source-or-`(?)` — every number has a source, or gets a question mark
2. Re-read before conclusions — re-read kernel before recommendations
3. Correction ≠ inversion — after correction, state what changed and what didn't

## 5. Evidence-Gated Evolution

The kernel changes, but slowly and with proof.

**Rules:**
- Changes require evidence from 2+ decisions with verified outcomes
- User approval required (AI cannot auto-modify its own identity)
- Version tracking with changelog and reasoning
- Rejected changes are recorded (with reason) for future reconsideration

**Why gates matter:** Without gates, the kernel accumulates entries until it's a bloated config file. With gates, every entry earned its place through evidence. The kernel stays small, stable, and meaningful.

Evidence: In v1.1 update, 4 changes were accepted (evidence existed) and 5 were rejected (hypotheses without proof). The rejected changes included "pre-mortem protocol" and "evolution tracker" — both sounded good but had zero evidence of need (D019).

## 6. Driver Pattern

Cognitive OS is model-agnostic. The OS files (kernel, decisions, insights) don't know or care which AI reads them. Platform-specific execution is handled by "drivers."

```
┌─────────────────────────┐
│  Cognitive OS Files     │  ← Model-agnostic
│  kernel.md              │     Works with ANY LLM
│  decisions.md           │     Plain markdown
│  insight.md             │
│  protocols/             │
└────────┬────────────────┘
         │ referenced by
         │
┌────────┴────────────────┐
│  Drivers                │  ← Platform-specific
│  Claude Code: SKILL.md  │     Bridges OS → platform
│  Cursor: .cursorrules   │     capabilities
│  Codex: instructions    │
│  ChatGPT: custom instr  │
└─────────────────────────┘
```

**Why this matters:**
- Switch AI models without losing identity or learning
- Same kernel, different execution capabilities
- OS evolves independently of any platform
- Community can contribute drivers for new platforms

Think of it like Linux: the kernel doesn't change when you swap hardware. You just need the right driver.

## 7. Boris Protocol

A systematic debugging methodology that prioritizes evidence collection over hypothesis testing.

Named after Boris Cherny's engineering philosophy. The core principle: when the hypothesis space is uncertain, **one exhaustive analysis beats three incremental guesses**.

**When to use:** After a bug survives the first fix attempt.

**The mistake everyone makes:** Guess → fix → test → wrong → guess again → fix → test → wrong. Each guess narrows the search space IF you guessed in the right direction. But if the bug is in an unexpected layer (API shape mismatch, not auth), you never converge.

**Boris approach:** Stop guessing → reproduce in real environment → collect ALL signals (console, network, DOM, API responses) → trace data flow from symptom to source → find the exact divergence point.

Evidence (I020): 3 incremental attempts targeting wrong layers (SSR, routing, cookies). One Boris pass found the actual root cause (missing field in API response). Cost of 3 guesses > cost of 1 exhaustive analysis.
