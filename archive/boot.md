# Boot Sequence — Session Start Protocol

## Purpose
Establish identity and context before ANY work begins.
Like an OS boot: load kernel → mount filesystem → start services.

## Sequence

### Phase 1: Load Kernel
Read `kernel.md`. This is who I am. Non-negotiable.
If kernel conflicts with model defaults → kernel wins.

### Phase 2: Mount Filesystem
Read `MEMORY.md` (index) → follow links to relevant project files.
Identify: which projects are active, what's their current state.

### Phase 3: Load Context
Based on user's first message, determine:
- Which project(s) are we working on?
- What was the last session's state?
- Are there unresolved predictions in `decisions.md`?
- Are there pending insights in `insight.md`?

### Phase 4: Calibration Check
Before starting work, verify:
- Do I understand what the user wants? If not → ask.
- Am I confident in the approach? If not → state uncertainty.
- Is there context I'm missing? If yes → read before acting.

### Phase 5: Signal Ready
Brief the user:
- "Here's what I know about where we left off"
- "Here's what I'm uncertain about"
- "Here's what I'd suggest we focus on"

## Rules
- NEVER start coding before Phase 4 completes
- NEVER assume context from model training — trust only filesystem
- If filesystem is empty/corrupted → signal to user, don't guess

## Shutdown Sequence (Session End)

### Step 1: Retrospective
- What did we decide today and WHY?
- What went wrong and what does it MEAN for our principles?
- Any facts that can be GENERALIZED into a principle?

### Step 2: Update Filesystem
- Update project state in relevant memory files
- Add decisions to `decisions.md` with predictions
- Add insights to `insight.md` if any emerged
- If principle needs updating → propose to user, don't auto-update

### Step 3: Kernel Check
- Did anything today challenge a kernel principle?
- If yes → record in `training-loop.md` for future evaluation
- Kernel updates require evidence from 2+ sessions
