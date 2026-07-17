# Product question template

Every product question emitted by `/prd-codebase-map`, refined by
`/review-product-questions`, or posted by `/post-product-questions` MUST include
these fields. Language must be **feature / user / product** — not modules, ADRs,
or implementation plans.

```markdown
### Q-{NN} — {short title}

- **PRD ref:** {section / capability / bullet}
- **Repos(s):** {org/repo list}
- **Delta:** partial | conflict | unknown
- **Scenario:** When {actor} tries to {goal} under {context}…
- **Example:** Concrete expected behaviour or acceptance line PM can edit into the PRD
- **Recommendation:** Preferred product stance
- **Why:** Risk if wrong (rework, wrong UX, scope creep, false “already built”)
- **Alternatives:**
  - A: …
  - B: …
- **Evidence:** {repo} · {graph node or path} · EXTRACTED|INFERRED|AMBIGUOUS · as-built: {row or none}
```

## Caps and priority

1. Default cap: **10** open product questions per map revision (PE may raise
   with explicit note).
2. Priority order: `conflict` → `partial` → high-impact `unknown`.
3. Do **not** open a question for clear `exists` or clear `absent` unless PM
   must confirm scope (e.g. “already shipped — drop from PRD?”).
4. Never ask PM to choose architecture, library, or module boundaries — those
   stay in the eng appendix or post-Gate feasibility / technical-review.

## Meta PR projection

Optional: PE runs `/review-product-questions` to refine stance, then
`/post-product-questions` to post on the **meta PRD PR** (after authorization),
linking to `PRD-Codebase-Map-{INIT}.md`. Comments are projections; the map (and
stance file, if any) remain canonical. **PM** answers on the PR and updates the
PRD via requirements skills.
