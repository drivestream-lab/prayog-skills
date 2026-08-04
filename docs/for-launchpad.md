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
| Purge (initiative closure) | App profiles include **`purge-initiative-artifacts-app`**; meta profile includes **`purge-initiative-artifacts-meta`** |
| Checkpoints | `prd-impact-acceptance`, `coding-readiness`, `initiative-closure-signoff-app`, `initiative-closure-signoff-meta` (not `gate-1` / `gate-2`) |
| Labels | Unchanged: `impact-map-*`, `spec-*` |
| WorkManifest | Launchpad **materializes** the pin only — it does **not** own, parse, or execute WorkManifest. Prayog owns the contract; Gateflow/humans validate and project it. Board is long-term WM home after seed; plan §9 is walk-time. |
| External-action auth | Pin may set `authorization: automated` on `spec-pr-action` / `wave-pr-action` / `initiative-closure-pr-action-app` / `initiative-closure-pr-action-meta` / `wave-in-progress-action` / `wave-done-action`. Playbooks should not require a human `/open-draft-pr` click for those nodes when remounted on this tip. |
| KEEP/PURGE | Declared in `references/artifact-write-contract.md` — Launchpad does not implement purge logic |
| Board status | Pin nodes `wave-in-progress-action` / `wave-done-action` (`update_board_status`). **Do not** materialize a human `/update-board-status` skill — orch ForgeClient only. |

## Pass-1 / Pass-2 / closure (copy for playbooks)

```text
Pass-1:  board seed → In Progress → /pre-implement → /loop-spec → wave-pr-action → live-verify (human)
Pass-2:  /learning-extract → /ground-spec → Done (orch) → wave-signoff (human merge)
Closure (all waves done; eng loop then PM loop):
  initiative-closure
    → /purge-initiative-artifacts-app → initiative-closure-pr-action-app
    → initiative-closure-signoff-app (human merge app)
    → /purge-initiative-artifacts-meta → initiative-closure-pr-action-meta
    → initiative-closure-signoff-meta (human merge meta)
```

Do not document orchestrated auto-verify/ground after `loop-spec`.
Do not materialize a merge Forge skill — wave / initiative-closure merge is
human-only.
Do not materialize `/update-board-status` — keep human forge trio only.
Do not document per-wave purge.

## Partner handoff

Share [for-launchpad.md](for-launchpad.md) with the launchpad team when the pin
lands (they track fixture/`review_roles`/materialize/AGENTS changes on **their**
side). Purge skill **semantics** live in prayog skill packages; Launchpad only
materializes and lists slash commands.

## Out of scope for Launchpad

- Implementing Gateflow Enter-at or learning DB
- Putting forge skills on workflow `outcomes`
- Confusing kit **forge templates** (`apply-forge-templates`) with **forge skills**
- Implementing purge allowlist logic (prayog skills own that)
