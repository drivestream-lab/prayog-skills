---
name: github-issue-classifier
description: Reviews GitHub issues stored as local markdown files (from Github-Issue-Extractor), classifies every non-DONE issue into epics/user stories/tasks/defects by label, and produces two reports — a flat classification with status, and a full hierarchy organized by milestone → epic → story/task → defect. Use when asked to categorize issues, identify epics, build a hierarchy view, find related tickets, or analyze a GitHub issue repo dump.
---

# GitHub Issue Classifier

Classifies GitHub issues into epics / user stories / tasks / defects. Supports:

- **Mode A — Classify All:** Flat list of every open issue categorized by type, with status
- **Mode B — Hierarchy View:** Full repo organized as Milestone → Epic → Story/Task → Defect
- **Mode C — Lab (gh):** Live classification via `gh` when no local issue dump exists (prayog-meta Ch8)

---

## Mode C — Lab (gh) — prayog-meta Chapter 8

Use when planning **INIT-PRAYOG-001** epics/issues without a Github-Issue-Extractor dump.

```bash
gh issue list --repo drivestream-lab/prayog-meta --state all \
  --json number,title,labels,state,milestone,body \
  --limit 200
```

Repeat per app repo if needed (`prayog-parichay`, `prayog-abhilekh`, `prayog-ops`).

**Lab label → type mapping** (adjust if repo labels differ):

| Label | Type |
|-------|------|
| `epic` | Epic |
| `story`, `user-story` | User Story |
| `task`, `chore` | Task |
| `bug`, `defect` | Defect |
| `enhancement` | User Story |

**Title inference** (unlabeled): `EPIC` in title → Epic; `BUG`/`FIX` → Defect; `INIT-PRAYOG-001` prefix → match parent epic by issue body links.

Output: `playbook/reports/issue-classification-INIT-PRAYOG-001-YYYY-MM-DD.md` in the consumer repo (create `playbook/reports/` if missing).

---

## Setup (Modes A & B — local markdown dump)

Issues live in:
```
issues/<owner>-<repo>/
```

Each issue is a markdown file with YAML frontmatter (from [Github-Issue-Extractor](https://github.com) or similar export). Optional `.metadata.json` in the same folder.

**Scripts** (vendored with this skill):
```
.agents/skills/github-issue-classifier/scripts/
```

**Dependencies:**
```bash
pip install pyyaml
```

Run scripts from the consumer repo root, passing the skill script path:
```bash
python .agents/skills/github-issue-classifier/scripts/classify_issues.py issues/<owner>-<repo>/
```

---

## Mode A — Classify All Issues

Run the classification script:
```bash
python .agents/skills/github-issue-classifier/scripts/classify_issues.py issues/<owner>-<repo>/
```

### What it outputs
| Output | Content |
|---|---|
| **File** (full) | `issues/<owner>-<repo>/reports/classification-YYYY-MM-DD.md` — GitHub-flavoured markdown tables for all four types, each row including `# | Status | Labels | Milestone | Title` |
| **Terminal** (summary) | Counts only (Epic / Defect / User Story / Task / Total) + path to the file |

The file is created automatically; no flags needed. Running again on the same day overwrites the file.

### Columns in every issue table
| Column | Content |
|---|---|
| `#` | Issue number |
| `Status` | 🟢 open or ⚫ closed |
| `Labels` | Comma-separated GitHub labels |
| `Milestone` | Milestone name, blank if none |
| `Title` | Linked to the GitHub issue URL |

### Label → Type Mapping

| Label(s) on issue | Assigned Type |
|---|---|
| `epic` | **Epic** |
| `story`, `Technical story` | **User Story** |
| `enhancement` | **User Story** (feature additions have user value) |
| `bug`, `UAT-Bug` | **Defect** |
| `design`, `housekeeping`, `wontfix` | **Task** |
| *(no labels)* | **Task** by default; infer from title if possible |

**Priority when multiple labels exist:** Epic > Defect > User Story > Task

### "DONE" Definition
`state: closed` = Done. Only open issues are shown in the four type buckets.
There is no explicit "DONE" label in this repo's convention — closures are the signal.

### Inferring type from title (unlabeled issues only)
- Title contains `EPIC` → Epic
- Title starts with `SEC:` or `SUSA-` → Task (security audit finding)
- Title contains `BUG`, `CRASH`, `FIX`, `ERROR` → Defect
- Otherwise → Task

---

## Mode B — Hierarchy View

Run the hierarchy script:
```bash
python .agents/skills/github-issue-classifier/scripts/build_hierarchy.py issues/<owner>-<repo>/
```

### What it outputs
| Output | Content |
|---|---|
| **File** (full) | `issues/<owner>-<repo>/reports/hierarchy-YYYY-MM-DD.md` — milestone summary table then one section per milestone, closing with a no-milestone section |
| **Terminal** (summary) | Per-milestone counts (Total / Epics / Stories/Tasks / Defects) + path to the file |

The file is created automatically; no flags needed. Running again on the same day overwrites the file.

### File Structure

```
# Issue Hierarchy — <repo>

## Milestones          ← summary table of all milestones

---
## Milestone: Bugs     ← alphabetical order
  ### Epics (N)
    #### 🔗 Epic #XXX — 🟢 open
      | # | Status | Labels | Title |     ← child stories/tasks
      | ↳ #YYY | ...  |        |       ← defects linked to that story
  ### User Stories & Tasks — no epic (N)
      | # | Status | Labels | Title |
      | ↳ #ZZZ | ...  |        |       ← defects linked to story
  ### Defects — no story/task or epic (N)

---
## Milestone: Comms
  ...

---
## No Milestone        ← always last; same internal structure
```

### Milestone ordering
- Named milestones: **alphabetical A → Z**
- Issues with no milestone: collected under **"No Milestone"** at the very end

### How children are linked to an epic
| Priority | Signal |
|---|---|
| 0 — Definitive | `parent_issue` on issue = epic number, or epic's `sub_issues` list contains the issue |
| 1 — Hard data | Same milestone AND keyword match from epic title |

🔗 badge = confirmed via hierarchy link (Signal 0). No badge = milestone/keyword only.

### How defects are linked to a story/task
| Priority | Signal |
|---|---|
| 0 — Definitive | `parent_issue` on defect = story number |
| 1 — Hard data | Standalone `#<story_number>` reference in defect body |

Defects not linked to any story/task or epic appear in the **"Defects — no story/task or epic"** subsection of their milestone.

---

## Output Format

### Mode A — Terminal summary
```
============================================================
  Issue Classification — DBDHub-SecuritasOfficer-Android
  2026-02-26
============================================================

  Total : 310  |  Closed/DONE : 132  |  Open : 178

  Type        Count
  ----------  -----
  Epic        10
  Defect      54
  User Story  94
  Task        20
  TOTAL       178

  Full report written to:
  issues/DBDHub-SecuritasOfficer-Android/reports/classification-2026-02-26.md
```

### Mode A — File content
```markdown
# Issue Classification — DBDHub-SecuritasOfficer-Android
*Generated: 2026-02-26*

**Total issues:** 310 | **Closed/DONE:** 132 | **Open/Active:** 178

---
## Epics (10)
| #    | Status  | Labels       | Milestone        | Title                   |
|------|---------|--------------|------------------|-------------------------|
| #697 | 🟢 open | design, epic | Geolocation      | [GEO: EPIC: ...](<url>) |

---
## Defects (54)  ...
## User Stories (94)  ...
## Tasks (20)  ...

## Summary
| Type       | Open Count |
|------------|------------|
| **TOTAL**  | **178**    |
```

### Mode B — Terminal summary
```
============================================================
  Issue Hierarchy — DBDHub-SecuritasOfficer-Android
  2026-02-26
============================================================

  Total: 310  |  Closed/DONE: 132  |  Open: 178

  Milestone          Total  Epics  Stories/Tasks  Defects
  ------------------ ------  -----  -------------  -------
  Bugs                   12      0              3        9
  Geo Enhancements       10      2              7        1
  Geolocation           174      7            113       54
  ...

  Full report written to:
  issues/DBDHub-SecuritasOfficer-Android/reports/hierarchy-2026-02-26.md
```

### Mode B — File content (excerpt: Geo Enhancements)
```markdown
## Milestone: Geo Enhancements  (10 open / 10 total)

### Epics (2)

#### 🔗 Epic #1042 — 🟢 open
**[EPIC -- Android -- Employee Tools Access Point](<url>)**
Labels: `epic`

| #        | Status  | Labels | Title                                 |
|----------|---------|--------|---------------------------------------|
| 🔗#1043  | 🟢 open | story  | [Android -- Employee Tools -- ...](<url>) |
| 🔗#1044  | 🟢 open | story  | [Android -- Employee Tools -- ...](<url>) |
| #1045    | 🟢 open | story  | [Android -- Employee Tools -- ...](<url>) |

### User Stories & Tasks — no epic (1)
| #     | Status  | Labels          | Title                    |
|-------|---------|-----------------|--------------------------|
| #1046 | 🟢 open | Technical story | [SPIKE - ...](<url>)     |

### Defects — no story/task or epic (1)
| #     | Status  | Labels | Title                    |
|-------|---------|--------|--------------------------|
| #1075 | 🟢 open | bug    | [Use shiftSummaryId ...](<url>) |
```

---

## Key Rules

1. **Hierarchy first** — `parent_issue` / `sub_issues` frontmatter fields are the strongest signal; always check them before falling back to milestone/keyword
2. **Status always shown** — every issue row in every report includes a `Status` column (🟢 open / ⚫ closed)
3. **No guesswork for confirmed relations** — only report a relationship if at least one signal is present
4. **Always verify false positives** for numeric `#N` references before reporting them
5. **Closed issues included in hierarchy** — the hierarchy view shows all issues (open and closed) so the full picture is visible; status column makes state clear
6. **Superseded stories** — flag duplicates; do not silently omit them
7. **Empty hierarchy** — if `sub_issues` is empty on an epic, that does not mean it has no children; some teams don't use GitHub's sub-issue feature — rely on milestone + keyword signals instead

---

## Scripts

| Script | Mode | Input | Output file |
|---|---|---|---|
| `scripts/classify_issues.py` | A — Flat classification | `<issues_folder>` | `reports/classification-YYYY-MM-DD.md` |
| `scripts/build_hierarchy.py` | B — Hierarchy view | `<issues_folder>` | `reports/hierarchy-YYYY-MM-DD.md` |
| `scripts/find_epic_relations.py` | Single-epic deep-dive | `<issues_folder> <epic_number>` | `reports/epic-<N>-relations-YYYY-MM-DD.md` |

Example (single-epic deep-dive):
```bash
python .agents/skills/github-issue-classifier/scripts/find_epic_relations.py issues/<owner>-<repo>/ 42
```
