# Decision Log — Sample (Anonymized)

These are real decisions from a solo founder running 5 production projects with AI as CTO.
Numbers are real. Project names anonymized.

---

## D001: Choose Supplier A for MVP
- **When:** Month 1 | **Project:** E-commerce platform
- **Context:** Need API integration for MVP. Limited options evaluated.
- **Primary weight:** W2 (Feedback Speed) — quick integration path
- **Decision:** Go with Supplier A despite limited documentation
- **Prediction:** Sufficient for MVP launch, API stable enough.
- **Confidence:** 60%
- **Outcome:** Partially wrong. Key API field always null, balance only 50 EUR, no webhooks. Works with significant workarounds.
- **Learned principle:** Never rely on single provider without fallback, even for MVP. Always verify API capabilities hands-on before committing.
- **Calibration:** 60% was appropriate — uncertainty was correct.

## D002: Adapter pattern for multi-vendor integration
- **When:** Month 1 | **Project:** B2B platform
- **Context:** Multiple vendors needed. Need clean abstraction.
- **Primary weight:** W1 (Structural Correctness) — swap providers without touching business logic
- **Decision:** Adapter pattern with interface per vendor
- **Prediction:** Will scale to 5+ providers cleanly.
- **Confidence:** 90%
- **Outcome:** Confirmed. 3 adapters work. Mock adapter enables testing. Pattern held through all integrations.
- **Calibration:** 90% was appropriate — well-known pattern, predictable result.

## D003: Switch to Supplier B — evidence-based pivot
- **When:** Month 2 | **Project:** E-commerce platform
- **Context:** Supplier B sent rate sheet with transparent pricing. Evaluated against Supplier A (broken API) and Supplier C (hidden pricing, annual commitment). Analyzed wholesale prices for 25+ countries.
- **Primary weight:** W4 (Evidence) — transparent pricing vs hidden, working webhooks vs none
- **Decision:** Switch to Supplier B. $1,000 initial investment. Start with 4 high-demand markets.
- **Prediction:** Go to market within 3 days of integration start.
- **Confidence:** 85%
- **Margins achieved:**
  - Market A: $1.32 wholesale → $4.49 retail = 70%
  - Market B: $1.34 → $5.99 = 78%
  - Market C: $6.65 → $16.99 = 61%
- **Outcome:** CONFIRMED — first live order in exactly 3 days, margin 71%.
- **Calibration:** 85% was accurate. Adapter pattern (D002) paid off — swap took 1 day.
- **Lesson:** D001 → D003 shows calibration arc: first supplier at 60% (uncertain, partially wrong), second supplier at 85% (evidence-backed, confirmed). Learning happened.

## D004: Boris protocol finds root cause adapter bug missed by 3 fixes
- **When:** Month 2 | **Project:** B2B platform
- **Primary weight:** W4 (Evidence) — traced actual API response vs adapter expectation
- **Context:** Test order showed `provision_failed` despite upstream API returning "completed." Worker marked SUCCESS as FAILURE. Three incremental fix attempts failed.
- **Root cause (Boris protocol):** Response parser checked `data.get("assigned")` expecting an array. Upstream API returns `assigned: true` (boolean). Real data lives in `data["order"][0]["items"][0]`. Parser was structurally wrong, not just conditionally wrong.
- **Fix:** Rewrote parser with real API response shape. 45/45 tests pass.
- **Prediction:** Next integration test will pass without manual intervention.
- **Confidence:** 90%
- **Outcome:** CONFIRMED — 4 countries provisioned cleanly. Two additional root causes found and fixed.
- **Learned:** Multiple failures mask each other. Boris (exhaustive analysis) found 3 issues in 1 pass; incremental debugging found 0 in 3 attempts.

## D005: Paid ads = diagnostic tool, not sales channel
- **When:** Month 2 | **Project:** E-commerce (Marketing)
- **Primary weight:** W0 (Calibrated Uncertainty) + W4 (Evidence)
- **Context:** Average order $8-10. Minimum cost per acquisition: $23. At 2% conversion, 5 clicks/day = 1 purchase per 10 days. $8 revenue on $100 spend. Structurally cash-negative. Industry leaders confirmed performance marketing "failed" early — they grew via influencers.
- **Decision:** Run ads at $10/day as DIAGNOSTIC, not sales channel. Goal: learn CPC, CTR, conversion rate. Run 7 days untouched.
- **Prediction:** 100-200 clicks in 7 days, CPC $1-3, 0-3 purchases. Data value > revenue value.
- **Confidence:** 50% this is best use of $300.
- **Outcome:** CONFIRMED diagnostic value:
  - Clicks: 64 (below 100-200 prediction — over-confident)
  - CPC: $1.06 (better than $1-3 prediction — under-confident)
  - Purchases: 0 (within 0-3 range)
  - Total spend: $67.58
  - Landing page not optimized → 0% conversion confirmed fear
- **Calibration:** 50% confidence was honest — right call. Predictions partially off (clicks over-estimated, CPC under-estimated). Data value was indeed > revenue value.

---

## Calibration Summary (after 5 decisions)

| Decision | Confidence | Outcome | Calibration |
|----------|-----------|---------|-------------|
| D001 | 60% | Partially wrong | Appropriate uncertainty |
| D002 | 90% | Confirmed | Accurate |
| D003 | 85% | Confirmed | Accurate |
| D004 | 90% | Confirmed | Accurate |
| D005 | 50% | Confirmed (diagnostic) | Honest uncertainty |

**Pattern:** High confidence (85-90%) on technical decisions with known patterns = accurate. Low confidence (50-60%) on novel/market decisions = appropriate humility. The prediction-outcome gap teaches WHERE to trust judgment and where to gather more evidence.
