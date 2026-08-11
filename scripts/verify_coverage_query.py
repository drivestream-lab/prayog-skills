#!/usr/bin/env python3
"""Live-verify coverage query tool (read-only, stdout only).

Scans a `live_verify_dir` for the `prayog:covers:` marker
(see references/live-verify-coverage-contract.md) and answers "what already
covers this" — a computed view over self-declared, per-artifact facts, never
a stored/committed listing. There is no `--write` mode and none should ever
be added: the whole point is that nothing here needs to be kept in sync by
hand, the way `tests/README.md` used to.

CLI:
  python scripts/verify_coverage_query.py <live_verify_dir> --req REQ-01
  python scripts/verify_coverage_query.py <live_verify_dir> --capability tenant-registry
  python scripts/verify_coverage_query.py <live_verify_dir> --wave "INIT-X:W3"
  python scripts/verify_coverage_query.py <live_verify_dir> --dump

Import:
  from scripts.verify_coverage_query import scan_coverage
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from scripts.workmanifest_contract import extract_declared_coverage

# Deliberately broad — a live-verify artifact may be any stack's script or a
# markdown runbook. Skip obvious non-candidates only.
SKIP_DIR_NAMES = frozenset({"__pycache__", "node_modules", ".git"})


@dataclass(frozen=True)
class CoverageEntry:
    path: str
    covers: list[str] | None  # None = no marker found (not an error)


def scan_coverage(live_verify_dir: str | Path) -> list[CoverageEntry]:
    """Scan every file under ``live_verify_dir`` for the coverage marker.

    Returns one entry per file, including files with no marker (``covers is
    None``) — callers decide what "no evidence yet" means for their use
    case; this function never fails closed on an unmarked legacy artifact."""
    root = Path(live_verify_dir)
    entries: list[CoverageEntry] = []
    if not root.is_dir():
        return entries
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        entries.append(
            CoverageEntry(path=str(path.relative_to(root)), covers=extract_declared_coverage(text))
        )
    return entries


def _matches_req(entry: CoverageEntry, req: str) -> bool:
    return bool(entry.covers) and req in entry.covers


def _matches_keyword(entry: CoverageEntry, keyword: str, root: Path) -> bool:
    """Best-effort substring match against path + file content.

    Only `--req` is a structured match against the marker; `--capability`
    and `--wave` have no dedicated marker field today, so this is a
    heuristic, not a guarantee — stated plainly rather than pretending
    otherwise."""
    needle = keyword.lower()
    if needle in entry.path.lower():
        return True
    try:
        text = (root / entry.path).read_text(encoding="utf-8").lower()
    except (OSError, UnicodeDecodeError):
        return False
    return needle in text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("live_verify_dir", type=Path, help="Directory to scan")
    parser.add_argument("--req", help="Exact REQ-* id to match against the self-declared marker")
    parser.add_argument(
        "--capability",
        help="Best-effort keyword match against file path/content (not a structured field)",
    )
    parser.add_argument(
        "--wave",
        help="Best-effort keyword match against file path/content (not a structured field)",
    )
    parser.add_argument("--dump", action="store_true", help="List every scanned artifact, no filter")
    parser.add_argument("--json", action="store_true", help="Emit results as JSON")
    args = parser.parse_args(argv)

    if not args.live_verify_dir.is_dir():
        print(f"error: not a directory: {args.live_verify_dir}", file=sys.stderr)
        return 2

    entries = scan_coverage(args.live_verify_dir)

    if not (args.dump or args.req or args.capability or args.wave):
        print("error: pass --req, --capability, --wave, or --dump", file=sys.stderr)
        return 2

    if not args.dump:
        if args.req:
            entries = [e for e in entries if _matches_req(e, args.req)]
        if args.capability:
            entries = [e for e in entries if _matches_keyword(e, args.capability, args.live_verify_dir)]
        if args.wave:
            entries = [e for e in entries if _matches_keyword(e, args.wave, args.live_verify_dir)]

    if args.json:
        print(json.dumps([{"path": e.path, "covers": e.covers} for e in entries], indent=2))
        return 0

    if not entries:
        print("No matches.")
        return 0

    for entry in entries:
        covers = ", ".join(entry.covers) if entry.covers else "(no marker — legacy artifact)"
        print(f"{entry.path} — covers {covers}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
