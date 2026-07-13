---
name: board-seed
description: >-
  After spec PR merge, seed the programme engineering board from Implementation
  Plan §9 WorkManifest: EPIC parent issue, wave sub-issues (W0..Wn), correct org
  Project, and initiative grouping. Stack-agnostic — use on any app repo with
  delivery_contract. Requires read-only meta clone for governance board binding.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/reports/**, .harness/profile.yaml
metadata:
  background_eligible: false
---

# Board seed

Seed **one initiative tree** on the **programme engineering board** after the
spec package is merged to the integration branch. Applies to **any app stack**
(python-backend, frontend, terraform-iac, data-platform, …) — not `meta-pm`.

**Do not run before spec merge.** **Do not write product code.**

## NON-NEGOTIABLE

1. Resolve layout from `.harness/profile.yaml` or
   [references/layout-defaults.md](references/layout-defaults.md).
2. **Spec merge gate first** — merged `Implementation-Plan-{initiative}.md` on
   integration branch (`develop` or profile equivalent); closed spec PR had
   `spec-lgtm` on merge head when verifiable via `gh`.
3. **Board binding** — resolve programme board from **read-only meta** governance:
   `{workspace}/{meta_repo}/config/governance-*.yaml` → `project_board.name`
   (exact match). If missing, run `launchpad board-bind --client <id>` and stop.
   Governance **wins** over plan §9 `target.project` free text.
4. Parse §9 WorkManifest YAML from the merged plan. Require `epic`, `work[]`
   with wave ids `W0`, `W1`, …
5. **Idempotent** — search existing issues by initiative label + wave title/id;
   create only missing items; link existing waves under EPIC when parent missing.
6. **Hierarchy** — EPIC first, then each wave as **sub-issue** (`--parent`) on
   the **same org Project** (`--project "<board name>"`). Initiative label on
   every issue.
7. **No GitHub mutations** until developer explicitly authorizes seeding.
8. If `gh` or `project` scope unavailable, print exact commands from
   [references/output-template.md](references/output-template.md) and stop —
   do not claim `seeded`.

## Inputs

1. **Initiative id** — (REQUIRED) e.g. `INIT-MOBBOT-001`
2. **Integration branch** — (REQUIRED) default `develop`
3. **Merged plan** — `{reports_dir}/{plan_prefix}-{initiative}.md` §9
4. **Meta governance** — (REQUIRED) sibling meta clone:
   `../{meta_repo}/config/governance-<org>.yaml` or path from `clients.yaml`
5. **`gh` auth** — (REQUIRED for apply) `gh auth status`; project scope for
   `--project` (`gh auth refresh -s project`)

## Prerequisite

- Spec PR **merged**; plan §9 on integration branch
- P14-valid WorkManifest in §9
- Programme board configured (`project_board.enabled` + `name`)

## Process

1. **T0 Gather** — initiative, plan path, §9 YAML, governance board binding,
   current repo slug, integration branch HEAD
2. **T1 Verify merge gate** — plan file exists; optional `gh pr list` closed
   spec PR with `spec-lgtm`; stop if open spec branch context
3. **T2 Dedupe search** — `gh issue list --repo {org}/{repo} --label {initiative}`
4. **T3 Present seed plan** — EPIC + waves, board name/URL, create vs existing,
   exact `gh issue create` / `gh issue edit` commands
5. **T4 Execute** (authorized only) — EPIC with `--project`; waves with
   `--parent {epic#} --project`; set dependency links in bodies if needed
6. **T5 Report** — issue URLs, project link, handoff `seeded` or `already-seeded`

## GitHub command pattern (all app stacks)

```bash
# Board name from governance — not guessed
BOARD="<governance.project_board.name>"
REPO=<org>/<epic.repo from §9>

EPIC=$(gh issue create --repo "$REPO" \
  --title "<epic.title from §9>" \
  --label "<initiative>" \
  --project "$BOARD" \
  --body-file /tmp/epic-body.md --json number -q .number)

gh issue create --repo "$REPO" \
  --title "<work.title>" \
  --label "<initiative>" \
  --parent "$EPIC" \
  --project "$BOARD" \
  --body-file /tmp/w0-body.md
```

Repair existing flat issues:

```bash
gh issue edit <EPIC#> --add-sub-issue <W0#>,<W1#>,...
gh issue edit <issue#> --add-project "$BOARD"
```

## Output

Present seed report using [references/output-template.md](references/output-template.md).
Run checks from [references/checks.md](references/checks.md).

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md`. Use stage
`board-seed`.

| Outcome | Next |
|---------|------|
| `pass` (`seeded` / `already-seeded`) | `/pre-implement` W0 |
| `blocked` | retry after `gh auth refresh -s project` or board access |
| `failed` | human fixes §9 or governance; re-run |
| `stale` | `/spec-implementation-plan` if plan not on integration branch |

Set `external_action: true` when GitHub issue/project mutations are the
candidate next step. The handoff never authorizes GitHub mutation without
explicit developer approval.
