# Forge side-effects

Pin-declared **mutation** policy for GitHub (and related systems). Orthogonal to
**tools** provisioned *during* a skill hop (for example code-graph / MCP).

| | Tools (future / slots) | Forge |
|--|------------------------|-------|
| When | During the skill hop | After the hop, or on a following `external-action` |
| Who | Agent runtime may call | Platform ForgeClient (runner) or human forge skill |
| What | Assist / read | Commit tree, Draft PR, projection labels, board tickets |

Contract surface: `delivery-contract.yaml` → `forge:`. Narrative SSOT: this file.
Handoff instance payload: [`handoff-envelope.md`](handoff-envelope.md) (`forge:`).

## Pin fields

### Skill nodes — `forge.commit_workspace`

| Value | Meaning |
|-------|---------|
| `disabled` | Do not publish workspace tree after the hop (schema default if `forge` absent) |
| `optional` | Publish when there are includable changes; empty OK |
| `required` | Fail closed when automate expects durable output and nothing to publish |

Do **not** put `forge.head` (`run` / `skill` / `meta`) on the pin. The orchestrator
binds the remote ref from run context (wave PR, meta PR, spec branch, …).

### External-action nodes — `forge.action`

| `forge.action` | Human skill id | Role |
|----------------|----------------|------|
| `commit_workspace` | `commit-workspace` | Publish workspace tree |
| `open_draft_pr` | `open-draft-pr` | Open/update Draft PR + projection labels |
| `create_board_tickets` | `create-board-tickets` | Create epic/wave tickets from readiness |

Naming rule: human skill id = `action` with `_` → `-`.

Typical `open_draft_pr` pin shape:

```yaml
prd-pr-action:
  type: external-action
  authorization: explicit
  forge:
    action: open_draft_pr
    draft: true
    apply_labels:
      - impact-map-pending
    remove_labels: []
    requires:
      - title
      - body_path
```

Rules:

- `apply_labels` / `remove_labels` are **projection** only. Never auto-apply
  approval labels whose names end in `-lgtm`.
- `requires` lists instance slots content skills must fill into `handoff.forge`.
- Pin wins on policy (action, draft, labels). Handoff supplies instance values.
- Conflict (handoff invents a label outside pin policy) → fail closed.

## Two executors

```text
Content skill
  → artifacts + complete handoff.forge (fill pin requires)
       │
       ├─ Human:  /commit-workspace | /open-draft-pr | /create-board-tickets
       └─ Runner: ForgeClient / BoardService (same pin ⋉ handoff)
```

- Human forge skills live under `skills/forge/`. They are **not** workflow
  graph nodes (never appear on `outcomes`). Frontmatter:
  `disable-model-invocation: true`.
- Orchestrators **must not** auto-dispatch forge skills. After a content hop they
  apply pin `commit_workspace` and/or stop on `external-action` for auth, then
  ForgeClient.
- Local CLI (`gh`, git) is an example of available Forge tooling for humans —
  never the automate success path.

## Content producers

Content skills produce durable artifacts and a complete handoff. They do **not**
execute forge mutations (commit, Draft PR, board tickets).

### Must

1. Persist the stage artifact and pin-faithful `handoff:` (including baton
   dual-write when `handoff_path` is bound).
2. Derive `next_candidates`, `human_checkpoint`, and `external_action` from
   pinned `workflow.yaml` (`external_action` = next node `type` is
   `external-action`).
3. When the pin expects forge instance slots for this outcome (next node has
   `forge.requires`, or this node’s `commit_workspace` is `optional`/`required`
   and a recommendation is appropriate), **fill `handoff.forge`** so the
   package is complete for either executor.
4. Align `handoff.forge.action` / labels with the pin. Do not invent approval
   labels (`*-lgtm`) or labels outside pin policy.
5. Recommend the matching human forge skill in chat **and** handoff
   (`/open-draft-pr`, `/commit-workspace`, `/create-board-tickets`) using the
   same action vocabulary (`open_draft_pr` ↔ `open-draft-pr`).
6. Use agent-/tool-neutral wording. Local CLI (`gh`, git) is an example only.

### Must not

1. Treat forge success (PR opened, tickets created, push succeeded) as this
   content skill’s success criteria.
2. Call forge / open PRs / create board tickets inside the content skill
   procedure as an automatic side effect.
3. Hardcode skill-id allowlists or walker-specific exemptions.

### Incomplete handoff

If `outcome` routes to an `external-action` with `forge.requires` and any
required slot is missing from `handoff.forge`, the envelope is **incomplete** —
orchestrators fail closed; human forge skills must ask or block.

## Consumer algorithm (sketch)

```text
# After content skill hop
policy = nodes[stage].forge.commit_workspace ?? disabled
if orchestrator and policy in {optional, required}:
    ForgeClient.commit_workspace(bind_head_from_run_context)
    if policy == required and nothing_published: FAIL

next = resolve(stage, outcome)
if next.type == external-action:
    # authorization is REQUIRED on every external-action (explicit|automated).
    # Missing or unknown value → invalid pin / FAIL closed.
    auth = next.authorization
    if auth not in {explicit, automated}:
        FAIL

    effective = merge(next.forge, handoff.forge)  # pin wins policy
    if next.forge.requires and missing any required slot:
        FAIL

    if auth == explicit:
        STOP until interactive / API authorization
    # auth == automated: no interactive STOP — pre-authorized ForgeClient

    if orchestrator:
        ForgeClient.apply(effective)
    # human walker: recommend / run skills/forge/<action-kebab>
    # (human forge skills still require user confirm when the human invokes them)
```

| `authorization` | Meaning |
|-----------------|--------|
| `explicit` | STOP for authorize, then ForgeClient |
| `automated` | ForgeClient runs immediately when requires are complete |

Day-one pin: `spec-pr-action`, `wave-pr-action`, and
`initiative-closure-pr-action` are `automated`; other external-actions are
`explicit`. Wave merge and initiative-closure merge remain human-only at
`wave-signoff` / `initiative-closure-signoff` (no merge Forge action).

## Reserved actions

Documented for later pins / skills (not required in this RC slice):

- `link_pr_to_ticket`
- `update_board_status`
- `post_forge_comment`
