# Decision Log — Sample (Anonymized)

These are real decisions from a solo founder running 5 production projects with AI as CTO.

---

## D001: Choose Supplier A for MVP
- **When:** Month 1 | **Project:** E-commerce platform
- **Context:** Need API integration for MVP. Limited options evaluated.
- **Primary weight:** W2 (Feedback Speed) — quick integration path
- **Decision:** Go with Supplier A despite limited documentation
- **Prediction:** Sufficient for MVP launch, API stable enough.
- **Confidence:** 60%
- **Outcome:** Partially wrong. Key API field always null, balance limited, no webhooks. Works with significant workarounds.
- **Learned principle:** Never rely on single provider without fallback, even for MVP. Always verify API capabilities hands-on before committing.

## D002: Adapter pattern for multi-vendor integration
- **When:** Month 1 | **Project:** B2B platform
- **Context:** Multiple vendors needed. Need clean abstraction.
- **Primary weight:** W1 (Structural Correctness) — swap providers without touching business logic
- **Decision:** Adapter pattern with interface per vendor
- **Prediction:** Will scale to 5+ providers cleanly.
- **Confidence:** 90%
- **Outcome:** Confirmed. 3 adapters work. Mock adapter enables testing. Pattern held through all integrations.
- **Learned principle:** Adapter pattern is a reliable primitive for multi-vendor. Transferable to other domains.
- **Calibration:** 90% confidence was appropriate — this is a well-known pattern.

## D003: Modular monolith over microservices
- **When:** Month 1 | **Project:** B2B platform
- **Primary weight:** W3 (Simplicity) — team of 1 + AI, microservices premature
- **Decision:** Monolith with clear module boundaries + row-level security for tenants
- **Prediction:** Will hold through MVP and early scaling.
- **Confidence:** 85%
- **Outcome:** Holding well. 800+ tests, 90% coverage. RLS provides tenant isolation without service boundaries.
- **Calibration:** Confidence accurate.

## D004: Kill failed marketing channel, pivot to revenue
- **When:** Month 2 | **Project:** Cross-project
- **Context:** Marketing automation: 0 clicks, 17 impressions, $0. Meanwhile product has real orders.
- **Primary weight:** W4 (Evidence) — 17 impressions, 0 clicks = definitive failure
- **Decision:** Kill marketing bot, focus all energy on product revenue
- **Prediction:** With focused effort on acquisition, first consistent revenue within 60 days.
- **Confidence:** 55%
- **Outcome:** PENDING
- **Calibration note:** Low confidence appropriate — product works but acquisition unproven.

## D005: Evidence-gated kernel evolution
- **When:** Month 2 | **Project:** Cognitive OS
- **Context:** Self-reflection revealed 16/18 decisions don't cite weights.
- **Primary weight:** W4 (Evidence) — only changes backed by decision data accepted
- **Decision:** 4 changes accepted (evidence exists), 5 rejected (hypotheses without proof)
- **Prediction:** Weight citation will improve decision quality within 5 decisions.
- **Confidence:** 75%
- **Outcome:** PENDING — need 5 more decisions to evaluate
