"""Behavioral tests for the ADR/TDD product-boundary lint.

Unlike test_development_stage_contract.py (which asserts pinned routing —
not generated content), these tests assert the lint's judgment on actual
document *text*: a leaky sample must fail, a clean sample must pass. This is
the mechanical backstop for T12/P13, independent of any single agent's
self-read.

Each adversarial probe from review is captured as its own test so none can
silently regress. Two tests are intentionally inverted (`assertTrue(result.ok)`
with an explanatory docstring) — they document known, permanent limitations
of a lexical lint rather than pretend they are fixed.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts.adr_boundary_lint import (
    _load_source_texts,
    compute_evidence_digest,
    lint_adr_text,
    lint_tdd_text,
    main as lint_main,
    validate_finding_marker,
)

REQ_SENTENCE = (
    "REQ-07: one upload must produce all four required output schemas in a "
    "single pass so the analyst never has to re-upload the same file."
)

FEASIBILITY_EVIDENCE = (
    "Spec quote: the system shall let the analyst upload once and receive "
    "all four schema outputs without a second upload step."
)

CLEAN_ADR = f"""# ADR-014 — Single-pass multi-schema extraction boundary

| Field | Value |
|-------|-------|
| Status | Draft |
| product_constraints | `[REQ-07]` |
| changes_user_visible_behavior | false |
| spec_amendment_required | false |

## Product decisions excluded

- See REQ-07.

## Context

REQ-07 constrains the extraction boundary to a single read of the source
file. The open question is whether the parser emits one row stream consumed
by four independent mappers, or four independent parse passes over the same
buffer. Independent implementers could reasonably choose either shape, and
the choice is hard to reverse once downstream mappers depend on the row
contract, so it is recorded here rather than left to an implementation
detail.

## Options considered

| Option | Benefits | Costs / risks |
|--------|----------|---------------|
| A: single pass, map to 4 schemas | One I/O pass, lower latency | Mapper coupling to a shared intermediate row shape |
| B: four independent parse passes | Mapper isolation | 4x I/O cost, memory pressure on large files |

## Recommendation

Option A: `extract(file) -> map<schema, rows>` as the internal extraction
boundary, satisfying REQ-07 without amending it. This keeps the I/O cost
bounded to a single pass and pushes schema-specific mapping to a narrow,
independently testable layer.

## Consequences

- Mappers depend on a shared intermediate row shape; a schema change to one
  mapper's row expectations requires a compatibility check across all four.
- Adding a fifth schema means extending the shared row contract rather than
  writing an independent parser, which is the intended trade-off.

## Revisit triggers

- Source file sizes exceed the single-pass memory budget.
- A future schema requires a source layout the shared row contract cannot
  represent without breaking an existing mapper.
"""

ACCEPTED_ADR = CLEAN_ADR.replace(
    "| Status | Draft |",
    "| Status | Accepted |\n"
    "| Approval evidence | https://example.com/pr/1#review-1 |\n"
    "| Approved head | abc123 |\n"
    "| Lint evidence | adr_boundary_lint.py 2/2, PASS, sha256:deadbeef |",
)


def _replace_section(adr: str, heading: str, new_body: str) -> str:
    """Test helper: replace one '## heading' section's body in an ADR fixture."""
    pattern = re.compile(
        rf"(^##\s+{re.escape(heading)}\s*\n)(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub(lambda m: m.group(1) + new_body + "\n\n", adr, count=1)


class AdrBoundaryLintTest(unittest.TestCase):
    # ── Baseline ────────────────────────────────────────────────────────

    def test_clean_adr_passes(self) -> None:
        result = lint_adr_text(
            CLEAN_ADR,
            source_texts={"REQ-07": REQ_SENTENCE, "feasibility-evidence": FEASIBILITY_EVIDENCE},
        )
        self.assertTrue(result.ok, msg=f"unexpected violations: {result.violations}")
        self.assertEqual(result.violations, [])

    def test_accepted_adr_with_full_metadata_passes(self) -> None:
        result = lint_adr_text(ACCEPTED_ADR)
        self.assertTrue(result.ok, msg=f"unexpected violations: {result.violations}")

    def test_leaky_adr_fails_on_forbidden_phrasing(self) -> None:
        leaky = _replace_section(
            CLEAN_ADR,
            "Context",
            "The user can upload a file and the system will process it. "
            "Acceptance criteria require that the user should see all four "
            "outputs without a second upload, per REQ-07.",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(
            any("the user" in v or "user can" in v or "acceptance criteri" in v for v in result.violations),
        )

    def test_leaky_adr_fails_on_verbatim_overlap_with_req_and_evidence(self) -> None:
        leaky = _replace_section(
            CLEAN_ADR,
            "Context",
            f"{FEASIBILITY_EVIDENCE} {REQ_SENTENCE} This bounds the design per REQ-07.",
        )
        result = lint_adr_text(
            leaky,
            source_texts={"REQ-07": REQ_SENTENCE, "feasibility-evidence": FEASIBILITY_EVIDENCE},
        )
        self.assertFalse(result.ok)
        overlap_violations = [v for v in result.violations if "overlap" in v]
        self.assertTrue(overlap_violations)
        self.assertTrue(any("REQ-07" in v for v in overlap_violations))
        self.assertTrue(any("feasibility-evidence" in v for v in overlap_violations))

    def test_missing_req_citation_fails(self) -> None:
        no_citation = CLEAN_ADR.replace("REQ-07", "the constraint")
        result = lint_adr_text(no_citation)
        self.assertFalse(result.ok)
        self.assertTrue(any("no REQ-* id" in v for v in result.violations))

    def test_oversized_record_body_fails(self) -> None:
        padding = " ".join(["engineering"] * 500)
        oversized = _replace_section(
            CLEAN_ADR,
            "Consequences",
            "- Mappers depend on a shared intermediate row shape.\n"
            f"- {padding}",
        )
        result = lint_adr_text(oversized)
        self.assertFalse(result.ok)
        self.assertTrue(any("design-doc smell" in v for v in result.violations))

    # ── Round-2 adversarial probes (still guarded) ─────────────────────

    def test_probe_feature_prose_hidden_in_options_table(self) -> None:
        leaky = _replace_section(
            CLEAN_ADR,
            "Options considered",
            "| Option | Benefits | Costs / risks |\n"
            "|--------|----------|---------------|\n"
            "| A | The user can upload once and the user should never see a "
            "second prompt | None |\n",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(any("the user" in v or "user can" in v for v in result.violations))

    def test_probe_feature_prose_hidden_in_exclusions(self) -> None:
        leaky = _replace_section(
            CLEAN_ADR,
            "Product decisions excluded",
            "- Whether the user can upload more than one file at a time — see REQ-07.",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(any("the user" in v or "user can" in v for v in result.violations))

    def test_probe_feature_prose_hidden_in_revisit_triggers(self) -> None:
        leaky = _replace_section(
            CLEAN_ADR,
            "Revisit triggers",
            "- If the user should ever need to upload more than one file at once.",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(any("the user" in v or "user should" in v for v in result.violations))

    def test_probe_system_shall_prose(self) -> None:
        leaky = _replace_section(
            CLEAN_ADR,
            "Context",
            "The system shall extract all four schemas from a single uploaded "
            "file per REQ-07, and the parser shall not require a second read.",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(any("shall" in v for v in result.violations))

    def test_probe_tiny_record_bypasses_phrase_and_overlap_checks(self) -> None:
        tiny = """# ADR-014 — Extraction boundary

| Field | Value |
|-------|-------|
| Status | Draft |
| product_constraints | `[REQ-07]` |
| changes_user_visible_behavior | false |
| spec_amendment_required | false |

## Product decisions excluded

- See REQ-07.

## Context

Single pass per REQ-07.

## Options considered

| Option | Benefits | Costs |
|--------|----------|-------|
| A | x | y |

## Recommendation

Option A.

## Consequences

- None material.

## Revisit triggers

- None known.
"""
        result = lint_adr_text(tiny)
        self.assertFalse(result.ok)
        self.assertTrue(any("too thin" in v for v in result.violations))

    def test_probe_source_supplied_synonym_paraphrase(self) -> None:
        paraphrase = _replace_section(
            CLEAN_ADR,
            "Context",
            "A single submission will generate all four mandatory deliverable "
            "schemas in one pass, so the analyst is not forced to upload the "
            "same file twice, per REQ-07.",
        )
        result = lint_adr_text(paraphrase, source_texts={"REQ-07": REQ_SENTENCE})
        self.assertFalse(result.ok)
        self.assertTrue(any("paraphrase" in v or "lexical similarity" in v for v in result.violations))

    def test_probe_feature_in_title(self) -> None:
        leaky = CLEAN_ADR.replace(
            "# ADR-014 — Single-pass multi-schema extraction boundary",
            "# ADR-014 — Let the user upload once and get all outputs",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(any("the user" in v for v in result.violations))

    def test_probe_missing_options_section(self) -> None:
        no_options = re.sub(
            r"^## Options considered\n.*?(?=^## Recommendation)",
            "",
            CLEAN_ADR,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertNotIn("## Options considered", no_options)
        result = lint_adr_text(no_options)
        self.assertFalse(result.ok)
        self.assertTrue(any("missing required section: '## Options considered'" in v for v in result.violations))

    def test_probe_three_decisions_bundled_via_duplicate_sections(self) -> None:
        bundled = CLEAN_ADR.replace(
            "## Revisit triggers",
            "## Recommendation\n\n"
            "Option C: a completely separate second decision bundled into "
            "this file.\n\n"
            "## Revisit triggers",
            1,
        )
        result = lint_adr_text(bundled)
        self.assertFalse(result.ok)
        self.assertTrue(any("appears 2 times" in v for v in result.violations))

    def test_probe_accepted_adr_with_true_product_flag_fails(self) -> None:
        lying = CLEAN_ADR.replace("| Status | Draft |", "| Status | Accepted |").replace(
            "| changes_user_visible_behavior | false |",
            "| changes_user_visible_behavior | true |",
        )
        result = lint_adr_text(lying)
        self.assertFalse(result.ok)
        self.assertTrue(any("Accepted" in v and "changes_user_visible_behavior" in v for v in result.violations))

    def test_probe_fabricated_req_citation_outside_approved_set(self) -> None:
        invented = _replace_section(
            CLEAN_ADR,
            "Recommendation",
            "Send an email digest to the account owner every time extraction "
            "completes, per REQ-99.",
        ).replace("`[REQ-07]`", "`[REQ-07, REQ-99]`")
        result_without_approved_list = lint_adr_text(invented)
        result_with_approved_list = lint_adr_text(invented, approved_req_ids={"REQ-07"})
        self.assertTrue(
            result_without_approved_list.ok
            or not any("not in the supplied approved" in v for v in result_without_approved_list.violations),
        )
        self.assertFalse(result_with_approved_list.ok)
        self.assertTrue(any("REQ-99" in v for v in result_with_approved_list.violations))

    def test_probe_invented_behavior_with_false_flags_is_a_known_residual_gap(self) -> None:
        """A real, honest limitation: invented behavior under a correctly
        cited REQ, with metadata flags falsely left `false`, using no
        forbidden phrase and no supplied source overlap, cannot be caught
        lexically. Documents the gap rather than hiding it."""
        invented = _replace_section(
            CLEAN_ADR,
            "Recommendation",
            "Dispatch a weekly digest summary to the account owner once "
            "extraction completes, satisfying REQ-07 without amending it.",
        )
        result = lint_adr_text(invented, source_texts={"REQ-07": REQ_SENTENCE})
        self.assertTrue(result.ok)

    def test_probe_loose_semantic_paraphrase_outside_synonym_map_is_a_known_residual_gap(self) -> None:
        paraphrase = _replace_section(
            CLEAN_ADR,
            "Context",
            "The workflow converts an incoming artifact into every needed "
            "structured record type during one traversal, avoiding a second "
            "customer round-trip, per REQ-07.",
        )
        result = lint_adr_text(paraphrase, source_texts={"REQ-07": REQ_SENTENCE})
        self.assertTrue(result.ok)

    def test_require_sources_fails_when_none_supplied(self) -> None:
        result = lint_adr_text(CLEAN_ADR, require_sources=True)
        self.assertFalse(result.ok)
        self.assertEqual(result.sources_checked, 0)

    def test_sources_checked_is_reported(self) -> None:
        result = lint_adr_text(CLEAN_ADR, source_texts={"REQ-07": REQ_SENTENCE})
        self.assertEqual(result.sources_checked, 1)

    def test_finding_marker_validation(self) -> None:
        self.assertEqual(validate_finding_marker("ALTERNATIVE: sync vs async processing model"), [])
        malformed = validate_finding_marker(
            "One upload must produce all four schemas without a second upload."
        )
        self.assertTrue(malformed)
        self.assertTrue(any("ALTERNATIVE" in v for v in malformed))

        result = lint_adr_text(
            CLEAN_ADR,
            finding_text="One upload must produce all four schemas without a second upload.",
        )
        self.assertFalse(result.ok)
        self.assertTrue(any("ALTERNATIVE" in v for v in result.violations))

    # ── Round-4 adversarial probes (new) ────────────────────────────────

    def test_probe_unknown_heading_still_scanned_for_leakage(self) -> None:
        """'## Customer outcome' / '## User experience' are not in the
        required-sections list — they must still be scanned, and flagged as
        unrecognized, not silently ignored."""
        leaky = CLEAN_ADR.replace(
            "## Revisit triggers",
            "## Customer outcome\n\n"
            "The user gets all four outputs from a single upload.\n\n"
            "## Revisit triggers",
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok)
        self.assertTrue(any("unrecognized section" in v and "Customer outcome" in v for v in result.violations))
        self.assertTrue(any("the user" in v for v in result.violations))

    def test_probe_case_variant_heading_counted_as_duplicate(self) -> None:
        bundled = CLEAN_ADR.replace(
            "## Revisit triggers",
            "## context\n\nA second, differently-cased Context section.\n\n## Revisit triggers",
        )
        result = lint_adr_text(bundled)
        self.assertFalse(result.ok)
        self.assertTrue(
            any("Context" in v and "appears 2 times" in v for v in result.violations),
            msg=f"expected case-insensitive duplicate detection, got: {result.violations}",
        )

    def test_probe_empty_required_section_fails(self) -> None:
        empty_options = _replace_section(CLEAN_ADR, "Options considered", "")
        result = lint_adr_text(empty_options)
        self.assertFalse(result.ok)
        self.assertTrue(any("exists but is empty" in v and "Options considered" in v for v in result.violations))

    def test_probe_conflicting_metadata_fails(self) -> None:
        conflicting = CLEAN_ADR.replace(
            "| changes_user_visible_behavior | false |",
            "| changes_user_visible_behavior | false |\n"
            "| changes_user_visible_behavior | true |",
        )
        result = lint_adr_text(conflicting)
        self.assertFalse(result.ok)
        self.assertTrue(any("conflicting values" in v for v in result.violations))

    def test_probe_empty_source_file_does_not_satisfy_require_sources(self) -> None:
        result = lint_adr_text(CLEAN_ADR, source_texts={"blank.txt": "   \n\n  "}, require_sources=True)
        self.assertFalse(result.ok)
        self.assertEqual(result.sources_checked, 0)
        self.assertTrue(any("empty/whitespace-only" in v for v in result.violations))

    def test_probe_colliding_basenames_do_not_overwrite(self, tmp_path: Path | None = None) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            p1 = Path(d1) / "req.txt"
            p2 = Path(d2) / "req.txt"
            p1.write_text("alpha content unique to file one")
            p2.write_text("beta content unique to file two")
            loaded = _load_source_texts([str(p1), str(p2)])
            self.assertIsNotNone(loaded)
            self.assertEqual(len(loaded), 2, msg=f"expected 2 distinct sources, got: {loaded}")

    def test_probe_invalid_status_fails(self) -> None:
        invalid = CLEAN_ADR.replace("| Status | Draft |", "| Status | Banana |")
        result = lint_adr_text(invalid)
        self.assertFalse(result.ok)
        self.assertTrue(any("Status" in v and "Banana" in v for v in result.violations))

    def test_probe_malformed_title_fails(self) -> None:
        malformed = CLEAN_ADR.replace(
            "# ADR-014 — Single-pass multi-schema extraction boundary",
            "# Extraction boundary decision",
        )
        result = lint_adr_text(malformed)
        self.assertFalse(result.ok)
        self.assertTrue(any("does not match the required" in v for v in result.violations))

    def test_probe_accepted_missing_approval_evidence_fails(self) -> None:
        accepted_no_evidence = CLEAN_ADR.replace("| Status | Draft |", "| Status | Accepted |")
        result = lint_adr_text(accepted_no_evidence)
        self.assertFalse(result.ok)
        self.assertTrue(any("Approval evidence" in v for v in result.violations))
        self.assertTrue(any("Approved head" in v for v in result.violations))
        self.assertTrue(any("Lint evidence" in v for v in result.violations))

    def test_probe_accepted_missing_lint_evidence_fails(self) -> None:
        accepted_no_lint_evidence = ACCEPTED_ADR.replace(
            "| Lint evidence | adr_boundary_lint.py 2/2, PASS, sha256:deadbeef |", ""
        )
        result = lint_adr_text(accepted_no_lint_evidence)
        self.assertFalse(result.ok)
        self.assertTrue(any("Lint evidence" in v for v in result.violations))

    def test_probe_alternative_marker_bare_text_fails(self) -> None:
        violations = validate_finding_marker("ALTERNATIVE: sync")
        self.assertTrue(any("too short" in v for v in violations))

    def test_probe_alternative_marker_product_framed_fails(self) -> None:
        violations = validate_finding_marker("ALTERNATIVE: the user can upload once or twice")
        self.assertTrue(any("the user" in v for v in violations))

    def test_probe_tdd_problem_statement_leakage_detected(self) -> None:
        leaky_tdd = """# Technical Design Document — INIT-EXAMPLE

## 1. Problem statement

The user can upload a file once and the system shall generate all four
schema outputs, per REQ-07.
"""
        result = lint_tdd_text(leaky_tdd)
        self.assertFalse(result.ok)
        self.assertTrue(any("the user" in v or "shall" in v for v in result.violations))

    def test_probe_tdd_clean_problem_statement_passes(self) -> None:
        clean_tdd = """# Technical Design Document — INIT-EXAMPLE

## 1. Problem statement

REQ-07 requires a single-pass extraction boundary across four schema
mappers; the module boundary and row contract are undecided.
"""
        result = lint_tdd_text(clean_tdd)
        self.assertTrue(result.ok, msg=f"unexpected violations: {result.violations}")

    def test_probe_tdd_overlap_with_source_detected(self) -> None:
        leaky_tdd = f"""# Technical Design Document — INIT-EXAMPLE

## 1. Problem statement

{REQ_SENTENCE}
"""
        result = lint_tdd_text(leaky_tdd, source_texts={"REQ-07": REQ_SENTENCE})
        self.assertFalse(result.ok)
        self.assertTrue(any("overlap" in v for v in result.violations))

    # ── Round-5 fixes ────────────────────────────────────────────────────

    def test_probe_case_variant_metadata_field_no_longer_invisible(self) -> None:
        """Bug: the field-name regex was case-sensitive, so a case-variant
        row wasn't just unflagged for conflict — it was entirely invisible,
        letting a shadow 'Changes_User_Visible_Behavior: true' row coexist
        with a canonical 'changes_user_visible_behavior: false' row."""
        shadow_conflict = CLEAN_ADR.replace(
            "| changes_user_visible_behavior | false |",
            "| changes_user_visible_behavior | false |\n"
            "| Changes_User_Visible_Behavior | true |",
        )
        result = lint_adr_text(shadow_conflict)
        self.assertFalse(result.ok)
        self.assertTrue(any("conflicting values" in v for v in result.violations))

    def test_probe_tbd_and_dash_approval_placeholders_fail(self) -> None:
        for placeholder in ("TBD", "-", "N/A", "none", ""):
            with self.subTest(placeholder=placeholder):
                accepted = CLEAN_ADR.replace("| Status | Draft |", "| Status | Accepted |")
                if placeholder:
                    accepted = accepted.replace(
                        "## Product decisions excluded",
                        f"| Approval evidence | {placeholder} |\n\n## Product decisions excluded",
                    )
                result = lint_adr_text(accepted)
                self.assertFalse(result.ok, f"placeholder {placeholder!r} should not satisfy Approval evidence")
                self.assertTrue(any("Approval evidence" in v for v in result.violations))

    def test_probe_non_numeric_adr_id_fails(self) -> None:
        bad_id = CLEAN_ADR.replace(
            "# ADR-014 — Single-pass multi-schema extraction boundary",
            "# ADR-XYZ — Single-pass multi-schema extraction boundary",
        )
        result = lint_adr_text(bad_id)
        self.assertFalse(result.ok)
        self.assertTrue(any("does not match the required" in v for v in result.violations))

    def test_probe_leakage_in_acceptance_finalization_scaffolding_detected(self) -> None:
        # CLEAN_ADR fixture doesn't include the Lifecycle/Acceptance
        # finalization boilerplate — append a minimal version with leakage
        # to confirm scaffolding sections are scanned, not just skipped.
        leaky = CLEAN_ADR + (
            "\n## Lifecycle — Accepted immutability and supersession\n\n"
            "Once Accepted, do not rewrite in place.\n\n"
            "## Acceptance finalization\n\n"
            "The user will not notice any change once this ships.\n"
        )
        result = lint_adr_text(leaky)
        self.assertFalse(result.ok, "leakage inside scaffolding sections must still be caught")
        self.assertTrue(any("scaffolding" in v and "the user" in v for v in result.violations))

    def test_strict_mode_requires_the_full_bundle(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            adr_path = Path(d) / "adr-014.md"
            adr_path.write_text(CLEAN_ADR)
            # --strict with --source-text but no --approved-req-id / --finding-text-file
            req_path = Path(d) / "req.txt"
            req_path.write_text(REQ_SENTENCE)
            exit_code = lint_main([str(adr_path), "--strict", "--source-text", str(req_path)])
            self.assertEqual(exit_code, 1, "strict mode must fail without approved-req-id and finding-text-file")

    def test_strict_mode_passes_with_full_bundle(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            adr_path = Path(d) / "adr-014.md"
            adr_path.write_text(CLEAN_ADR)
            req_path = Path(d) / "req.txt"
            req_path.write_text(REQ_SENTENCE)
            finding_path = Path(d) / "finding.txt"
            finding_path.write_text("ALTERNATIVE: single pass vs four independent parses")
            exit_code = lint_main([
                str(adr_path), "--strict",
                "--source-text", str(req_path),
                "--approved-req-id", "REQ-07",
                "--finding-text-file", str(finding_path),
            ])
            self.assertEqual(exit_code, 0)

    def test_compute_evidence_digest_is_stable_and_source_sensitive(self) -> None:
        digest_a = compute_evidence_digest(CLEAN_ADR, {"REQ-07": REQ_SENTENCE})
        digest_b = compute_evidence_digest(CLEAN_ADR, {"REQ-07": REQ_SENTENCE})
        digest_c = compute_evidence_digest(CLEAN_ADR, {"REQ-07": "different text"})
        self.assertEqual(digest_a, digest_b, "same inputs must produce the same digest")
        self.assertNotEqual(digest_a, digest_c, "different sources must change the digest")

    def test_compute_evidence_digest_ignores_existing_lint_evidence_row(self) -> None:
        """The digest must be computed the same way whether the Lint evidence
        row already exists or not — otherwise writing the row would change
        the digest that's supposed to describe the row's own accuracy."""
        digest_before = compute_evidence_digest(CLEAN_ADR, None)
        with_row = CLEAN_ADR.replace(
            "| spec_amendment_required | false |",
            "| spec_amendment_required | false |\n"
            "| Lint evidence | adr_boundary_lint.py 0/0, PASS, sha256:whatever |",
        )
        digest_after = compute_evidence_digest(with_row, None)
        self.assertEqual(digest_before, digest_after)

    def test_verify_lint_evidence_detects_tampering(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            adr_path = Path(d) / "adr-014.md"
            req_path = Path(d) / "req.txt"
            req_path.write_text(REQ_SENTENCE)

            # _load_source_texts keys by resolved absolute path (fixing the
            # basename-collision bug) — the digest must be computed with the
            # same key main() will actually use, not an arbitrary label.
            genuine_digest = compute_evidence_digest(
                ACCEPTED_ADR, {str(req_path.resolve()): REQ_SENTENCE}
            )
            genuine = ACCEPTED_ADR.replace(
                "sha256:deadbeef", f"sha256:{genuine_digest}"
            )
            adr_path.write_text(genuine)
            ok_exit = lint_main([str(adr_path), "--source-text", str(req_path), "--verify-lint-evidence"])
            self.assertEqual(ok_exit, 0, "matching digest must verify clean")

            tampered = genuine.replace(
                "Single-pass multi-schema extraction boundary",
                "Single-pass multi-schema extraction boundary (edited after acceptance)",
            )
            adr_path.write_text(tampered)
            tampered_exit = lint_main([str(adr_path), "--source-text", str(req_path), "--verify-lint-evidence"])
            self.assertEqual(tampered_exit, 1, "content changed after the digest was recorded must fail verification")

    def test_tdd_sections_5_and_9_are_scanned(self) -> None:
        tdd = """# Technical Design Document — INIT-EXAMPLE

## 1. Problem statement

REQ-07 requires a single-pass extraction boundary.

## 5. Test policy

The user should never see inconsistent results between runs.

## 9. Resolved engineering decisions

| Finding ID | Owner | Status | Question | Resolution |
|---|---|---|---|---|
| C1 | PE | resolved | internal batching | the user can configure batch size |
"""
        result = lint_tdd_text(tdd)
        self.assertFalse(result.ok, "leakage in §5/§9 must be caught")
        self.assertTrue(any("the user" in v for v in result.violations))

    def test_tdd_section_10_is_deliberately_not_scanned(self) -> None:
        """§10 exists specifically to carry genuine product-scope language
        for PM routing — a phrase that appears ONLY there must not produce
        any violation, or the lint would permanently false-positive on the
        one section whose entire purpose is talking about user-facing
        choices."""
        clean_engineering_sections = """# Technical Design Document — INIT-EXAMPLE

## 1. Problem statement

REQ-07 requires a single-pass extraction boundary.

## 5. Test policy

Unit tests cover the row-mapping contract; integration tests cover the
end-to-end parse boundary.

## 9. Resolved engineering decisions

| Finding ID | Owner | Status | Question | Resolution |
|---|---|---|---|---|
| C1 | PE | resolved | internal batching | single in-memory buffer, no external queue |
"""
        with_leaky_pm_section = clean_engineering_sections + (
            "\n## 10. Routed out — product questions (PM)\n\n"
            "Should the user be able to configure batch size, or is that "
            "PE's call? This section exists to carry exactly this kind of "
            "question — it must not be flagged.\n"
        )
        baseline = lint_tdd_text(clean_engineering_sections)
        with_pm = lint_tdd_text(with_leaky_pm_section)
        self.assertTrue(baseline.ok, msg=f"unexpected violations: {baseline.violations}")
        self.assertEqual(
            baseline.violations,
            with_pm.violations,
            msg="adding §10 content must not change the violation set at all",
        )


if __name__ == "__main__":
    unittest.main()
