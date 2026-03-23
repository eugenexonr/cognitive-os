# Cognitive OS — Codex Driver (Beta)

> Codex runs isolated tasks. This template wraps each task with OS context.

## Task Preamble (add to every Codex task)

```
CONTEXT:
- Read ~/cognitive-os/kernel.md for decision weights (W0-W5)
- This task is part of project: [PROJECT_NAME]

CONSTRAINTS:
- Cite primary kernel weight for any architectural decision
- Every number must have a source or be marked with (?)
- If uncertain about approach, state confidence % and why

ON COMPLETION:
- If you made a significant decision, append to ~/cognitive-os/decisions.md:
  ## DXXX: [title]
  - **Primary weight:** W[N] — [why]
  - **Decision:** [what]
  - **Prediction:** [expected outcome]
  - **Confidence:** [%]
  - **Outcome:** PENDING
```

## Review Assertions (add to task verification)

```
VERIFY:
- [ ] No hardcoded secrets in code
- [ ] All architectural decisions cite a kernel weight
- [ ] Tests exist for new functionality
- [ ] No numbers stated without source
```

## Notes

- Codex cannot read local files during execution — paste kernel content into task preamble
- For multi-step tasks, Vector (Claude Code) writes the spec, Codex executes, Vector reviews
- See `examples/solo-founder/` for real decision format
