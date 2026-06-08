# github-issue-classifier

Classify GitHub issues into epics / stories / tasks / defects. Modes A–B use vendored Python scripts on local issue markdown dumps; **Mode C (lab)** uses `gh issue list` for INIT planning.

**Original author:** rushikeshpol02 (ai-skills). **Maintainer:** drivestream-lab.

## Invoke

```
/github-issue-classifier
```

**Lab (Ch8):** classify `INIT-PRAYOG-001` issues across `prayog-meta` and app repos via `gh`.

**Scripts:** `scripts/classify_issues.py`, `build_hierarchy.py`, `find_epic_relations.py` — require `pyyaml`.

See repo root README for install command.
