"""Live-verify coverage query tool tests — read-only scan, never a write path."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.verify_coverage_query import scan_coverage


class VerifyCoverageQueryTest(unittest.TestCase):
    def _make_fixture_dir(self, tmp: str) -> Path:
        root = Path(tmp)
        (root / "01-tenant-create.py").write_text(
            "# prayog:covers: REQ-03, REQ-04\nprint('PASS')\n"
        )
        (root / "02-legacy-smoke.md").write_text(
            "# Verify: legacy smoke\nNo marker on this one yet.\n"
        )
        (root / "03-webhook-ingress.md").write_text(
            "<!-- prayog:covers: REQ-08 -->\n# Verify: webhook ingress\n"
        )
        return root

    def test_scan_returns_one_entry_per_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_fixture_dir(tmp)
            entries = scan_coverage(root)
            self.assertEqual(len(entries), 3)

    def test_scan_finds_marker_in_code_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_fixture_dir(tmp)
            entries = {e.path: e.covers for e in scan_coverage(root)}
            self.assertEqual(entries["01-tenant-create.py"], ["REQ-03", "REQ-04"])

    def test_scan_finds_marker_in_markdown_html_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_fixture_dir(tmp)
            entries = {e.path: e.covers for e in scan_coverage(root)}
            self.assertEqual(entries["03-webhook-ingress.md"], ["REQ-08"])

    def test_scan_no_marker_is_none_not_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_fixture_dir(tmp)
            entries = {e.path: e.covers for e in scan_coverage(root)}
            self.assertIsNone(entries["02-legacy-smoke.md"])

    def test_scan_missing_dir_returns_empty_not_an_error(self) -> None:
        self.assertEqual(scan_coverage("/does/not/exist"), [])

    def test_scan_never_writes_anything(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_fixture_dir(tmp)
            before = sorted(p.name for p in root.iterdir())
            scan_coverage(root)
            after = sorted(p.name for p in root.iterdir())
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
