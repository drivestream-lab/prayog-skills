from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.prompt_contract import (
    SHARED_VARIABLES,
    extract_template_vars,
    is_semver,
    iter_prompt_skill_dirs,
    normalize_text,
    render,
    validate_bound_inputs,
    validate_prompt_package,
    validate_schema,
    validate_template,
)


ROOT = Path(__file__).parent.parent
INVENTORY = ROOT / "tests" / "fixtures" / "prompt_inventory.json"


class PromptContractUnitTest(unittest.TestCase):
    def test_semver(self) -> None:
        self.assertTrue(is_semver("1.0.0"))
        self.assertTrue(is_semver("0.5.2"))
        self.assertFalse(is_semver("1.0"))
        self.assertFalse(is_semver("v1.0.0"))

    def test_render_and_normalize(self) -> None:
        template = "Hello {{ ticket }} / {{initiative}}!\n\n"
        rendered = render(
            template,
            {"ticket": "T-1", "initiative": "", "handoff_path": "x"},
        )
        self.assertEqual(normalize_text(rendered), "Hello T-1 / !")

    def test_extract_and_undeclared(self) -> None:
        template = "Use {{workspace}} and {{unknown}}"
        self.assertEqual(extract_template_vars(template), ["workspace", "unknown"])
        errors = validate_template(template, {"workspace": {"required": True}})
        self.assertTrue(any("undeclared" in e for e in errors))

    def test_forbidden_template_syntax(self) -> None:
        errors = validate_template("{{ticket|upper}}", dict(SHARED_VARIABLES))
        self.assertTrue(errors)

    def test_normative_schema_defaults(self) -> None:
        schema = {
            "prompt_id": "ground-spec",
            "revision": "1.0.0",
            "variables": {
                name: {"required": spec["required"], "type": spec["type"]}
                for name, spec in SHARED_VARIABLES.items()
            },
        }
        self.assertEqual(validate_schema(schema, expected_prompt_id="ground-spec"), [])
        bad = dict(schema)
        bad["variables"] = dict(schema["variables"])
        bad["variables"]["ticket"] = {"required": False, "type": "string"}
        self.assertTrue(validate_schema(bad, expected_prompt_id="ground-spec"))

    def test_required_bound_inputs(self) -> None:
        errors = validate_bound_inputs(
            SHARED_VARIABLES,
            {
                "ticket": "",
                "initiative": "",
                "handoff_path": "h",
                "workspace": "w",
                "meta_workspace": "",
                "skill_id": "ground-spec",
            },
        )
        self.assertTrue(any("ticket" in e for e in errors))


class PromptPackageInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
        cls.expected = {
            (e["area"], e["skill_id"]) for e in cls.inventory["skills"]
        }

    def test_inventory_count_and_areas(self) -> None:
        self.assertEqual(len(self.expected), 18)
        areas = {area for area, _ in self.expected}
        self.assertEqual(areas, {"requirements", "development", "forge"})
        self.assertFalse(any(a == "engg-reviews" for a, _ in self.expected))

    def test_inventory_matches_directories(self) -> None:
        found = {
            (area, skill_id) for area, skill_id, _ in iter_prompt_skill_dirs(ROOT)
        }
        self.assertEqual(self.expected, found)

    def test_inventory_independent_of_dispatch_fixture(self) -> None:
        # Coverage must not be derived from dispatch policy membership alone.
        # Content skills match dispatch nodes; forge skills are extra (not on graph).
        policy = json.loads(
            (ROOT / "tests" / "fixtures" / "workflow_dispatch_policy.json").read_text(
                encoding="utf-8"
            )
        )
        dispatch_skills = set(policy["manual"]) | set(policy["orchestrated"])
        inventory_skills = {skill_id for _, skill_id in self.expected}
        content_inventory = {
            skill_id
            for area, skill_id in self.expected
            if area in {"requirements", "development"}
        }
        self.assertEqual(content_inventory, dispatch_skills)
        forge_skills = {
            skill_id for area, skill_id in self.expected if area == "forge"
        }
        self.assertEqual(
            forge_skills,
            {"commit-workspace", "open-draft-pr", "create-board-tickets"},
        )
        self.assertTrue(forge_skills.isdisjoint(dispatch_skills))
        self.assertEqual(inventory_skills, content_inventory | forge_skills)

    def test_every_package_valid(self) -> None:
        for area, skill_id, skill_root in iter_prompt_skill_dirs(ROOT):
            with self.subTest(skill=f"{area}/{skill_id}"):
                errors = validate_prompt_package(skill_root, skill_id=skill_id)
                self.assertEqual(errors, [], msg=errors)


if __name__ == "__main__":
    unittest.main()
