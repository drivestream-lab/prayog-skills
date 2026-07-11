from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.handoff_contract import EFFECTIVE_STATES, RIPPLE_ACTIONS, effective_state, ripple_actions


ROOT = Path(__file__).parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "handoff_scenarios.json"


class HandoffContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_effective_state_scenarios(self) -> None:
        for scenario in self.scenarios["state_scenarios"]:
            with self.subTest(scenario=scenario["name"]):
                actual = effective_state(
                    current_head_sha=scenario["current_head_sha"],
                    current_prd_digest=scenario["current_prd_digest"],
                    artifact=scenario["artifact"],
                    approvals=scenario["approvals"],
                    blocked=scenario.get("blocked", False),
                    superseded=scenario.get("superseded", False),
                )
                self.assertIn(actual, EFFECTIVE_STATES)
                self.assertEqual(scenario["expected"], actual)

    def test_ripple_scenarios(self) -> None:
        for scenario in self.scenarios["ripple_scenarios"]:
            with self.subTest(scenario=scenario["name"]):
                actual = ripple_actions(
                    previous=scenario["previous"],
                    current=scenario["current"],
                    in_flight=scenario.get("in_flight", "none"),
                    dependency_order_changed=scenario.get("dependency_order_changed", False),
                )
                self.assertTrue(set(actual) <= RIPPLE_ACTIONS)
                self.assertEqual(scenario["expected"], actual)


if __name__ == "__main__":
    unittest.main()
