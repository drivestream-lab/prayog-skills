# PM lane — think-first authoring

**Purpose:** operator flow for meta workspaces. Normative procedure lives in
each skill's `SKILL.md`; this doc orients humans only.

## Why think-first

Community `/prd` (awesome-copilot) fills outlines. That produces PRD-shaped
documents that **look** complete but leak as-built detail, skip negative paths,
and force `/spec-draft` to guess. The think-first lane treats the brief as a
**hypothesis**, grills it, and writes **candidates** that `/prd-quality` scores
before anything reaches `prd/{INIT}.md`.

## Role separation

| Skill | Job | Writes |
|-------|-----|--------|
| `/prd-think` | Author candidates | `{reports_dir}/{INIT}-prd-think(-N).md` |
| `/prd-quality` | Score + Handover gate | `{reports_dir}/{INIT}-prd-quality.md` |
| `/validate-requirements` | Audit promoted PRD | `Validation-Report-{INIT}.md` |

Think **authors**. Quality **scores**. Validate **audits**. Do not collapse
these jobs.

## Operator chain

```text
outline/brief
  → /prd-think          (rerun → -2, -3, …; never overwrites prior runs)
  → /prd-quality        (Handover: yes = zero material FAILs on that file)
  → human promote       (named candidate → prd/{INIT}.md)
  → /validate-requirements
  → /review-findings
  → /update-documents
  → /prd-impact-map
```

**Rules:**

- Do not run validate, review, update, or impact-map on **candidates**.
- `handover: yes` on file X does not auto-promote — human names the file.
- `Ci-wins` is rank only, not permission to validate.
- CBM / codebase grapher belongs at **impact-map**, not think or validate.

## Harness

Both skills are listed in `profiles/meta-pm.yaml` `requirements_skills` but are
**not** workflow nodes. Entrypoint remains `/validate-requirements` on the
**promoted** PRD.

After pinning `v0.5.4+`:

1. Bump `agent_skills.ref` in `.harness-pin.yaml`
2. Add `prd-think` and `prd-quality` to `agent_skills.skills`
3. Remove `- prd` from skills list and delete `community_skills` awesome-copilot block
4. Run `launchpad apply-harness --meta --apply`

## Optional companions (overlay, not pin)

Install manually when useful:

- `/grilling`, `/grill-with-docs` — T1 challenge
- `/domain-modeling`, `/opportunity-solution-tree` — T2 model
- `/strategy-red-team` — T3 stress
- `/prd-critic` — secondary opinion inside `/prd-quality`

## Evidence (overlay experiment)

Gateflow lab runs on prayog-meta and drivestream-meta compared think-first
candidates vs outline-fill `/prd` on the same briefs.

| Signal | Think-first | Outline-fill `/prd` |
|--------|-------------|---------------------|
| Handover on grilled candidate | Often `yes` after 2–3 runs | N/A (no delivery bar) |
| As-built in REQ text | Caught by B11 at quality | Common in promoted PRDs |
| REQ table + CAP linkage | Required by candidate schema | Often missing |
| Factory citizenship | Locked in T1 (actors, non-goals) | Brief headings copied |

Example INIT-GATEFLOW-017: C3 (`prd-think-3.md`) handover yes; C4 (outline path)
handover no — HTTP paths and ops names in REQ text (B3/B11).

## Program truth at T0

Cite `planning/` (system brief, vision, actor tables) when Think needs product
context. Do **not** wire OKF / `knowledge/` at T0 unless explicitly agreed.
