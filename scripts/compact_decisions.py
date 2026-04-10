"""Compact decisions.md: archive resolved decisions, classify PENDING.

Supports two formats:
- Legacy (regex): decisions without inline metadata (D001-D074)
- New (<!--fm-->): decisions with inline YAML metadata (D075+)

Both formats coexist. Scripts parse <!--fm...fm--> when present,
fall back to regex when not.

Usage:
    python compact_decisions.py                # dry-run
    python compact_decisions.py --execute      # apply

Output:
    decisions.md          — PENDING + last N resolved + session headers
    decisions-archive.md  — all resolved decisions (append-only)
"""

from __future__ import annotations

import re
import sys
import yaml
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

OS_ROOT = Path(__file__).resolve().parent.parent
DECISIONS_PATH = OS_ROOT / "decisions.md"
ARCHIVE_PATH = OS_ROOT / "decisions-archive.md"

KEEP_RESOLVED = 10

# Customize: projects known to be stale/abandoned
STALE_PROJECTS = set()  # Add your stale project names here


@dataclass
class Block:
    header: str
    lines: list[str]
    kind: str  # "preamble", "decision", "session"
    decision_id: str
    outcome: str  # "PENDING", "resolved", ""
    pending_class: str  # "ACTIVE", "OVERDUE", "STALE", "BLOCKED", ""
    revisit_date: date | None
    project: str
    weight: str
    confidence: int  # 0-100 or -1
    depends_on: list[str] = field(default_factory=list)
    needs_review: bool = False
    has_frontmatter: bool = False


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _extract_fm(lines: list[str]) -> dict | None:
    """Extract <!--fm ... fm--> YAML from block body."""
    text = "\n".join(lines)
    m = re.search(r"<!--fm\s*\n(.+?)\nfm-->", text, re.DOTALL)
    if not m:
        return None
    try:
        parsed = yaml.safe_load(m.group(1))
        return parsed if isinstance(parsed, dict) else None
    except yaml.YAMLError:
        return None


def parse_blocks(text: str) -> list[Block]:
    """Split at ## boundaries, extract inline metadata per block."""
    lines = text.split("\n")
    blocks: list[Block] = []
    cur_header = ""
    cur_lines: list[str] = []

    def flush():
        nonlocal cur_header, cur_lines
        if cur_header or cur_lines:
            fm = _extract_fm(cur_lines) if cur_header else None
            blocks.append(_classify(cur_header, cur_lines, fm))
        cur_header = ""
        cur_lines = []

    for line in lines:
        if line.startswith("## "):
            flush()
            cur_header = line
        else:
            cur_lines.append(line)
    flush()
    return blocks


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def _classify(header: str, lines: list[str], fm: dict | None) -> Block:
    if not header:
        return Block(header=header, lines=lines, kind="preamble",
                     decision_id="", outcome="", pending_class="",
                     revisit_date=None, project="", weight="", confidence=-1)

    if re.match(r"^## (Session |PENDING Summary|Recent Resolved|OVERDUE|STALE)", header):
        return Block(header=header, lines=lines, kind="session",
                     decision_id="", outcome="", pending_class="",
                     revisit_date=None, project="", weight="", confidence=-1)

    did = ""
    m = re.match(r"^## (D\d+)", header)
    if m:
        did = m.group(1)

    if fm:
        return _from_yaml(header, lines, fm, did)
    return _from_regex(header, lines, did)


def _from_yaml(header: str, lines: list[str], fm: dict, did: str) -> Block:
    outcome = "PENDING" if fm.get("status", "pending") == "pending" else "resolved"
    project = str(fm.get("project", ""))
    weight = str(fm.get("weight", ""))
    confidence = int(fm.get("confidence", -1))
    depends_on = fm.get("depends_on") or []
    if isinstance(depends_on, str):
        depends_on = [depends_on]

    revisit_date = None
    rd = fm.get("revisit")
    if isinstance(rd, date):
        revisit_date = rd
    elif rd:
        try:
            revisit_date = datetime.strptime(str(rd), "%Y-%m-%d").date()
        except ValueError:
            pass

    full_text = "\n".join(lines)
    pc = _classify_pending(project, revisit_date, full_text) if outcome == "PENDING" else ""

    return Block(header=header, lines=lines, kind="decision",
                 decision_id=fm.get("id", did) or did,
                 outcome=outcome, pending_class=pc,
                 revisit_date=revisit_date, project=project,
                 weight=weight, confidence=confidence,
                 depends_on=depends_on, has_frontmatter=True)


def _from_regex(header: str, lines: list[str], did: str) -> Block:
    full = "\n".join(lines)

    outcome = "resolved"
    if re.search(r"\*\*Outcome:\*\*.*PENDING", full):
        outcome = "PENDING"

    project = ""
    pm = re.search(r"\*\*Project:\*\*\s*(.+?)(?:\n|$)", full)
    if pm:
        project = pm.group(1).strip()

    weight = ""
    wm = re.search(r"\bW([0-5])\b", full)
    if wm:
        weight = f"W{wm.group(1)}"

    confidence = -1
    cm = re.search(r"\*\*Confidence:\*\*\s*(\d+)%?", full)
    if cm:
        confidence = int(cm.group(1))

    revisit_date = None
    rm = re.search(
        r"[Rr]evisit.*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})",
        full)
    if rm:
        try:
            revisit_date = datetime.strptime(f"{rm.group(1)} {rm.group(2)}", "%B %Y").date()
        except ValueError:
            pass

    pc = _classify_pending(project, revisit_date, full) if outcome == "PENDING" else ""

    return Block(header=header, lines=lines, kind="decision",
                 decision_id=did, outcome=outcome, pending_class=pc,
                 revisit_date=revisit_date, project=project,
                 weight=weight, confidence=confidence)


def _classify_pending(project: str, revisit_date: date | None, text: str) -> str:
    today = date.today()

    for stale in STALE_PROJECTS:
        if stale.lower() in project.lower() or stale.lower() in text.lower():
            return "STALE"

    if revisit_date and revisit_date < today.replace(day=1):
        return "OVERDUE"

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    for i, name in enumerate(months, 1):
        m = re.search(rf"[Rr]evisit.*{name}\s+(\d{{4}})", text)
        if m:
            try:
                if date(int(m.group(1)), i, 1) < today.replace(day=1):
                    return "OVERDUE"
            except ValueError:
                pass

    return "ACTIVE"


# ---------------------------------------------------------------------------
# Staleness propagation
# ---------------------------------------------------------------------------

def propagate_staleness(decisions: list[Block]) -> None:
    """Flag pending decisions whose dependency has been resolved."""
    resolved_ids = {d.decision_id for d in decisions if d.outcome == "resolved" and d.decision_id}
    for d in decisions:
        if d.outcome == "PENDING" and d.depends_on:
            if any(dep in resolved_ids for dep in d.depends_on):
                d.needs_review = True


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def block_to_text(block: Block) -> str:
    parts = []
    if block.header:
        parts.append(block.header)
    parts.extend(block.lines)
    return "\n".join(parts)


def compact(blocks: list[Block], dry_run: bool = True) -> dict:
    preamble = [b for b in blocks if b.kind == "preamble"]
    sessions = [b for b in blocks if b.kind == "session"]
    decisions = [b for b in blocks if b.kind == "decision"]

    resolved = [d for d in decisions if d.outcome == "resolved"]
    pending = [d for d in decisions if d.outcome == "PENDING"]

    propagate_staleness(decisions)
    needs_review = [d for d in pending if d.needs_review]
    active = [d for d in pending if d.pending_class == "ACTIVE"]
    overdue = [d for d in pending if d.pending_class == "OVERDUE"]
    stale = [d for d in pending if d.pending_class == "STALE"]
    blocked = [d for d in pending if d.pending_class == "BLOCKED"]
    with_fm = [d for d in decisions if d.has_frontmatter]

    archive_resolved = resolved[:-KEEP_RESOLVED] if len(resolved) > KEEP_RESOLVED else []
    keep_resolved = resolved[-KEEP_RESOLVED:] if len(resolved) > KEEP_RESOLVED else resolved

    stats = {
        "total": len(decisions), "resolved": len(resolved),
        "pending": len(pending), "active": len(active),
        "overdue": len(overdue), "stale": len(stale),
        "blocked": len(blocked), "needs_review": len(needs_review),
        "with_fm": len(with_fm), "archive": len(archive_resolved),
        "keep": len(keep_resolved), "sessions": len(sessions),
    }

    if dry_run:
        return stats

    # --- Build active file ---
    out: list[str] = []
    for b in preamble:
        out.append(block_to_text(b))

    out.append("")
    out.append(f"> **Compacted {date.today()}**: {len(archive_resolved)} resolved archived. {len(keep_resolved)} recent resolved kept.")
    out.append("")
    out.append("## PENDING Summary")
    out.append(f"- **ACTIVE:** {len(active)}")
    out.append(f"- **OVERDUE:** {len(overdue)}")
    out.append(f"- **STALE:** {len(stale)}")
    if needs_review:
        out.append(f"- **NEEDS REVIEW:** {len(needs_review)} (dependency resolved)")
    out.append("")

    def _label(d: Block) -> str:
        return d.header.split(": ", 1)[-1] if ": " in d.header else d.header

    if overdue:
        out.append("### OVERDUE")
        for d in overdue:
            out.append(f"- **{d.decision_id}**: {_label(d)}")
        out.append("")

    if needs_review:
        out.append("### NEEDS REVIEW — dependency resolved")
        for d in needs_review:
            rdeps = [dep for dep in d.depends_on if dep in {r.decision_id for r in resolved}]
            out.append(f"- **{d.decision_id}**: {_label(d)} (deps: {', '.join(rdeps)})")
        out.append("")

    if stale:
        out.append("### STALE")
        for d in stale:
            out.append(f"- **{d.decision_id}**: {_label(d)}")
        out.append("")

    for s in sessions[-5:]:
        out.append(block_to_text(s))

    out.extend(["", "---", ""])
    for d in pending:
        tag = f" [{d.pending_class}]"
        if d.needs_review:
            tag += " [NEEDS REVIEW]"
        h = re.sub(r"\s*\[(ACTIVE|OVERDUE|STALE|BLOCKED|NEEDS REVIEW)\]", "", d.header.rstrip())
        out.append(h + tag)
        out.extend(d.lines)

    out.extend(["", "---", f"## Recent Resolved (last {KEEP_RESOLVED})", ""])
    for d in keep_resolved:
        out.append(block_to_text(d))

    # --- Archive ---
    arch: list[str] = []
    if ARCHIVE_PATH.exists():
        arch.append(ARCHIVE_PATH.read_text(encoding="utf-8").rstrip())
        arch.append("")
    else:
        arch.extend(["# Decision Archive", "", "Resolved decisions archived by compaction.", "", "---", ""])

    arch.extend([f"## Archived {date.today()}", ""])
    for d in archive_resolved:
        arch.append(block_to_text(d))

    DECISIONS_PATH.write_text("\n".join(out), encoding="utf-8")
    ARCHIVE_PATH.write_text("\n".join(arch), encoding="utf-8")
    return stats


def main():
    dry_run = "--execute" not in sys.argv
    text = DECISIONS_PATH.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    stats = compact(blocks, dry_run=dry_run)

    mode = "DRY RUN" if dry_run else "EXECUTED"
    print(f"=== Compaction {mode} ===")
    print(f"Total: {stats['total']} | Resolved: {stats['resolved']} | PENDING: {stats['pending']}")
    print(f"  ACTIVE={stats['active']} OVERDUE={stats['overdue']} STALE={stats['stale']} BLOCKED={stats['blocked']}")
    print(f"  Needs review: {stats['needs_review']} | With frontmatter: {stats['with_fm']}")
    print(f"Archive: {stats['archive']} | Keep resolved: {stats['keep']}")
    if dry_run:
        print("\nRun with --execute to apply.")


if __name__ == "__main__":
    main()
