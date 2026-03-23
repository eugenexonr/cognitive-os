# Cognitive OS — Launch Kit

Everything needed to launch on open source. Checklist + drafts + instructions.

---

## Pre-Launch Checklist

- [x] README with competitive positioning
- [x] Real examples with actual numbers (anonymized)
- [x] Cursor driver (full .cursorrules, not placeholder)
- [x] Codex driver (beta template)
- [x] cog-update.sh mentioned in README
- [x] Archive explained in project structure
- [ ] **Terminal demo GIF** (see instructions below)
- [ ] **GitHub repo public** (currently private at eugenexonr/cognitive-os-private)
- [ ] **15-20 initial stars** from personal network
- [ ] **Show HN post** (draft below)
- [ ] **Reddit posts** (drafts below)

---

## Show HN Post Draft

**Title:** `Show HN: Cognitive OS – Prediction-error learning layer for AI agents`

**URL:** `https://github.com/eugenexonr/cognitive-os`

**Comment (post immediately after submission):**

```
Hi HN, I built this after 3 months of using AI (Claude, GPT, Codex) as CTO
across 5 production projects.

The problem: my AI kept contradicting decisions it made days earlier. It would
recommend X on Monday, then recommend not-X on Thursday, with no awareness of
the contradiction. Memory tools (claude-mem, etc.) solve "AI forgets what
happened." But my problem was deeper — AI doesn't learn from what happened.

Cognitive OS adds a prediction-error learning loop:

1. Every significant decision gets a PREDICTION with confidence %
2. When the outcome is known, compare prediction to reality
3. The gap between prediction and outcome = where learning happens
4. Over 73 decisions, I can see calibration patterns: my AI is over-confident
   on market predictions (50-60% accuracy) and well-calibrated on technical
   ones (85-90% accuracy)

It also includes anti-drift — binary checks that work WHEN the AI is already
drifting. Key insight: judgment rules ("cite the relevant principle") fail
during drift because judgment is compromised. Binary checks ("did I verify
this number? yes/no") require only honesty, not judgment.

Real example: my AI stated "$0 deposit required" for a supplier. Anti-drift
check: source? No source. Actual answer: $1,000 minimum. The (?) marker
caught a $1,000 error.

It's model-agnostic (markdown files, zero dependencies), works with Claude Code,
Cursor, ChatGPT, or any LLM. MIT licensed.

What I'd love feedback on:
- Does prediction-error tracking for AI decisions resonate with your workflow?
- Is the anti-drift mechanism (binary checks > judgment rules) useful outside
  my specific setup?
- Would you use this, or is this solving a problem only power users have?

Happy to answer questions about the methodology or share more data.
```

---

## Reddit Post Drafts

### r/ClaudeAI

**Title:** `I tracked 73 decisions my AI made over 3 months. Here's what I learned about calibration.`

**Body:**

```
I've been using Claude as CTO across 5 production projects. After month 1,
I noticed a pattern: Claude would confidently recommend Approach A, then
a week later confidently recommend the opposite — with zero awareness of
the contradiction.

So I started tracking every significant decision with a prediction and
confidence percentage. After 73 decisions:

- Technical decisions (architecture, patterns): 85-90% confidence,
  mostly confirmed. Claude is well-calibrated here.
- Market/business decisions: 50-60% confidence, mixed outcomes.
  Claude is appropriately uncertain here (good!).
- The scary part: without tracking, I couldn't tell which category
  a recommendation fell into. Both SOUND equally confident.

I also built "anti-drift" — binary checks that catch self-contradiction.
The key insight: telling an AI "always cite your reasoning" doesn't work
during drift (reasoning is compromised). But "did you verify this number?
yes/no" works because it requires honesty, not judgment.

Open sourced the whole system: [link]

It's just markdown files — works with Claude Code, Cursor, ChatGPT,
anything. Zero dependencies. The value isn't in the files, it's in the
prediction-error loop that compounds learning over time.

Curious if anyone else has tried systematic decision tracking with AI.
```

### r/LocalLLaMA

**Title:** `Model-agnostic "learning layer" for AI agents — prediction-error tracking + anti-drift (open source, markdown-only)`

**Body:**

```
Built a system for making AI agents learn from their own mistakes,
model-agnostic (works with any LLM):

Core idea: every significant decision gets a prediction + confidence %.
When the outcome is known, compare. The gap = learning signal.

After 73 decisions across 5 projects, the calibration data is interesting:
- High-confidence (85%+) technical predictions: 90% accurate
- Low-confidence (50-60%) market predictions: ~50% accurate
- Without tracking, both sound equally confident in the moment

Also includes "anti-drift" — binary self-correction checks inspired by
computational neuroscience (prediction-error minimization / free energy
principle). Key finding: binary checks (verified? yes/no) work during
drift; judgment rules (which principle applies?) don't.

It's not a framework — it's 4 markdown files + 3 protocols. Zero
dependencies, zero lock-in. MIT licensed.

Drivers for Claude Code (skills), Cursor (.cursorrules), Codex
(task templates), and raw system prompts.

[link]

Would love feedback from people running local models — does the
prediction-error tracking translate to open-weight models, or is
calibration a closed-model thing?
```

---

## Terminal Demo — Instructions for Recording

### What You Need

1. **Windows Terminal** (already installed) or any terminal
2. **asciinema** — terminal recorder that creates lightweight, embeddable recordings

### Install asciinema (Windows)

```bash
pip install asciinema
```

If pip doesn't work, alternative: use **ScreenToGif** (https://www.screentogif.com/)
- Free, portable, records any screen area
- Export as GIF (max 15MB for GitHub README)
- Simpler than asciinema on Windows

### What to Record (90 seconds max)

**Script — follow this exactly:**

```
Scene 1 (10 sec): Show the files
$ ls ~/cognitive-os/
→ kernel.md  decisions.md  insight.md  protocols/

Scene 2 (15 sec): Boot
$ claude
> boot
→ [Vector shows: kernel loaded, 34 pending decisions, ready]

Scene 3 (20 sec): Make a decision
> [ask Claude to compare two approaches for something]
→ [Claude responds, cites W3 (Simplicity)]
> /cos-decide
→ [Decision recorded with prediction + confidence]

Scene 4 (15 sec): Show anti-drift
> [ask about pricing of something]
→ [Claude writes a number with (?)]
→ "No source for this number — marking as unverified"

Scene 5 (10 sec): Show calibration
$ grep "Outcome:" ~/cognitive-os/decisions.md | head -5
→ [Shows CONFIRMED, CONFIRMED, Partially wrong, PENDING...]

Scene 6 (5 sec): End
"73 decisions. 51 insights. 3 months. Zero dependencies."
```

### Recording Steps (ScreenToGif)

1. Open ScreenToGif
2. Click **Recorder**
3. Position the frame over your terminal (make it ~800x500 pixels)
4. Set **FPS: 10** (keeps file small)
5. Click **Record** (F7)
6. Run the script above in your terminal
7. Click **Stop** (F7) when done
8. In the editor:
   - **Edit → Remove Duplicates** (reduces file size)
   - Speed up boring parts (select frames → Edit → Override Delay → 50ms)
   - Slow down key moments (select frames → Edit → Override Delay → 200ms)
9. **Save As → GIF**, quality: 15-20, max 10MB
10. Save to `cognitive-os/assets/demo.gif`

### Add GIF to README

After recording, add this right after the title:

```markdown
# Cognitive OS

**Identity and learning layer for AI agents.**

![Demo](assets/demo.gif)
```

### Alternative: Short Video Instead of GIF

If GIF is too large (>10MB), record a video:

1. Use **OBS Studio** (free) or Windows Game Bar (Win+G → Record)
2. Record same 90-second script
3. Upload to YouTube (unlisted)
4. Add to README:

```markdown
[![Demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID)
```

YouTube embed looks more professional and has no file size limit.

---

## Launch Day Sequence

### Day -1 (preparation)
1. Record demo GIF/video
2. Add to README
3. Make GitHub repo public (Settings → Danger Zone → Change visibility)
4. Send link to 10-15 people you know, ask them to star it
5. Verify README renders correctly on GitHub

### Day 0 (launch — Monday or Tuesday, ~9am US Eastern / ~4pm Moscow)
1. Post Show HN (use draft above)
2. Post first comment immediately (use draft above)
3. Monitor HN for questions — respond to every comment within 1 hour
4. Be technical, not salesy. Agree with criticism before addressing it.

### Day 1-2
1. Post on r/ClaudeAI (use draft above)
2. Post on r/LocalLLaMA (use draft above)
3. Respond to every GitHub issue within 24 hours

### Week 1-2
1. Write dev.to article: "I Tracked 73 Decisions My AI Made. Here's What I Learned."
2. Post on Twitter/X with key insight + link
3. If HN didn't hit frontpage → post again with different angle in 2 weeks

### Ongoing
1. Respond to issues/discussions within 24h
2. Publish 1-2 articles/week on dev.to or blog
3. Re-launch on HN with new angle every 2-3 weeks (5-7% hit rate)

---

## Realistic Expectations

- **Month 1:** 200-500 stars (if HN hits, could be 500-1000)
- **Active users:** 10-30 (not all stars = users)
- **GitHub issues:** 5-15 (good signal of engagement)
- **HN frontpage probability:** ~30% with good execution
- **Total audience for this product:** ~5,000-10,000 people worldwide

The value is real even at 50 stars — it's a clean documented framework for our own projects and a credibility signal as CTO.
