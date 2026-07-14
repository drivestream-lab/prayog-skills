from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).parent.parent


class WorkflowContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = yaml.safe_load((ROOT / "delivery-contract.yaml").read_text())
        cls.workflow = yaml.safe_load((ROOT / "workflow.yaml").read_text())
        cls.scenarios = json.loads(
            (ROOT / "tests" / "fixtures" / "workflow_scenarios.json").read_text()
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

    @staticmethod
    def _profile_skills(profile: str, key: str) -> set[str]:
        raw = yaml.safe_load((ROOT / "profiles" / f"{profile}.yaml").read_text())
        return set(raw[key])


if __name__ == "__main__":
    unittest.main()
