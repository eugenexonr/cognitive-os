"""Query decisions with filters. Works with both YAML frontmatter and legacy format.

Usage:
    python query_decisions.py                              # all decisions
    python query_decisions.py --status pending             # only pending
    python query_decisions.py --project MyProject             # by project
    python query_decisions.py --weight W4                  # by kernel weight
    python query_decisions.py --min-confidence 70          # high-confidence
    python query_decisions.py --has-depends                # with dependencies
    python query_decisions.py --needs-review               # dependency resolved
    python query_decisions.py --calibration                # confidence accuracy report

Reads both decisions.md and decisions-archive.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from compact_decisions import parse_blocks, propagate_staleness, Block

OS_ROOT = Path(__file__).resolve().parent.parent
DECISIONS_PATH = OS_ROOT / "decisions.md"
ARCHIVE_PATH = OS_ROOT / "decisions-archive.md"


def load_all_decisions() -> list[Block]:
    """Load decisions from active + archive files."""
    decisions = []

    for path in [DECISIONS_PATH, ARCHIVE_PATH]:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            blocks = parse_blocks(text)
            decisions.extend(b for b in blocks if b.kind == "decision")

    propagate_staleness(decisions)
    return decisions


def filter_decisions(
    decisions: list[Block],
    status: str | None = None,
    project: str | None = None,
    weight: str | None = None,
    min_confidence: int | None = None,
    max_confidence: int | None = None,
    has_depends: bool = False,
    needs_review: bool = False,
) -> list[Block]:
    result = decisions

    if status:
        if status == "pending":
            result = [d for d in result if d.outcome == "PENDING"]
        elif status == "resolved":
            result = [d for d in result if d.outcome == "resolved"]

    if project:
        needle = project.lower()
        result = [d for d in result if needle in d.project.lower()]

    if weight:
        result = [d for d in result if d.weight == weight]

    if min_confidence is not None:
        result = [d for d in result if d.confidence >= min_confidence]

    if max_confidence is not None:
        result = [d for d in result if 0 <= d.confidence <= max_confidence]

    if has_depends:
        result = [d for d in result if d.depends_on]

    if needs_review:
        result = [d for d in result if d.needs_review]

    return result


def print_table(decisions: list[Block]) -> None:
    """Print decisions as a readable table."""
    if not decisions:
        print("No matching decisions.")
        return

    print(f"{'ID':<6} {'Status':<10} {'Project':<20} {'W':<4} {'Conf':>4} {'Deps':<12} {'Title'}")
    print("-" * 90)
    for d in decisions:
        title = d.header.split(": ", 1)[-1][:35] if ": " in d.header else d.header[:35]
        # Remove classification tags from title
        import re
        title = re.sub(r"\s*\[.*?\]", "", title)
        status = d.outcome.lower()
        if d.pending_class:
            status = d.pending_class.lower()
        if d.needs_review:
            status += "*"
        deps = ",".join(d.depends_on) if d.depends_on else "-"
        conf = str(d.confidence) if d.confidence >= 0 else "?"
        print(f"{d.decision_id:<6} {status:<10} {d.project[:20]:<20} {d.weight:<4} {conf:>4} {deps:<12} {title}")

    print(f"\nTotal: {len(decisions)}")


def calibration_report(decisions: list[Block]) -> None:
    """Analyze prediction accuracy for resolved decisions with confidence."""
    resolved = [d for d in decisions if d.outcome == "resolved" and d.confidence >= 0]

    if len(resolved) < 3:
        print(f"Need at least 3 resolved decisions with confidence. Have: {len(resolved)}")
        return

    # Group by confidence bucket
    buckets = {"high (80%+)": [], "medium (50-79%)": [], "low (<50%)": []}
    for d in resolved:
        body = "\n".join(d.lines).lower()
        # Heuristic: if outcome mentions "wrong", "failed", "incorrect" → failed prediction
        failed = any(w in body for w in ["wrong", "failed", "incorrect", "partially wrong", "not as expected"])
        succeeded = not failed

        if d.confidence >= 80:
            buckets["high (80%+)"].append((d, succeeded))
        elif d.confidence >= 50:
            buckets["medium (50-79%)"].append((d, succeeded))
        else:
            buckets["low (<50%)"].append((d, succeeded))

    print("=== Calibration Report ===\n")
    for bucket_name, items in buckets.items():
        if not items:
            continue
        success_count = sum(1 for _, s in items if s)
        total = len(items)
        rate = success_count / total * 100
        print(f"{bucket_name}: {success_count}/{total} succeeded ({rate:.0f}%)")
        if bucket_name == "high (80%+)" and rate < 70:
            print("  ⚠ Over-confident pattern detected")
        if bucket_name == "low (<50%)" and rate > 70:
            print("  ⚠ Under-confident pattern detected")

    print(f"\nTotal resolved with confidence: {len(resolved)}")


def main():
    parser = argparse.ArgumentParser(description="Query Cognitive OS decisions")
    parser.add_argument("--status", choices=["pending", "resolved"])
    parser.add_argument("--project")
    parser.add_argument("--weight", help="Kernel weight (W0-W5)")
    parser.add_argument("--min-confidence", type=int)
    parser.add_argument("--max-confidence", type=int)
    parser.add_argument("--has-depends", action="store_true")
    parser.add_argument("--needs-review", action="store_true")
    parser.add_argument("--calibration", action="store_true", help="Show calibration report")
    args = parser.parse_args()

    decisions = load_all_decisions()

    if args.calibration:
        calibration_report(decisions)
        return

    filtered = filter_decisions(
        decisions,
        status=args.status,
        project=args.project,
        weight=args.weight,
        min_confidence=args.min_confidence,
        max_confidence=args.max_confidence,
        has_depends=args.has_depends,
        needs_review=args.needs_review,
    )

    print_table(filtered)


if __name__ == "__main__":
    main()
