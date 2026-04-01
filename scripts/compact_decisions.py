"""Compact decisions.md: archive resolved decisions, classify PENDING.

As decisions accumulate, the file grows beyond what AI models can load at boot.
This script splits it into an active file (PENDING + recent resolved) and an
append-only archive (old resolved decisions). Zero data loss guaranteed.

Usage:
    python compact_decisions.py                # dry-run: show what would happen
    python compact_decisions.py --execute      # actually write files

Output:
    decisions.md          — PENDING + last N resolved + session headers
    decisions-archive.md  — all resolved decisions (append-only)
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

OS_ROOT = Path(__file__).resolve().parent.parent
DECISIONS_PATH = OS_ROOT / "decisions.md"
ARCHIVE_PATH = OS_ROOT / "decisions-archive.md"

KEEP_RESOLVED = 10  # keep last N resolved in active file

# Add project names that are abandoned/stale for your context.
# Decisions referencing these projects will be classified as STALE.
STALE_PROJECTS: set[str] = set()
# Example: STALE_PROJECTS = {"OldProject", "DeprecatedTool"}


@dataclass
class Block:
    """One section of decisions.md (decision, session header, or preamble)."""

    header: str
    lines: list[str]
    kind: str  # "preamble", "decision", "session"
    decision_id: str  # "D001" or ""
    outcome: str  # "PENDING", "resolved", ""
    pending_class: str  # "ACTIVE", "OVERDUE", "STALE", "BLOCKED", ""
    revisit_date: date | None
    project: str


def parse_blocks(text: str) -> list[Block]:
    """Parse decisions.md into structured blocks."""
    lines = text.split("\n")
    blocks: list[Block] = []
    current_header = ""
    current_lines: list[str] = []

    def flush():
        nonlocal current_header, current_lines
        if current_header or current_lines:
            block = classify_block(current_header, current_lines)
            blocks.append(block)
        current_header = ""
        current_lines = []

    for line in lines:
        if line.startswith("## "):
            flush()
            current_header = line
        else:
            current_lines.append(line)

    flush()
    return blocks


def classify_block(header: str, lines: list[str]) -> Block:
    """Classify a block as preamble, decision, or session."""
    full_text = "\n".join(lines)

    # Preamble (before first ## header)
    if not header:
        return Block(
            header=header, lines=lines, kind="preamble",
            decision_id="", outcome="", pending_class="",
            revisit_date=None, project="",
        )

    # Session header
    if re.match(r"^## Session ", header):
        return Block(
            header=header, lines=lines, kind="session",
            decision_id="", outcome="", pending_class="",
            revisit_date=None, project="",
        )

    # Compaction-generated sections (skip on re-run for idempotency)
    if re.match(r"^## (PENDING Summary|Recent Resolved|OVERDUE|STALE)", header):
        return Block(
            header=header, lines=lines, kind="session",
            decision_id="", outcome="", pending_class="",
            revisit_date=None, project="",
        )

    # Decision
    did_match = re.match(r"^## (D\d+)", header)
    decision_id = did_match.group(1) if did_match else ""

    # Extract outcome
    outcome = "resolved"
    if "PENDING" in full_text and re.search(r"\*\*Outcome:\*\*.*PENDING", full_text):
        outcome = "PENDING"

    # Extract project
    project = ""
    proj_match = re.search(r"\*\*Project:\*\*\s*(.+?)(?:\n|$)", full_text)
    if proj_match:
        project = proj_match.group(1).strip()

    # Extract revisit date (try "Month YYYY" format)
    revisit_date = None
    revisit_match = re.search(
        r"[Rr]evisit.*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})",
        full_text,
    )
    if revisit_match:
        try:
            revisit_date = datetime.strptime(
                f"{revisit_match.group(1)} {revisit_match.group(2)}",
                "%B %Y",
            ).date()
        except ValueError:
            pass

    # Classify PENDING
    pending_class = ""
    if outcome == "PENDING":
        pending_class = classify_pending(project, revisit_date, full_text)

    return Block(
        header=header, lines=lines, kind="decision",
        decision_id=decision_id, outcome=outcome,
        pending_class=pending_class, revisit_date=revisit_date,
        project=project,
    )


def classify_pending(project: str, revisit_date: date | None, text: str) -> str:
    """Classify a PENDING decision: ACTIVE, OVERDUE, STALE, BLOCKED."""
    today = date.today()

    # Stale: project abandoned or context changed
    for stale in STALE_PROJECTS:
        if stale.lower() in project.lower() or stale.lower() in text.lower():
            return "STALE"

    # Overdue: revisit date (month-level) has passed
    if revisit_date and revisit_date < today.replace(day=1):
        return "OVERDUE"

    # Check all month references in "Revisit when" context
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    for i, month_name in enumerate(month_names, 1):
        pattern = rf"[Rr]evisit.*{month_name}\s+(\d{{4}})"
        m = re.search(pattern, text)
        if m:
            try:
                revisit = date(int(m.group(1)), i, 1)
                if revisit < today.replace(day=1):
                    return "OVERDUE"
            except ValueError:
                pass

    return "ACTIVE"


def block_to_text(block: Block) -> str:
    """Render block back to markdown."""
    parts = []
    if block.header:
        parts.append(block.header)
    parts.extend(block.lines)
    return "\n".join(parts)


def compact(blocks: list[Block], dry_run: bool = True) -> dict:
    """Perform compaction, return stats."""
    preamble = [b for b in blocks if b.kind == "preamble"]
    sessions = [b for b in blocks if b.kind == "session"]
    decisions = [b for b in blocks if b.kind == "decision"]

    resolved = [d for d in decisions if d.outcome == "resolved"]
    pending = [d for d in decisions if d.outcome == "PENDING"]

    # Classify pending
    active = [d for d in pending if d.pending_class == "ACTIVE"]
    overdue = [d for d in pending if d.pending_class == "OVERDUE"]
    stale = [d for d in pending if d.pending_class == "STALE"]
    blocked = [d for d in pending if d.pending_class == "BLOCKED"]

    # Keep last N resolved in active file
    archive_resolved = resolved[:-KEEP_RESOLVED] if len(resolved) > KEEP_RESOLVED else []
    keep_resolved = resolved[-KEEP_RESOLVED:] if len(resolved) > KEEP_RESOLVED else resolved

    stats = {
        "total_decisions": len(decisions),
        "resolved": len(resolved),
        "pending_total": len(pending),
        "pending_active": len(active),
        "pending_overdue": len(overdue),
        "pending_stale": len(stale),
        "pending_blocked": len(blocked),
        "archive_count": len(archive_resolved),
        "keep_resolved_count": len(keep_resolved),
        "sessions": len(sessions),
    }

    if dry_run:
        return stats

    # Build active file
    active_parts = []

    # Preamble
    for b in preamble:
        active_parts.append(block_to_text(b))

    # Compaction notice
    active_parts.append("")
    active_parts.append(f"> **Compacted {date.today()}**: {len(archive_resolved)} resolved decisions archived to `decisions-archive.md`. {len(keep_resolved)} recent resolved kept here.")
    active_parts.append("")

    # PENDING classification summary
    active_parts.append("## PENDING Summary")
    active_parts.append(f"- **ACTIVE:** {len(active)} (waiting for event/data)")
    active_parts.append(f"- **OVERDUE:** {len(overdue)} (revisit date passed)")
    active_parts.append(f"- **STALE:** {len(stale)} (context changed, likely irrelevant)")
    active_parts.append("")

    if overdue:
        active_parts.append("### OVERDUE — need resolution")
        for d in overdue:
            label = d.header.split(": ", 1)[-1] if ": " in d.header else d.header
            active_parts.append(f"- **{d.decision_id}**: {label}")
        active_parts.append("")

    if stale:
        active_parts.append("### STALE — consider closing")
        for d in stale:
            label = d.header.split(": ", 1)[-1] if ": " in d.header else d.header
            active_parts.append(f"- **{d.decision_id}**: {label}")
        active_parts.append("")

    # Session headers (keep recent ones)
    recent_sessions = sessions[-5:]
    for s in recent_sessions:
        active_parts.append(block_to_text(s))

    # All PENDING decisions (full text, tagged)
    active_parts.append("")
    active_parts.append("---")
    active_parts.append("")

    for d in pending:
        tag = f" [{d.pending_class}]" if d.pending_class else ""
        tagged_header = d.header.rstrip() + tag
        active_parts.append(tagged_header)
        active_parts.extend(d.lines)

    # Last N resolved (full text)
    active_parts.append("")
    active_parts.append("---")
    active_parts.append(f"## Recent Resolved (last {KEEP_RESOLVED})")
    active_parts.append("")

    for d in keep_resolved:
        active_parts.append(block_to_text(d))

    # Build archive file (append-only)
    archive_parts = []
    if ARCHIVE_PATH.exists():
        archive_parts.append(ARCHIVE_PATH.read_text(encoding="utf-8").rstrip())
        archive_parts.append("")
    else:
        archive_parts.append("# Decision Archive")
        archive_parts.append("")
        archive_parts.append("Resolved decisions moved from decisions.md by compaction.")
        archive_parts.append("")
        archive_parts.append("---")
        archive_parts.append("")

    archive_parts.append(f"## Archived {date.today()}")
    archive_parts.append("")
    for d in archive_resolved:
        archive_parts.append(block_to_text(d))

    # Write files
    DECISIONS_PATH.write_text("\n".join(active_parts), encoding="utf-8")
    ARCHIVE_PATH.write_text("\n".join(archive_parts), encoding="utf-8")

    return stats


def main():
    dry_run = "--execute" not in sys.argv

    text = DECISIONS_PATH.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    stats = compact(blocks, dry_run=dry_run)

    mode = "DRY RUN" if dry_run else "EXECUTED"
    print(f"=== Compaction {mode} ===")
    print(f"Total decisions:     {stats['total_decisions']}")
    print(f"  Resolved:          {stats['resolved']}")
    print(f"  PENDING total:     {stats['pending_total']}")
    print(f"    ACTIVE:          {stats['pending_active']}")
    print(f"    OVERDUE:         {stats['pending_overdue']}")
    print(f"    STALE:           {stats['pending_stale']}")
    print(f"    BLOCKED:         {stats['pending_blocked']}")
    print(f"Session headers:     {stats['sessions']}")
    print(f"---")
    print(f"Archive (move out):  {stats['archive_count']} resolved")
    print(f"Keep in active:      {stats['keep_resolved_count']} resolved + {stats['pending_total']} PENDING")

    if dry_run:
        print("\nRun with --execute to apply changes.")


if __name__ == "__main__":
    main()
