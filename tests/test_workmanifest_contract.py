"""Deterministic WorkManifest contract validator tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.workmanifest_contract import (
    extract_declared_coverage,
    extract_workmanifest_yaml,
    validate_workmanifest,
    _valid_repo_path,
)


ROOT = Path(__file__).parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "workmanifest"


def _codes(errors: list[dict[str, str]]) -> set[str]:
    return {e["code"] for e in errors}


class WorkManifestContractTest(unittest.TestCase):
    def test_valid_fixture_passes(self) -> None:
        text = (FIXTURES / "valid.yaml").read_text(encoding="utf-8")
        errors = validate_workmanifest(text)
        self.assertEqual(errors, [])

    def test_valid_round_trip_mapping(self) -> None:
        data = yaml.safe_load((FIXTURES / "valid.yaml").read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        errors = validate_workmanifest(data)
        self.assertEqual(errors, [])
        self.assertEqual(data["apiVersion"], "prayog/v1")
        self.assertEqual(data["kind"], "WorkManifest")
        self.assertIn("depends_on", data["work"][0]["tasks"][1])
        self.assertIn("exit", data["work"][0]["tasks"][0])
        self.assertIn("verification", data["work"][0])

    def test_extract_from_plan_section(self) -> None:
        plan = (
            "# Plan\n\n"
            "## 9. WorkManifest seed\n\n"
            "```yaml\n"
            + (FIXTURES / "valid.yaml").read_text(encoding="utf-8")
            + "\n```\n\n"
            "## 10. Coding-readiness unlock\n\n"
            "note\n"
        )
        extracted = extract_workmanifest_yaml(plan)
        self.assertIsNotNone(extracted)
        errors = validate_workmanifest(plan)
        self.assertEqual(errors, [])

    def test_invalid_missing_dependency(self) -> None:
        text = (FIXTURES / "invalid_missing_dependency.yaml").read_text(encoding="utf-8")
        errors = validate_workmanifest(text)
        self.assertIn("depends_on_missing", _codes(errors))

    def test_invalid_cycle(self) -> None:
        text = (FIXTURES / "invalid_cycle.yaml").read_text(encoding="utf-8")
        errors = validate_workmanifest(text)
        self.assertIn("depends_on_cycle", _codes(errors))

    def test_invalid_path_action(self) -> None:
        text = (FIXTURES / "invalid_path_action.yaml").read_text(encoding="utf-8")
        codes = _codes(validate_workmanifest(text))
        self.assertIn("file_path", codes)
        self.assertIn("file_action", codes)

    def test_invalid_vague_exit(self) -> None:
        text = (FIXTURES / "invalid_vague_exit.yaml").read_text(encoding="utf-8")
        codes = _codes(validate_workmanifest(text))
        self.assertIn("exit_criteria_vague", codes)
        self.assertTrue(
            {"exit_proof_command", "exit_proof_expected", "exit_proof_evidence"} & codes
        )

    def test_invalid_missing_req(self) -> None:
        text = (FIXTURES / "invalid_missing_req.yaml").read_text(encoding="utf-8")
        self.assertIn("implements", _codes(validate_workmanifest(text)))

    def test_invalid_unit_as_live(self) -> None:
        text = (FIXTURES / "invalid_unit_as_live.yaml").read_text(encoding="utf-8")
        self.assertIn("unit_as_live", _codes(validate_workmanifest(text)))

    def test_invalid_missing_cleanup_stop(self) -> None:
        text = (FIXTURES / "invalid_missing_cleanup_stop.yaml").read_text(encoding="utf-8")
        codes = _codes(validate_workmanifest(text))
        self.assertIn("live_cleanup", codes)
        self.assertIn("live_stop_conditions", codes)

    def test_rejects_launchpad_identity(self) -> None:
        data = yaml.safe_load((FIXTURES / "valid.yaml").read_text(encoding="utf-8"))
        data["apiVersion"] = "launchpad/v1"
        errors = validate_workmanifest(data)
        self.assertIn("identity", _codes(errors))

    def test_rejects_mutable_status(self) -> None:
        data = yaml.safe_load((FIXTURES / "valid.yaml").read_text(encoding="utf-8"))
        data["work"][0]["status"] = "Backlog"
        errors = validate_workmanifest(data)
        self.assertIn("mutable_field", _codes(errors))

    def test_error_shape_is_structured(self) -> None:
        text = (FIXTURES / "invalid_cycle.yaml").read_text(encoding="utf-8")
        for err in validate_workmanifest(text):
            self.assertEqual(set(err), {"code", "message", "path"})
            self.assertTrue(err["code"])
            self.assertTrue(err["message"])

    def test_extract_declared_coverage_parses_marker(self) -> None:
        self.assertEqual(
            extract_declared_coverage("# prayog:covers: REQ-01, REQ-02\n"),
            ["REQ-01", "REQ-02"],
        )

    def test_extract_declared_coverage_none_when_absent(self) -> None:
        self.assertIsNone(extract_declared_coverage("no marker here\n"))

    def test_live_coverage_skipped_without_base_path(self) -> None:
        # Same fixture that passes today — omitting base_path must never add
        # a coverage-check error, even though the referenced file isn't
        # actually opened.
        text = (FIXTURES / "valid.yaml").read_text(encoding="utf-8")
        self.assertEqual(validate_workmanifest(text), [])

    def test_live_coverage_matches_when_marker_present(self) -> None:
        text = (FIXTURES / "valid.yaml").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            script = base / "tests" / "verify" / "verify_health.py"
            script.parent.mkdir(parents=True)
            script.write_text("# prayog:covers: REQ-01\nprint('PASS')\n")
            errors = validate_workmanifest(text, base_path=base)
            self.assertEqual(errors, [])

    def test_live_coverage_mismatch_when_marker_disjoint(self) -> None:
        text = (FIXTURES / "valid.yaml").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            script = base / "tests" / "verify" / "verify_health.py"
            script.parent.mkdir(parents=True)
            script.write_text("# prayog:covers: REQ-99\nprint('PASS')\n")
            errors = validate_workmanifest(text, base_path=base)
            self.assertIn("live_coverage_mismatch", _codes(errors))

    def test_live_coverage_no_marker_is_not_an_error(self) -> None:
        text = (FIXTURES / "valid.yaml").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            script = base / "tests" / "verify" / "verify_health.py"
            script.parent.mkdir(parents=True)
            script.write_text("print('PASS')  # no marker — legacy artifact\n")
            errors = validate_workmanifest(text, base_path=base)
            self.assertNotIn("live_coverage_mismatch", _codes(errors))

    # ------------------------------------------------------------------
    # _valid_repo_path  –  Next.js dynamic-route segment support
    # ------------------------------------------------------------------

    def test_valid_path_plain(self) -> None:
        self.assertTrue(_valid_repo_path("src/api/health.py"))
        self.assertTrue(_valid_repo_path("app/api/pravah/remote-operations/commands/[commandId]/route.ts"))
        self.assertTrue(_valid_repo_path("app/api/pravah/remote-operations/batches/[batchId]/route.ts"))
        self.assertTrue(_valid_repo_path("app/api/pravah/remote-operations/controls/[commandType]/route.ts"))

    def test_valid_nextjs_dynamic_segments(self) -> None:
        """[id], [...slug], and [[...slug]] are accepted."""
        self.assertTrue(_valid_repo_path("app/api/[commandId]/route.ts"))
        self.assertTrue(_valid_repo_path("app/pages/[...slug]/page.tsx"))
        self.assertTrue(_valid_repo_path("app/pages/[[...slug]]/page.tsx"))
        self.assertTrue(_valid_repo_path("src/[resource]/[action]/handler.ts"))

    def test_rejects_glob_wildcards(self) -> None:
        """Actual glob patterns must still fail."""
        self.assertFalse(_valid_repo_path("src/*.ts"))
        self.assertFalse(_valid_repo_path("src/file?.ts"))
        self.assertFalse(_valid_repo_path("src/[a-z].ts"))

    def test_rejects_malformed_bracket_segments(self) -> None:
        """Non-Next.js bracket forms are rejected."""
        self.assertFalse(_valid_repo_path("src/[.txt].py"))
        self.assertFalse(_valid_repo_path("src/[].ts"))
        self.assertFalse(_valid_repo_path("src/[123].ts"))  # starts with digit
        self.assertFalse(_valid_repo_path("src/[missing-close.ts"))

    def test_rejects_existing_security_violations(self) -> None:
        """Absolute paths, ~, and parent traversal remain rejected."""
        self.assertFalse(_valid_repo_path("/etc/passwd"))
        self.assertFalse(_valid_repo_path("~/secret/file"))
        self.assertFalse(_valid_repo_path("../etc/passwd"))
        self.assertFalse(_valid_repo_path("src/../etc/passwd"))

    def test_nextjs_paths_in_full_manifest(self) -> None:
        """A complete valid WorkManifest with Next.js dynamic-route paths passes."""
        text = (
            "apiVersion: prayog/v1\n"
            "kind: WorkManifest\n"
            "initiative: INIT-RO-001\n"
            "epic:\n"
            "  id: EPIC\n"
            "  repo: example-service\n"
            "  title: demo\n"
            "  codebase: example-service\n"
            "  spec_path: docs/specification/product/INIT-DEMO-001.md\n"
            "  verify_command: python tests/verify/verify_health.py\n"
            "work:\n"
            "  - id: W0\n"
            "    kind: issue\n"
            "    repo: example-service\n"
            "    title: W0\n"
            "    depends_on: []\n"
            "    codebase: example-service\n"
            "    spec_path: docs/specification/product/INIT-DEMO-001.md\n"
            "    verify_command: python tests/verify/verify_health.py\n"
            "    tasks:\n"
            "      - id: TASK-W0-01\n"
            "        implements: [REQ-01]\n"
            "        depends_on: []\n"
            "        files:\n"
            "          - path: app/api/pravah/remote-operations/commands/[commandId]/route.ts\n"
            "            action: create\n"
            "          - path: app/api/pravah/remote-operations/batches/[batchId]/route.ts\n"
            "            action: create\n"
            "          - path: app/api/pravah/remote-operations/controls/[commandType]/route.ts\n"
            "            action: modify\n"
            "        exit:\n"
            "          criteria:\n"
            "            - 'API endpoints return expected responses'\n"
            "          proof:\n"
            "            kind: command\n"
            '            command: "pytest tests/unit/test_routes.py -q"\n'
            '            expected: "exit 0"\n'
            '            evidence_expected: "Wave-Execution-INIT-DEMO-001-W0.md § TASK-W0-01"\n'
            "    verification:\n"
            '      check: "make check"\n'
            '      unit: "pytest tests/unit -q"\n'
            "      live:\n"
            "        applicable: true\n"
            "        mode: smoke\n"
            "        command: python tests/verify/verify_health.py\n"
            "        covers: [REQ-01]\n"
            "        prerequisites:\n"
            '          - "Local stack up"\n'
            "        safe_test_data:\n"
            '          - "no durable tenant mutation"\n'
            "        steps:\n"
            '          - "Run verify"\n'
            "        expected_observations:\n"
            '          - "Script exits 0"\n'
            '        evidence_expected: "wave-accepted on tip"\n'
            "        cleanup:\n"
            '          - "No durable resources"\n'
            "        stop_conditions:\n"
            '          - "Non-zero exit → stop"\n'
        )
        errors = validate_workmanifest(text)
        self.assertEqual(errors, [])

    def test_invalid_glob_paths_still_fail(self) -> None:
        """Globs in a manifest must still produce file_path errors."""
        text = (
            "apiVersion: prayog/v1\n"
            "kind: WorkManifest\n"
            "initiative: INIT-DEMO-001\n"
            "epic:\n"
            "  id: EPIC\n"
            "  repo: example-service\n"
            "  title: demo\n"
            "  codebase: example-service\n"
            "  spec_path: docs/specification/product/INIT-DEMO-001.md\n"
            "  verify_command: python tests/verify/verify_health.py\n"
            "work:\n"
            "  - id: W0\n"
            "    kind: issue\n"
            "    repo: example-service\n"
            "    title: W0\n"
            "    depends_on: []\n"
            "    codebase: example-service\n"
            "    spec_path: docs/specification/product/INIT-DEMO-001.md\n"
            "    verify_command: python tests/verify/verify_health.py\n"
            "    tasks:\n"
            "      - id: TASK-W0-01\n"
            "        implements: [REQ-01]\n"
            "        depends_on: []\n"
            "        files:\n"
            "          - path: src/*.ts\n"
            "            action: create\n"
            "        exit:\n"
            "          criteria:\n"
            "            - 'Test passes'\n"
            "          proof:\n"
            "            kind: command\n"
            '            command: "pytest -q"\n'
            '            expected: "exit 0"\n'
            '            evidence_expected: "Wave-Execution-INIT-DEMO-001-W0.md § TASK-W0-01"\n'
            "    verification:\n"
            '      check: "make check"\n'
            '      unit: "pytest -q"\n'
            "      live:\n"
            "        applicable: true\n"
            "        mode: smoke\n"
            "        command: python tests/verify/verify_health.py\n"
            "        covers: [REQ-01]\n"
            "        prerequisites:\n"
            '          - "Local stack up"\n'
            "        safe_test_data:\n"
            '          - "no durable tenant mutation"\n'
            "        steps:\n"
            '          - "Run verify"\n'
            "        expected_observations:\n"
            '          - "Script exits 0"\n'
            '        evidence_expected: "wave-accepted on tip"\n'
            "        cleanup:\n"
            '          - "No durable resources"\n'
            "        stop_conditions:\n"
            '          - "Non-zero exit → stop"\n'
        )
        errors = validate_workmanifest(text)
        codes = _codes(errors)
        self.assertIn("file_path", codes)


if __name__ == "__main__":
    unittest.main()
