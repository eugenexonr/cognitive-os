# Cognitive OS — Project Plan

## What This Is

Cognitive OS is a model-agnostic identity and learning layer for AI agents.
Not another agent framework. Not another prompt template.
A methodology that gives AI persistent identity, prediction-error learning, and self-correction.

**Origin:** Built over 3 months (Jan-Mar 2026) across 5 production projects (Esimra, BCC, Connect, AI Marketer, TechVol-Alpha). Battle-tested with real money, real bugs, real decisions.

**Unique:** 5 of 7 core components have zero analogues in the AI agent ecosystem (including OpenClaw 247K stars, LangChain, CrewAI, AutoGPT).

---

## Four Parallel Tracks

### Track 1: Upgrade Existing Projects (Skills + Rules + Hooks)

**Goal:** Apply Claude Code platform features (skills, rules, hooks) to our production projects. Stop using text instructions where executable automation exists.

**What we learned from Thariq's post (Anthropic, March 2026):**
- Skills are FOLDERS with scripts, not markdown files
- Progressive disclosure > monolithic CLAUDE.md
- On-demand hooks prevent production incidents
- Description field is for model triggering, not human reading
- Skills compose with each other

**Current state (Boris audit findings):**
- Root `.claude/settings.json` — 1 PostToolUse hook (ruff + prettier) ✅
- n8n-mcp `.claude/agents/` — 8 agent definitions ✅
- ALL other projects — zero skills, zero rules, zero commands, zero agents ❌
- CLAUDE.md files — 4 strong ones, but monolithic (up to 705 lines) ⚠️
- MEMORY.md — truncated at 200 lines due to no progressive disclosure ❌

**Action items:**

| # | Task | Project | Impact | Effort |
|---|---|---|---|---|
| 1.1 | Add PreToolUse safety hook (block DROP TABLE, --force, rm -rf) | Root .claude/ | Prevents production incidents | 30min |
| 1.2 | Create `.claude/rules/` with glob patterns for Esimra | esimstore | Context-specific guidance, smaller context | 1h |
| 1.3 | Create `/verify-esimra` skill with Playwright scripts | esimstore | Automated deploy verification | 3h |
| 1.4 | Create `/boris` skill with executable scripts | Personal skills | Automated debugging protocol | 3h |
| 1.5 | Split esimra-connect CLAUDE.md (705 lines) into rules | esimra-connect | Progressive disclosure | 1h |
| 1.6 | Add agent definitions to esimstore, connect, BCC | All projects | Specialized agents per project | 2h |
| 1.7 | Create `/boot` skill for Cognitive OS session init | Personal skills | Automated boot protocol | 2h |
| 1.8 | Create `/decide` skill for structured decision recording | Personal skills | Auto weight citation, fixes I012 | 1h |

**Verification:** After each task, test that the skill/rule/hook actually triggers and works correctly.

---

### Track 2: Claude Certified Architect Preparation

**Goal:** Pass certification exam by applying exam concepts to real projects. Learn by doing, not by reading.

**Current readiness:** ~38% (need 72% to pass)

**Exam domains mapped to project tasks:**

| Domain | Weight | Current | Gap | Learning Task |
|---|---|---|---|---|
| D1: Agentic Architecture | 27% | 30% | Agent SDK hooks, multi-agent orchestration, guardrails | Track 1 tasks 1.4, 1.6, 1.7 — building skills IS learning D1 |
| D2: Tool Design & MCP | 18% | 50% | Writing own MCP tools, JSON schemas | Build MCP server for Connect API (expose as tools) |
| D3: Claude Code Config | 20% | 55% | .claude/rules/, commands, CI integration | Track 1 tasks 1.1, 1.2, 1.5 — upgrading projects IS learning D3 |
| D4: Prompt Engineering | 20% | 25% | tool_use API, tool_choice, prefill, caching | Migrate 1 AI Marketer agent flow to direct Anthropic API |
| D5: Context Management | 15% | 45% | Multi-agent error handling, Message Batches API | Formalize context budget, add prompt caching to kernel |

**Key insight:** Track 1 and Track 2 overlap ~70%. Building skills for our projects = learning exam material.

**What we already do correctly (above average):**
- Production multi-model orchestration (Vector/Opus + Codex + Sonnet)
- MCP integration (7+ servers in production)
- CLAUDE.md with gotchas, architecture rules, verification commands
- Cognitive OS memory system (ahead of Anthropic's documented patterns)

**What we lack (specific API knowledge):**
- Claude API `tool_use` with JSON schemas (never used directly — always via OpenRouter)
- `tool_choice` parameter (`{"type": "tool", "name": "analyze"}`)
- Agent SDK hooks syntax (`PostToolUse`, `PreToolUse` lifecycle)
- Prompt caching API (`cache_control: {"type": "ephemeral"}`)
- Message Batches API for parallel processing
- `.claude/rules/` with glob patterns (never created any)

**Study approach:** Build it → test it → record decision → verify knowledge gap closed.

---

### Track 3: Refine Cognitive OS Framework

**Goal:** Extract the methodology from our personal usage into a clean, model-agnostic framework that others can adopt.

**Core components (what makes this unique):**

1. **Kernel** — Identity + decision weights (W0-W5) + anti-patterns + heuristics
   - Model-agnostic: works with any LLM
   - Evidence-gated evolution: changes require proof from 2+ decisions
   - Not personality ("be friendly") but decision framework ("uncertainty > speed")

2. **Decision Loop** — Prediction → Outcome → Delta → Principle Update
   - Every significant decision recorded with confidence level
   - Outcomes tracked and compared to predictions
   - Calibration: over-confident (predicted 80%, failed) patterns detected
   - NO analogue exists in any AI framework

3. **Insight Mechanism** — Expectation → Reality → Delta → Fractal Check
   - Prediction-error based (not pattern matching)
   - Fractal validation: insight must hold at variable → module → service → business
   - META tag for cross-cutting patterns
   - NO analogue exists

4. **Anti-Drift** — Binary checks that work WHEN the model is drifting
   - `(?)` marker for unverified numbers (binary: verified or not)
   - Re-read kernel before conclusions (binary: re-read or not)
   - Evidence from I017: binary checks > judgment rules
   - Evidence from I031: Vector contradicted own decision 5 days later, caught by re-read

5. **Boot Protocol** — Session initialization that loads accumulated knowledge
   - Read kernel → read insights → check pending decisions → calibrate
   - Session fingerprint for continuity tracking

6. **Kernel Evolution** — Self-modifying identity with safety gates
   - 2+ decision outcomes showing same pattern → propose principle update
   - User approval required (not auto-update)
   - Version tracking with changelog and evidence

7. **Driver Pattern** — Platform-specific bridges to model-agnostic OS
   - OS files (kernel, decisions, insight) live independently
   - "Drivers" adapt OS to specific platforms (Claude Code skills, Cursor rules, Codex instructions)
   - Switch models without losing identity or learning

**What to extract vs what stays personal:**

| Extract (framework) | Stays personal |
|---|---|
| Weight system concept (W0-W5) | Specific weight VALUES |
| Decision format + prediction loop | Actual decisions (D001-D060) |
| Insight format + fractal check | Actual insights (I001-I033) |
| Boot protocol template | Project-specific memory files |
| Anti-drift mechanism | Personal gotchas list |
| Driver pattern + skill templates | Personal skill configurations |

---

### Track 4: Open Source Launch

**Goal:** Publish Cognitive OS on GitHub, gain initial traction (target: 500+ stars in first month).

**Positioning:** "Identity and learning layer for AI agents" — NOT another agent framework.

**Differentiator vs landscape:**
```
Execution frameworks:    OpenClaw, LangChain, CrewAI, AutoGPT
                         → HOW to run tools
                         → 200+ projects, red ocean

Cognitive layer:         Cognitive OS (this project)
                         → HOW to learn, remember, self-correct
                         → 0 projects, blue ocean
```

**Pre-launch checklist:**

- [ ] Clean templates with clear placeholders
- [ ] README that explains "why" in 30 seconds
- [ ] Architecture diagram (kernel/driver layers)
- [ ] 2-3 anonymized examples from real usage
- [ ] Getting started guide (15-minute setup)
- [ ] Claude Code driver (working skills)
- [ ] Cursor driver (working .cursorrules)
- [ ] 1 blog post: "My AI kept making the same mistakes"
- [ ] Demo GIF or 2-min video

**Launch channels (simultaneous):**
1. Hacker News: "Show HN: Cognitive OS — prediction-error learning for AI agents"
2. Reddit: r/LocalLLaMA + r/ClaudeAI + r/artificial
3. Twitter/X: thread (5-7 tweets) with demo
4. Dev.to: technical deep dive article

**Success metrics:**
- 500+ stars in month 1 = good (continue)
- 50-500 stars = okay (iterate on messaging)
- <50 stars = messaging failed (not the product)

**Timing:** Tuesday-Thursday, 9-11 AM EST for HN post.

---

## Dependencies Between Tracks

```
Track 1 (Skills/Rules)  ──→  Track 2 (Certification)
    Building skills         = learning exam material
         │
         ↓
Track 3 (Refine OS)      ──→  Track 4 (Open Source)
    Clean framework           = publishable repo
         │
         ↓
    Track 1 feeds back
    Skills become OS drivers
```

**Track 1 and 2 run in parallel** (70% overlap).
**Track 3 starts after Track 1 stabilizes** (need working skills to include as drivers).
**Track 4 is the final step** (need everything clean and tested).

---

## Timeline (realistic, solo founder)

| Week | Focus | Deliverable |
|---|---|---|
| Week 1 | Safety hook + Esimra rules + /boris skill | Production improvements + D3 exam prep |
| Week 2 | /boot + /decide skills + Connect MCP server | OS drivers + D1/D2 exam prep |
| Week 3 | Tool_use API migration (AI Marketer) + prompt caching | D4 exam prep + cost savings |
| Week 4 | Clean templates + anonymized examples + README | Framework extraction |
| Week 5 | Blog post + demo video + launch prep | Marketing assets |
| Week 6 | Open source launch | GitHub + HN + Reddit + Twitter |

**Note:** This is aspirational. Real timeline depends on Esimra revenue work, BCC beta, and founder's priorities. Each week is independent — if week 3 slips, week 4 can still start.

---

## Risk Register

| Risk | Prob | Impact | Mitigation |
|---|---|---|---|
| Track 1 takes longer than expected | 40% | Delays Track 3-4 | Start with highest-impact tasks (safety hook, /boris) |
| Certification exam harder than assessed | 30% | Need more study time | Hands-on learning through Track 1 reduces this risk |
| Open source gets no traction | 35% | Wasted launch effort | Worst case = clean documented framework for ourselves |
| Anthropic builds cognitive layer natively | 20% | Obsoletes project | First-mover advantage + model-agnostic positioning |
| Founder priorities shift (revenue > OS) | 50% | Pause Track 3-4 | Track 1-2 improve revenue projects regardless |

---

## Decision Record

### D070: Create Cognitive OS as open-source project
- **When:** 2026-03-17
- **Context:** Boris audit revealed 5/7 OS components have zero analogues in AI ecosystem. OpenClaw (247K stars) has execution but no learning. Claude Code Skills have automation but no identity. Gap is real and unoccupied.
- **Primary weight:** W4 (Evidence) — 3 months production usage, 60+ decisions, 33 insights, anti-drift mechanism proven by I031
- **Decision:** Extract methodology into model-agnostic framework, publish as open source
- **Prediction:** Will reach 500+ GitHub stars in first month if launched with proper positioning (HN + Reddit + Twitter simultaneously)
- **Confidence:** 50% — product is strong, but marketing execution is unproven for open source
- **Outcome:** PENDING
- **Revisit when:** After launch (Week 6) — check star count, community engagement, forks
