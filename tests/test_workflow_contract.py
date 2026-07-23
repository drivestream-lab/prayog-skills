from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).parent.parent
DISPATCH_ENUM = frozenset({"manual", "orchestrated"})


class WorkflowContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = yaml.safe_load((ROOT / "delivery-contract.yaml").read_text())
        cls.workflow = yaml.safe_load((ROOT / "workflow.yaml").read_text())
        cls.scenarios = json.loads(
            (ROOT / "tests" / "fixtures" / "workflow_scenarios.json").read_text()
        )
        cls.policy = json.loads(
            (ROOT / "tests" / "fixtures" / "workflow_dispatch_policy.json").read_text()
        )

    def test_contract_and_workflow_identity_match(self) -> None:
        expected = f"{self.contract['id']}/v{self.contract['version']}"
        self.assertEqual(expected, self.workflow["contract"])
        self.assertEqual(self.contract["workflow"], "workflow.yaml")

    def test_all_transitions_target_existing_nodes(self) -> None:
        nodes = self.workflow["nodes"]
        for stage, node in nodes.items():
            for outcome, target in (node.get("outcomes") or {}).items():
                with self.subTest(stage=stage, outcome=outcome):
                    self.assertIn(target, nodes)

    def test_skill_nodes_exist_and_emit_handoffs(self) -> None:
        profile_skills = {
            "meta-pm": self._profile_skills("meta-pm", "requirements_skills"),
            "development": self._profile_skills("python-backend", "development_skills"),
        }
        buckets = {"meta-pm": "requirements", "development": "development"}

        for stage, node in self.workflow["nodes"].items():
            if node["type"] != "skill":
                continue
            profile = node["profile"]
            with self.subTest(stage=stage):
                self.assertIn(stage, profile_skills[profile])
                skill_file = ROOT / "skills" / buckets[profile] / stage / "SKILL.md"
                self.assertTrue(skill_file.is_file())
                self.assertIn("## Workflow handoff", skill_file.read_text())

    def test_scenario_routes(self) -> None:
        nodes = self.workflow["nodes"]
        for scenario in self.scenarios:
            with self.subTest(scenario=scenario["name"]):
                actual = nodes[scenario["stage"]]["outcomes"][scenario["outcome"]]
                self.assertEqual(scenario["next"], actual)

    def test_skill_nodes_have_valid_dispatch(self) -> None:
        for stage, node in self.workflow["nodes"].items():
            with self.subTest(stage=stage):
                if node["type"] == "skill":
                    self.assertIn("dispatch", node)
                    self.assertIn(node["dispatch"], DISPATCH_ENUM)
                else:
                    self.assertNotIn("dispatch", node)

    def test_dispatch_matches_policy_fixture(self) -> None:
        orchestrated = set(self.policy["orchestrated"])
        manual = set(self.policy["manual"])
        self.assertFalse(orchestrated & manual)
        skill_nodes = {
            stage
            for stage, node in self.workflow["nodes"].items()
            if node["type"] == "skill"
        }
        self.assertEqual(skill_nodes, orchestrated | manual)
        for stage, node in self.workflow["nodes"].items():
            if node["type"] != "skill":
                continue
            expected = "orchestrated" if stage in orchestrated else "manual"
            with self.subTest(stage=stage):
                self.assertEqual(node["dispatch"], expected)

    def test_human_checkpoints_have_purpose(self) -> None:
        expected = self.policy["human_checkpoint_purposes"]
        checkpoints = {
            stage: node
            for stage, node in self.workflow["nodes"].items()
            if node["type"] == "human-checkpoint"
        }
        self.assertEqual(set(checkpoints), set(expected))
        for stage, node in checkpoints.items():
            with self.subTest(stage=stage):
                self.assertNotEqual(node.get("type"), "gate")
                purpose = node.get("purpose")
                self.assertIsInstance(purpose, str)
                self.assertTrue(purpose.strip())
                self.assertEqual(purpose, expected[stage])

    def test_no_gate_node_type(self) -> None:
        for stage, node in self.workflow["nodes"].items():
            with self.subTest(stage=stage):
                self.assertNotEqual(node.get("type"), "gate")

    def test_contract_documents_dispatch(self) -> None:
        dispatch = self.contract.get("dispatch") or {}
        self.assertEqual(set(dispatch.get("enum") or []), DISPATCH_ENUM)
        self.assertEqual(dispatch.get("schema_default"), "manual")
        self.assertIn(
            "invocation-mode-is-not-an-exemption",
            self.contract.get("principles") or [],
        )
        hc = self.contract.get("human_checkpoint") or {}
        self.assertEqual(hc.get("required_field"), "purpose")
        self.assertEqual(hc.get("mechanism"), "human-checkpoint")

    @staticmethod
    def _profile_skills(profile: str, key: str) -> set[str]:
        raw = yaml.safe_load((ROOT / "profiles" / f"{profile}.yaml").read_text())
        return set(raw[key])


if __name__ == "__main__":
    unittest.main()
