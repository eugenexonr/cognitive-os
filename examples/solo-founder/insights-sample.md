# Insight Log — Sample (Anonymized)

Real insights from 3 months of production AI-assisted development.

---

## I001: Exhaustive analysis >> incremental debugging
- **When:** Month 2 | **Source:** Admin panel bug
- **Expectation:** Incremental debugging (hypothesis → fix → test → repeat) is efficient
- **Reality:** 3 incremental attempts at fixing admin panel, each targeting wrong root cause:
  1. Server-side rendering issue → wrong
  2. Router caching conflict → wrong
  3. Cookie parsing → wrong
  One exhaustive analysis (open real browser, capture console + network + API response) found root cause in ONE pass: API response missing expected field.
- **Delta:** When hypothesis space is uncertain, evidence collection > hypothesis testing. Cost of 3 guesses > cost of 1 exhaustive analysis.
- **Fractal check:**
  - Code: integration test (real env) > unit test (mocked) ✓
  - Debugging: browser repro > curl guess ✓
  - Business: real user feedback > assumed UX ✓
  - → **META**
- **Status:** validated — 3 failures + 1 success = clear evidence

## I002: Binary checks > judgment rules for self-correction
- **When:** Month 2 | **Source:** Anti-drift mechanism design
- **Expectation:** Behavioral rules ("cite weight in every decision") will change model behavior
- **Reality:** Weight citation rule had 0 effect (no weights cited during analysis). The rule requires JUDGMENT (which weight?) — judgment under drift = still drifting. By contrast, `(?)` marker requires only HONESTY (verified? yes/no) — binary check under drift still works.
- **Delta:** Two categories:
  1. Binary checks (verified? → `?` if not) — trivial, reliable
  2. Judgment rules (which weight?) — skippable, unreliable
  Design mechanisms that work WHEN drifting, not only when calibrated.
- **Fractal check:**
  - Code: type system (binary: compiles?) > code review (judgment: is this good?) ✓
  - CI: test pass/fail (binary) > manual QA (judgment) ✓
  - → **META**
- **Status:** validated

## I003: Execution without verification = unbounded cost
- **When:** Month 1 | **Source:** Marketing automation audit
- **Expectation:** Autonomous marketing bot creates campaigns, optimizes, generates leads
- **Reality:** Bot creates campaigns (PAUSED by default), optimizer loop broken, feedback loop dead. Spending hosting + API costs, zero learning.
- **Delta:** Autonomous execution without verification pipeline = open spending tap. System SPENDS but doesn't LEARN. Without learning loop it can't improve — only get more expensive.
- **Fractal check:**
  - Tests without real assertions (mock everything) ✓
  - Policy that checks risk but not results ✓
  - Business spending without revenue tracking ✓
  - → **META**
- **Status:** validated — confirmed across 3 subsystems

## META: Philosophy without measurement = theater
- **Source:** I002 + I003 convergence
- **Pattern:** Tests without assertions + Weights without citations + Social proof without verification = same defect: **declared mechanism without activation/measurement**
- **Root cause:** Creating mechanism FEELS like progress. Measuring it = additional work. Without measurement → mechanism drifts to decoration.
- **Prescription:** For any new mechanism → define activation signal + measurement at creation time.
- **Status:** validated
