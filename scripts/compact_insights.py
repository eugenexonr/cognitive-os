"""Compact insight.md: graduate validated insights to separate archive file.

Over time, insights accumulate — many get validated and become reference material.
This script moves validated insights to a separate file, keeping the active file
focused on observations still being tested.

Usage:
    python compact_insights.py                # dry-run
    python compact_insights.py --execute      # apply
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

OS_ROOT = Path(__file__).resolve().parent.parent
INSIGHT_PATH = OS_ROOT / "insight.md"
VALIDATED_PATH = OS_ROOT / "insight-validated.md"


@dataclass
class InsightBlock:
    header: str
    lines: list[str]
    kind: str  # "preamble", "insight", "meta"
    insight_id: str
    status: str  # "validated", "observation", "fixing", "invalidated", etc.


def parse_insights(text: str) -> list[InsightBlock]:
    lines = text.split("\n")
    blocks: list[InsightBlock] = []
    current_header = ""
    current_lines: list[str] = []

    def flush():
        nonlocal current_header, current_lines
        if current_header or current_lines:
            blocks.append(classify_insight(current_header, current_lines))
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


def classify_insight(header: str, lines: list[str]) -> InsightBlock:
    full_text = "\n".join(lines)

    if not header:
        return InsightBlock(header=header, lines=lines, kind="preamble",
                            insight_id="", status="")

    if header.startswith("## META"):
        return InsightBlock(header=header, lines=lines, kind="meta",
                            insight_id="META", status="observation")

    iid_match = re.match(r"^## (I\d+)", header)
    insight_id = iid_match.group(1) if iid_match else ""

    status = ""
    status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", full_text)
    if status_match:
        status = status_match.group(1).lower()

    return InsightBlock(header=header, lines=lines, kind="insight",
                        insight_id=insight_id, status=status)


def block_to_text(block: InsightBlock) -> str:
    parts = []
    if block.header:
        parts.append(block.header)
    parts.extend(block.lines)
    return "\n".join(parts)


def compact(blocks: list[InsightBlock], dry_run: bool = True) -> dict:
    preamble = [b for b in blocks if b.kind == "preamble"]
    insights = [b for b in blocks if b.kind in ("insight", "meta")]

    # Only "validated" gets graduated. Everything else stays active.
    # This is a blacklist approach — new/unknown statuses default to active (safe).
    validated = [b for b in insights if b.status == "validated"]
    invalidated = [b for b in insights if b.status == "invalidated"]
    active = [b for b in insights if b.status not in ("validated", "invalidated")]

    stats = {
        "total": len(insights),
        "validated": len(validated),
        "observation": len([b for b in insights if b.status == "observation"]),
        "fixing": len([b for b in insights if b.status == "fixing"]),
        "invalidated": len(invalidated),
        "other_status": len([b for b in insights if b.status not in ("validated", "observation", "fixing", "invalidated", "")]),
        "graduate": len(validated),
        "keep_active": len(active),
    }

    if dry_run:
        return stats

    # Build active file
    active_parts = []
    for b in preamble:
        active_parts.append(block_to_text(b))

    active_parts.append("")
    active_parts.append(f"> **Compacted {date.today()}**: {len(validated)} validated insights graduated to `insight-validated.md`. {len(active)} active insights remain here.")
    active_parts.append("")

    for b in active:
        active_parts.append(block_to_text(b))

    # Build validated file (append-only)
    validated_parts = []
    if VALIDATED_PATH.exists():
        validated_parts.append(VALIDATED_PATH.read_text(encoding="utf-8").rstrip())
        validated_parts.append("")
    else:
        validated_parts.append("# Validated Insights Archive")
        validated_parts.append("")
        validated_parts.append("Proven cross-domain patterns graduated from insight.md.")
        validated_parts.append("These are reference-only — load on demand, not at boot.")
        validated_parts.append("")
        validated_parts.append("---")
        validated_parts.append("")

    validated_parts.append(f"## Graduated {date.today()}")
    validated_parts.append("")
    for b in validated:
        validated_parts.append(block_to_text(b))

    if invalidated:
        validated_parts.append("")
        validated_parts.append("## Invalidated")
        validated_parts.append("")
        for b in invalidated:
            validated_parts.append(block_to_text(b))

    INSIGHT_PATH.write_text("\n".join(active_parts), encoding="utf-8")
    VALIDATED_PATH.write_text("\n".join(validated_parts), encoding="utf-8")

    return stats


def main():
    dry_run = "--execute" not in sys.argv
    text = INSIGHT_PATH.read_text(encoding="utf-8")
    blocks = parse_insights(text)
    stats = compact(blocks, dry_run=dry_run)

    mode = "DRY RUN" if dry_run else "EXECUTED"
    print(f"=== Insight Compaction {mode} ===")
    print(f"Total insights:    {stats['total']}")
    print(f"  Validated:       {stats['validated']}")
    print(f"  Observation:     {stats['observation']}")
    print(f"  Fixing:          {stats['fixing']}")
    print(f"  Invalidated:     {stats['invalidated']}")
    print(f"  Other status:    {stats['other_status']}")
    print(f"---")
    print(f"Graduate (move):   {stats['graduate']} validated")
    print(f"Keep active:       {stats['keep_active']} observation/fixing/other")

    if dry_run:
        print("\nRun with --execute to apply.")


if __name__ == "__main__":
    main()
