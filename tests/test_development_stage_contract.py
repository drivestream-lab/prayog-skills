"""Deterministic contract-policy tests for development stage outcomes.

These fixtures assert pinned workflow navigation and checkpoint/action flags
for declared evidence → outcome mappings. They are not a behavioral guarantee
that every LLM run will classify evidence correctly.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).parent.parent


class DevelopmentStageContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = yaml.safe_load((ROOT / "workflow.yaml").read_text())
        cls.scenarios = json.loads(
            (ROOT / "tests" / "fixtures" / "development_stage_scenarios.json").read_text()
        )
        cls.nodes = cls.workflow["nodes"]

    def test_scenario_routes_and_flags(self) -> None:
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario["name"]):
                stage = scenario["stage"]
                outcome = scenario["outcome"]
                self.assertIn(stage, self.nodes)
                node = self.nodes[stage]
                outcomes = node.get("outcomes") or {}
                self.assertIn(outcome, outcomes)
                next_id = outcomes[outcome]
                self.assertEqual(scenario["next"], next_id)

                next_node = self.nodes[next_id]
                human = next_node.get("type") == "human-checkpoint"
                external = next_node.get("type") == "external-action"
                self.assertEqual(scenario["human_checkpoint"], human)
                self.assertEqual(scenario["external_action"], external)

                blockers = scenario.get("blockers") or []
                for blocker in blockers:
                    self.assertFalse(
                        blocker.isdigit(),
                        f"{scenario['name']}: bare numeric blocker {blocker!r}",
                    )
                    self.assertNotRegex(
                        blocker,
                        r"^F-\d+$",
                        f"{scenario['name']}: bare F-* check id {blocker!r}",
                    )

    def test_feasibility_pm_cannot_reach_technical_review(self) -> None:
        scenario = next(
            s for s in self.scenarios if s["name"] == "feasibility-pm-blocker-needs-input"
        )
        self.assertEqual(scenario["outcome"], "needs-input")
        self.assertNotEqual(scenario["next"], "spec-technical-review")

    def test_pe_finding_cannot_skip_to_plan(self) -> None:
        scenario = next(
            s for s in self.scenarios if s["name"] == "feasibility-pe-finding"
        )
        self.assertEqual(scenario["outcome"], "findings")
        self.assertEqual(scenario["next"], "spec-technical-review")
        self.assertNotEqual(scenario["next"], "spec-implementation-plan")

    def test_product_leakage_cannot_pass(self) -> None:
        for name in (
            "adr-invents-unapproved-behavior-needs-input",
            "adr-quality-leakage-findings",
        ):
            scenario = next(s for s in self.scenarios if s["name"] == name)
            self.assertNotEqual(scenario["outcome"], "pass")
            # Technical-review-native findings (T12 audit results) use TF-*,
            # never feasibility-owned FF-* (see id-conventions.md).
            self.assertTrue(any(b.startswith("TF-") for b in scenario["blockers"]))

    def test_missing_product_approval_routes_needs_input_not_findings(self) -> None:
        """A T12 FAIL because the ADR depends on behavior absent from any
        approved REQ-* is a missing-product-input gap (spec amendment
        required), matching the SKILL.md rubric row for `needs-input`
        ("product behavior missing from approved REQs") — not `findings`,
        which is reserved for engineering-quality gaps PE can resolve without
        a spec amendment."""
        invents_behavior = next(
            s
            for s in self.scenarios
            if s["name"] == "adr-invents-unapproved-behavior-needs-input"
        )
        self.assertEqual(invents_behavior["outcome"], "needs-input")

        quality_gap = next(
            s for s in self.scenarios if s["name"] == "adr-quality-leakage-findings"
        )
        self.assertEqual(quality_gap["outcome"], "findings")

    def test_ground_findings_use_gf_namespace(self) -> None:
        scenario = next(s for s in self.scenarios if s["name"] == "grounding-findings")
        self.assertTrue(all(b.startswith("GF-") for b in scenario["blockers"]))

    def test_technical_review_findings_use_tf_namespace_not_ff(self) -> None:
        """Technical-review-native findings (a T-check FAIL discovered while
        drafting/auditing the TDD/ADR) must use TF-*, not the feasibility-owned
        FF-* namespace — see id-conventions.md Process ids / Rules."""
        for name in (
            "adr-invents-unapproved-behavior-needs-input",
            "adr-quality-leakage-findings",
        ):
            scenario = next(s for s in self.scenarios if s["name"] == name)
            self.assertTrue(all(b.startswith("TF-") for b in scenario["blockers"]))
            self.assertFalse(any(b.startswith("FF-") for b in scenario["blockers"]))


if __name__ == "__main__":
    unittest.main()
