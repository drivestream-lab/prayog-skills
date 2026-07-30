# For Launchpad

Orientation for harness / materialize maintainers. Normative lists live in
prayog `profiles/*.yaml` and `delivery-contract.yaml` — this page does not fork
them.

## What launchpad must do

1. Pin `prayog-skills` at the programme `skills[].ref` / `agent_skills.ref`.
2. Resolve skill names from the profile:
   - meta: `requirements_skills` + **`forge_skills`**
   - app: `development_skills` + **`forge_skills`**
3. Materialize sources from `skills/{requirements|development|forge}/<name>/`.
4. Fail closed if a listed skill lacks `SKILL.md` at the pin.
5. Seed AGENTS slash list from the same combined name list.
6. Bind `review_roles` by **checkpoint node id** from the pinned delivery
   contract (ids ≡ purpose where renamed).

## Current pin expectations (rc-2 family)

| Topic | Expectation |
|-------|-------------|
| Forge trio | `commit-workspace`, `open-draft-pr`, `create-board-tickets` on every profile `forge_skills` |
| Board seeding | **No** content `board-seed`; humans use `/create-board-tickets` |
| Learning | App profiles include **`learning-extract`** |
| Checkpoints | `prd-impact-acceptance`, `coding-readiness` (not `gate-1` / `gate-2`) |
| Labels | Unchanged: `impact-map-*`, `spec-*` |
| WorkManifest | Launchpad **materializes** the pin only — it does **not** own, parse, or execute WorkManifest. Prayog owns the contract; Gateflow/humans validate and project it. |

## Pass-1 / Pass-2 (copy for playbooks)

```text
Pass-1:  /pre-implement → /loop-spec → wave-pr-action → live-verify (human)
Pass-2:  /learning-extract → /ground-spec → wave-signoff
```

Do not document orchestrated auto-verify/ground after `loop-spec`.
Do not materialize a merge Forge skill — wave merge is human-only.

## Partner handoff

Share [for-launchpad.md](for-launchpad.md) with the launchpad team when the pin
lands (they track fixture/`review_roles`/materialize changes on their side).
Launchpad **0.5.24** already aligns with this pin slice.


- Implementing Gateflow Enter-at or learning DB
- Putting forge skills on workflow `outcomes`
- Confusing kit **forge templates** (`apply-forge-templates`) with **forge skills**
