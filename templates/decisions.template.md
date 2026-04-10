# Decision Log

Format: Decision → Context → Why → Prediction → Confidence → Outcome

<!-- WRITE TRIGGER: Record a decision IMMEDIATELY after:
     - Choosing a technology or tool
     - Rejecting or pushing back on an approach
     - Making an architectural decision
     - Encountering an unexpected result

     DO NOT WRITE for: simple answers, small fixes, informational questions.

     WHY THIS FORMAT:
     Most teams record WHAT they decided. This format records WHAT + WHY +
     PREDICTED OUTCOME + ACTUAL OUTCOME. The prediction-outcome gap is where
     learning happens. Without predictions, you can't calibrate. -->

---

## Session YYYY-MM-DD: [topic in 5 words]

## D001: [Short decision title]
<!--fm
id: D001
status: pending
project: [project name]
weight: W[N]
confidence: [X]
created: YYYY-MM-DD
depends_on: []
fm-->
- **When:** YYYY-MM-DD | **Project:** [project name]
- **Context:** [What situation prompted this decision]
- **Primary weight:** W[N] ([weight name]) — [why this weight was primary]
- **Decision:** [What we decided to do]
- **Why:** [Reasoning, trade-offs considered]
- **Prediction:** [What we expect to happen as a result]
- **Confidence:** [X%] — [what would change our confidence]
- **Outcome:** PENDING
- **Revisit when:** [Specific trigger for checking outcome]

<!-- OUTCOME UPDATE FORMAT (fill in when outcome is known):
- **Outcome:** [What actually happened]
- **Learned principle:** [What this teaches us, if anything]
- **Calibration:** [Was confidence accurate? Over/under-confident?]
-->

<!-- CALIBRATION CHECK (run at session boot):
     Look at last 5 resolved decisions.
     Over-confident (predicted 80%+, failed) = need more humility
     Under-confident (predicted <60%, succeeded) = trust judgment more
     If 3+ show same pattern → report to user -->

<!-- COMPACTION: When this file exceeds ~500 lines, run:
     python ~/cognitive-os/scripts/compact_decisions.py --execute
     This archives resolved decisions and classifies PENDING as ACTIVE/OVERDUE/STALE.
     Archive file: decisions-archive.md (append-only, never loses data). -->
