#!/usr/bin/env python3
"""WorkManifest contract validator (prayog/v1).

Parse a fenced §9 YAML block or standalone document and fail closed on
identity, stable-ID, dependency-DAG, file-scope, exit-proof, REQ-mapping,
wave-ordering, and live-verification violations.

CLI:
  python scripts/workmanifest_contract.py <plan.md|manifest.yaml>

Import:
  from scripts.workmanifest_contract import (
      extract_workmanifest_yaml,
      validate_workmanifest,
  )
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover — CI installs PyYAML
    yaml = None  # type: ignore[assignment]

API_VERSION = "prayog/v1"
KIND = "WorkManifest"
FILE_ACTIONS = frozenset({"create", "modify", "delete", "inspect"})
PROOF_KINDS = frozenset({"command", "review"})
LIVE_MODES = frozenset({"smoke", "sandbox"})
FORBIDDEN_MUTABLE = frozenset(
    {
        "status",
        "state",
        "observed",
        "evidence_actual",
        "board_status",
        "column",
        "runtime_head",
        "build_sha",
    }
)

WAVE_ID_RE = re.compile(r"^W(\d+)$")
TASK_ID_RE = re.compile(r"^TASK-W(\d+)-(\d+)$")
REQ_ID_RE = re.compile(r"^REQ-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$")
SHADOW_REQ_RE = re.compile(r"^REQ-W\d")
ABS_PATH_RE = re.compile(r"^(?:[A-Za-z]:[\\/]|/)")
GLOB_CHARS_RE = re.compile(r"[*?\[\]]")
UNIT_AS_LIVE_RE = re.compile(
    r"(?i)^\s*(make\s+test|npm\s+test|yarn\s+test|pytest(\s|$)|go\s+test|"
    r"cargo\s+test|mvn\s+test|\{test_command\}|\$\{?test_command\}?)\b"
)
VAGUE_EXIT_RE = re.compile(
    r"(?i)^\s*(done|complete|completed|works|working|ok|fine|looks\s+good|"
    r"implemented|finished|shipped|lgtm|pass(es|ed)?|good)\s*\.?$"
)

FENCE_RE = re.compile(
    r"```(?:yaml|yml)\s*\n(.*?)```",
    flags=re.DOTALL | re.IGNORECASE,
)

# Live-verify coverage marker — a plain literal substring, not a per-language
# comment syntax. See references/live-verify-coverage-contract.md.
COVERS_MARKER_RE = re.compile(r"prayog:covers:\s*([^\n\r]+)")


def extract_declared_coverage(text: str) -> list[str] | None:
    """Return the REQ-* ids self-declared by a ``prayog:covers:`` marker, or
    None when the marker is absent (no evidence to check — not a mismatch).

    Only keeps REQ-shaped tokens — the marker's trailing text often runs
    into a comment closer (``-->``, ``*/``, ``#>``) depending on the host
    file's native comment syntax; filtering by shape is more robust than
    trying to enumerate every closer for every language."""
    match = COVERS_MARKER_RE.search(text)
    if not match:
        return None
    return [
        item.strip()
        for item in re.split(r"[,\s]+", match.group(1).strip())
        if REQ_ID_RE.fullmatch(item.strip())
    ]


def _err(code: str, message: str, path: str = "") -> dict[str, str]:
    return {"code": code, "message": message, "path": path}


def extract_workmanifest_yaml(text: str) -> str | None:
    """Return the YAML body of the WorkManifest fence, or None."""
    if not text or not text.strip():
        return None

    stripped = text.strip()
    if stripped.startswith("apiVersion:") or stripped.startswith("kind:"):
        return stripped

    # Prefer fence under §9 when present
    section = text
    marker = re.search(r"^##\s*9\.\s*WorkManifest", text, flags=re.MULTILINE)
    if marker:
        section = text[marker.start() :]
        next_h2 = re.search(r"^##\s+(?!9\.)", section[1:], flags=re.MULTILINE)
        if next_h2:
            section = section[: next_h2.start() + 1]

    for match in FENCE_RE.finditer(section):
        body = match.group(1).strip()
        if "kind: WorkManifest" in body or "kind:WorkManifest" in body:
            return body
        if "apiVersion:" in body and "work:" in body:
            return body

    for match in FENCE_RE.finditer(text):
        body = match.group(1).strip()
        if "kind: WorkManifest" in body or "apiVersion: prayog/v1" in body:
            return body
    return None


def _load_mapping(source: str | dict[str, Any]) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if isinstance(source, dict):
        return source, []
    if yaml is None:
        return None, [_err("dependency", "PyYAML is required for WorkManifest validation")]
    raw = extract_workmanifest_yaml(source) if "```" in source or "## 9." in source else source
    if raw is None:
        # Try whole text as YAML
        raw = source
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001 — surface parse errors structurally
        return None, [_err("yaml_parse", f"YAML parse failed: {exc}")]
    if not isinstance(data, dict):
        return None, [_err("yaml_parse", "WorkManifest root must be a mapping")]
    return data, []


def _is_vague_criterion(text: str) -> bool:
    cleaned = " ".join(str(text).strip().split())
    if len(cleaned) < 12:
        return True
    return bool(VAGUE_EXIT_RE.match(cleaned))


def _valid_repo_path(path: str) -> bool:
    if not path or not isinstance(path, str):
        return False
    p = path.strip()
    if not p or p.startswith("~") or ABS_PATH_RE.match(p):
        return False
    if p.startswith("../") or "/../" in p or p == "..":
        return False
    if GLOB_CHARS_RE.search(p):
        return False
    return True


def _topo_cycle(nodes: set[str], edges: dict[str, list[str]]) -> list[str] | None:
    """Return a cycle path if present, else None."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        color[node] = GRAY
        stack.append(node)
        for nxt in edges.get(node, []):
            if nxt not in nodes:
                continue
            if color[nxt] == GRAY:
                if nxt in stack:
                    i = stack.index(nxt)
                    return stack[i:] + [nxt]
                return [node, nxt, node]
            if color[nxt] == WHITE:
                found = visit(nxt)
                if found:
                    return found
        stack.pop()
        color[node] = BLACK
        return None

    for n in sorted(nodes):
        if color[n] == WHITE:
            found = visit(n)
            if found:
                return found
    return None


def _reject_mutable(obj: Any, path: str, errors: list[dict[str, str]]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = f"{path}.{key}" if path else str(key)
            if key in FORBIDDEN_MUTABLE:
                errors.append(
                    _err(
                        "mutable_field",
                        f"mutable/runtime field {key!r} is forbidden on approved WorkManifest",
                        child,
                    )
                )
            _reject_mutable(value, child, errors)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _reject_mutable(item, f"{path}[{i}]", errors)


def _validate_task(
    task: Any,
    *,
    wave_id: str,
    wave_num: int,
    index: int,
    errors: list[dict[str, str]],
) -> str | None:
    path = f"work[{wave_id}].tasks[{index}]"
    if not isinstance(task, dict):
        errors.append(_err("task_shape", "task must be a mapping", path))
        return None

    tid = task.get("id")
    if not isinstance(tid, str) or not TASK_ID_RE.fullmatch(tid):
        errors.append(
            _err(
                "task_id",
                f"task id must match TASK-W{{n}}-{{nn}}; got {tid!r}",
                f"{path}.id",
            )
        )
        tid_out = None
    else:
        m = TASK_ID_RE.fullmatch(tid)
        assert m is not None
        if int(m.group(1)) != wave_num:
            errors.append(
                _err(
                    "task_id_wave",
                    f"task {tid} wave number must match containing wave {wave_id}",
                    f"{path}.id",
                )
            )
        tid_out = tid

    implements = task.get("implements")
    if not isinstance(implements, list) or not implements:
        errors.append(
            _err("implements", "implements must be a non-empty list of REQ-*", f"{path}.implements")
        )
    else:
        for j, req in enumerate(implements):
            rpath = f"{path}.implements[{j}]"
            if not isinstance(req, str) or not REQ_ID_RE.fullmatch(req):
                errors.append(_err("implements", f"invalid REQ id {req!r}", rpath))
            elif SHADOW_REQ_RE.match(req):
                errors.append(
                    _err("implements", f"shadow REQ-W* id forbidden: {req!r}", rpath)
                )

    depends = task.get("depends_on", [])
    if depends is None:
        depends = []
    if not isinstance(depends, list):
        errors.append(_err("depends_on", "depends_on must be a list", f"{path}.depends_on"))
        depends = []
    for j, dep in enumerate(depends):
        dpath = f"{path}.depends_on[{j}]"
        if not isinstance(dep, str) or not TASK_ID_RE.fullmatch(dep):
            errors.append(_err("depends_on", f"depends_on entry must be TASK-*; got {dep!r}", dpath))
        elif tid_out and dep == tid_out:
            errors.append(_err("depends_on_self", f"task must not depend on itself: {dep}", dpath))
        elif isinstance(dep, str):
            dm = TASK_ID_RE.fullmatch(dep)
            if dm and int(dm.group(1)) != wave_num:
                errors.append(
                    _err(
                        "depends_on_wave",
                        f"task dependency {dep} must be same-wave as {wave_id}",
                        dpath,
                    )
                )

    files = task.get("files")
    if files is None:
        errors.append(_err("files", "files is required (use [] only for explicit docs-only)", f"{path}.files"))
        files = []
    if not isinstance(files, list):
        errors.append(_err("files", "files must be a list", f"{path}.files"))
        files = []
    for j, entry in enumerate(files):
        fpath = f"{path}.files[{j}]"
        if not isinstance(entry, dict):
            errors.append(_err("files", "file entry must be a mapping", fpath))
            continue
        file_path = entry.get("path")
        action = entry.get("action")
        if not _valid_repo_path(str(file_path) if file_path is not None else ""):
            errors.append(
                _err(
                    "file_path",
                    f"path must be repo-relative exact path; got {file_path!r}",
                    f"{fpath}.path",
                )
            )
        if action not in FILE_ACTIONS:
            errors.append(
                _err(
                    "file_action",
                    f"action must be one of {sorted(FILE_ACTIONS)}; got {action!r}",
                    f"{fpath}.action",
                )
            )

    exit_block = task.get("exit")
    if not isinstance(exit_block, dict):
        errors.append(_err("exit", "exit mapping is required", f"{path}.exit"))
    else:
        criteria = exit_block.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            errors.append(
                _err("exit_criteria", "exit.criteria must be a non-empty list", f"{path}.exit.criteria")
            )
        else:
            for j, item in enumerate(criteria):
                cpath = f"{path}.exit.criteria[{j}]"
                if not isinstance(item, str) or not item.strip():
                    errors.append(_err("exit_criteria", "criterion must be non-empty string", cpath))
                elif _is_vague_criterion(item):
                    errors.append(
                        _err(
                            "exit_criteria_vague",
                            f"exit criterion is vague/non-observable: {item!r}",
                            cpath,
                        )
                    )
            if not files:
                joined = " ".join(str(c).lower() for c in criteria)
                if "docs" not in joined and "documentation" not in joined:
                    errors.append(
                        _err(
                            "files_empty",
                            "empty files[] requires docs-only exit criteria",
                            f"{path}.files",
                        )
                    )

        proof = exit_block.get("proof")
        if not isinstance(proof, dict):
            errors.append(_err("exit_proof", "exit.proof mapping is required", f"{path}.exit.proof"))
        else:
            kind = proof.get("kind")
            if kind not in PROOF_KINDS:
                errors.append(
                    _err(
                        "exit_proof_kind",
                        f"exit.proof.kind must be one of {sorted(PROOF_KINDS)}; got {kind!r}",
                        f"{path}.exit.proof.kind",
                    )
                )
            if kind == "command":
                cmd = proof.get("command")
                if not isinstance(cmd, str) or not cmd.strip():
                    errors.append(
                        _err(
                            "exit_proof_command",
                            "exit.proof.command is required when kind=command",
                            f"{path}.exit.proof.command",
                        )
                    )
            if kind == "review":
                review = proof.get("review")
                if not isinstance(review, str) or not review.strip():
                    errors.append(
                        _err(
                            "exit_proof_review",
                            "exit.proof.review is required when kind=review",
                            f"{path}.exit.proof.review",
                        )
                    )
            expected = proof.get("expected")
            if not isinstance(expected, str) or not expected.strip():
                errors.append(
                    _err(
                        "exit_proof_expected",
                        "exit.proof.expected is required",
                        f"{path}.exit.proof.expected",
                    )
                )
            evidence = proof.get("evidence_expected")
            if not isinstance(evidence, str) or not evidence.strip():
                errors.append(
                    _err(
                        "exit_proof_evidence",
                        "exit.proof.evidence_expected is required",
                        f"{path}.exit.proof.evidence_expected",
                    )
                )

    if "parallel_safe" in task or "shared_files" in task:
        errors.append(
            _err(
                "deferred_field",
                "parallel_safe/shared_files are not part of prayog/v1",
                path,
            )
        )

    return tid_out


def _check_declared_coverage(
    covers: list[str],
    *,
    wave_id: str,
    wave_files: list[str],
    base_path: Path | None,
    path: str,
    errors: list[dict[str, str]],
) -> None:
    """Cross-check ``live.covers`` against any wave file's self-declared
    marker (resolved via files[], never by parsing ``command``). Only runs
    when a workspace root is supplied — omit ``base_path`` and this is
    skipped, not failed. A file with no marker is not evidence of anything
    (best-effort backfill); only a *present but disjoint* marker fails."""
    if base_path is None or not wave_files:
        return
    for rel_path in wave_files:
        candidate = base_path / rel_path
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except OSError:
            continue
        declared = extract_declared_coverage(text)
        if declared is None:
            continue
        if declared and covers and not (set(declared) & set(covers)):
            errors.append(
                _err(
                    "live_coverage_mismatch",
                    f"{rel_path} declares coverage {declared} disjoint from "
                    f"manifest live.covers {covers} — plan and artifact have drifted",
                    f"{path}.covers",
                )
            )


def _validate_live(
    live: Any,
    *,
    wave_id: str,
    verify_command: Any,
    errors: list[dict[str, str]],
    wave_files: list[str] | None = None,
    base_path: Path | None = None,
) -> None:
    path = f"work[{wave_id}].verification.live"
    if not isinstance(live, dict):
        errors.append(_err("live", "verification.live must be a mapping", path))
        return

    applicable = live.get("applicable")
    if applicable is not True and applicable is not False:
        errors.append(
            _err("live_applicable", "verification.live.applicable must be boolean", f"{path}.applicable")
        )
        return

    if applicable is False:
        reason = live.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(
                _err(
                    "live_reason",
                    "verification.live.reason is required when applicable=false",
                    f"{path}.reason",
                )
            )
        if isinstance(verify_command, str) and verify_command.strip():
            vc = verify_command.strip()
            if not vc.upper().startswith("N/A"):
                errors.append(
                    _err(
                        "verify_command_na",
                        "verify_command must be N/A — reason when live is not applicable",
                        f"work[{wave_id}].verify_command",
                    )
                )
        return

    mode = live.get("mode")
    if mode not in LIVE_MODES:
        errors.append(
            _err(
                "live_mode",
                f"live.mode must be one of {sorted(LIVE_MODES)}; got {mode!r}",
                f"{path}.mode",
            )
        )

    command = live.get("command")
    if not isinstance(command, str) or not command.strip():
        errors.append(_err("live_command", "live.command is required when applicable", f"{path}.command"))
    else:
        if UNIT_AS_LIVE_RE.match(command.strip()):
            errors.append(
                _err(
                    "unit_as_live",
                    f"live.command looks unit-only, not a live verify script: {command!r}",
                    f"{path}.command",
                )
            )
        if isinstance(verify_command, str) and verify_command.strip() and verify_command.strip() != command.strip():
            errors.append(
                _err(
                    "verify_command_mismatch",
                    "verify_command must equal verification.live.command when applicable",
                    f"work[{wave_id}].verify_command",
                )
            )

    covers = live.get("covers")
    if not isinstance(covers, list) or not covers:
        errors.append(_err("live_covers", "live.covers must be a non-empty REQ list", f"{path}.covers"))
    else:
        for j, req in enumerate(covers):
            if not isinstance(req, str) or not REQ_ID_RE.fullmatch(req) or SHADOW_REQ_RE.match(req):
                errors.append(_err("live_covers", f"invalid REQ in covers: {req!r}", f"{path}.covers[{j}]"))
        _check_declared_coverage(
            [c for c in covers if isinstance(c, str)],
            wave_id=wave_id,
            wave_files=wave_files or [],
            base_path=base_path,
            path=path,
            errors=errors,
        )

    for field in ("prerequisites", "expected_observations", "cleanup", "stop_conditions"):
        value = live.get(field)
        if not isinstance(value, list) or not value:
            errors.append(
                _err(
                    f"live_{field}",
                    f"live.{field} must be a non-empty list when applicable",
                    f"{path}.{field}",
                )
            )
        elif any(not isinstance(x, str) or not str(x).strip() for x in value):
            errors.append(
                _err(
                    f"live_{field}",
                    f"live.{field} entries must be non-empty strings",
                    f"{path}.{field}",
                )
            )


def validate_workmanifest(
    source: str | dict[str, Any],
    *,
    base_path: str | Path | None = None,
) -> list[dict[str, str]]:
    """Validate WorkManifest text or mapping. Return structured errors (empty = ok).

    ``base_path``, when supplied, enables the live-verify coverage
    cross-check (resolves each wave's declared ``files[]`` under this root
    and compares any self-declared marker against ``live.covers``). Omit it
    and that check is skipped, not failed — every other check runs
    regardless."""
    if base_path is not None:
        base_path = Path(base_path)
    data, errors = _load_mapping(source)
    if data is None:
        return errors

    if data.get("apiVersion") != API_VERSION:
        errors.append(
            _err(
                "identity",
                f"apiVersion must be {API_VERSION!r}; got {data.get('apiVersion')!r}",
                "apiVersion",
            )
        )
    if data.get("kind") != KIND:
        errors.append(
            _err("identity", f"kind must be {KIND!r}; got {data.get('kind')!r}", "kind")
        )

    _reject_mutable(data, "", errors)

    initiative = data.get("initiative")
    if not isinstance(initiative, str) or not initiative.strip():
        errors.append(_err("initiative", "initiative is required", "initiative"))

    epic = data.get("epic")
    if not isinstance(epic, dict):
        errors.append(_err("epic", "epic mapping is required", "epic"))
    elif epic.get("id") != "EPIC":
        errors.append(_err("epic_id", "epic.id must be EPIC", "epic.id"))

    work = data.get("work")
    if not isinstance(work, list) or not work:
        errors.append(_err("work", "work must be a non-empty list of waves", "work"))
        return errors

    wave_ids: list[str] = []
    wave_nums: list[int] = []
    all_implements: set[str] = set()

    for i, wave in enumerate(work):
        wpath = f"work[{i}]"
        if not isinstance(wave, dict):
            errors.append(_err("wave_shape", "wave must be a mapping", wpath))
            continue

        wid = wave.get("id")
        if not isinstance(wid, str) or not WAVE_ID_RE.fullmatch(wid):
            errors.append(_err("wave_id", f"wave id must match W{{n}}; got {wid!r}", f"{wpath}.id"))
            continue
        m = WAVE_ID_RE.fullmatch(wid)
        assert m is not None
        wnum = int(m.group(1))
        wave_ids.append(wid)
        wave_nums.append(wnum)

        wdeps = wave.get("depends_on", [])
        if wdeps is None:
            wdeps = []
        if not isinstance(wdeps, list):
            errors.append(_err("wave_depends_on", "depends_on must be a list", f"{wpath}.depends_on"))
            wdeps = []
        for j, dep in enumerate(wdeps):
            dpath = f"{wpath}.depends_on[{j}]"
            if not isinstance(dep, str) or not WAVE_ID_RE.fullmatch(dep):
                errors.append(_err("wave_depends_on", f"wave depends_on must be W*; got {dep!r}", dpath))
            else:
                dm = WAVE_ID_RE.fullmatch(dep)
                assert dm is not None
                if int(dm.group(1)) >= wnum:
                    errors.append(
                        _err(
                            "wave_depends_on_order",
                            f"wave {wid} may only depend on earlier waves; got {dep}",
                            dpath,
                        )
                    )

        tasks = wave.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            errors.append(_err("tasks", "each wave requires non-empty tasks[]", f"{wpath}.tasks"))
            tasks = []

        task_ids: set[str] = set()
        edges: dict[str, list[str]] = {}
        wave_files: list[str] = []
        for j, task in enumerate(tasks):
            tid = _validate_task(task, wave_id=wid, wave_num=wnum, index=j, errors=errors)
            if tid:
                if tid in task_ids:
                    errors.append(_err("task_id_dup", f"duplicate task id {tid}", f"{wpath}.tasks[{j}].id"))
                task_ids.add(tid)
                deps = task.get("depends_on") if isinstance(task, dict) else []
                if not isinstance(deps, list):
                    deps = []
                edges[tid] = [d for d in deps if isinstance(d, str)]
                impl = task.get("implements") if isinstance(task, dict) else []
                if isinstance(impl, list):
                    all_implements.update(str(x) for x in impl if isinstance(x, str))
            if isinstance(task, dict):
                for entry in task.get("files") or []:
                    if (
                        isinstance(entry, dict)
                        and entry.get("action") in {"create", "modify"}
                        and isinstance(entry.get("path"), str)
                    ):
                        wave_files.append(entry["path"])

        for tid, deps in edges.items():
            for dep in deps:
                if dep not in task_ids and TASK_ID_RE.fullmatch(dep):
                    errors.append(
                        _err(
                            "depends_on_missing",
                            f"dependency {dep} not found in wave {wid}",
                            f"work[{wid}].tasks",
                        )
                    )

        cycle = _topo_cycle(task_ids, edges)
        if cycle:
            errors.append(
                _err(
                    "depends_on_cycle",
                    f"task dependency cycle in {wid}: {' -> '.join(cycle)}",
                    f"work[{wid}].tasks",
                )
            )

        verification = wave.get("verification")
        if not isinstance(verification, dict):
            errors.append(
                _err("verification", "verification mapping is required", f"{wpath}.verification")
            )
        else:
            for layer in ("check", "unit"):
                val = verification.get(layer)
                if not isinstance(val, str) or not val.strip():
                    errors.append(
                        _err(
                            f"verification_{layer}",
                            f"verification.{layer} command is required",
                            f"{wpath}.verification.{layer}",
                        )
                    )
            _validate_live(
                verification.get("live"),
                wave_id=wid,
                verify_command=wave.get("verify_command"),
                errors=errors,
                wave_files=wave_files,
                base_path=base_path,
            )

    # Contiguous wave ordering W0..Wn
    if wave_nums:
        expected = list(range(len(wave_nums)))
        if sorted(wave_nums) != expected or wave_nums != expected:
            errors.append(
                _err(
                    "wave_order",
                    f"waves must be contiguous W0..W{{n}} in order; got {wave_ids}",
                    "work",
                )
            )

    if not all_implements:
        errors.append(_err("implements", "manifest has no REQ mappings on tasks", "work"))

    # Stable sort for determinism
    errors.sort(key=lambda e: (e.get("code", ""), e.get("path", ""), e.get("message", "")))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate prayog/v1 WorkManifest")
    parser.add_argument("path", type=Path, help="Plan markdown (§9) or standalone YAML")
    parser.add_argument("--json", action="store_true", help="Emit errors as JSON")
    parser.add_argument(
        "--base-path",
        type=Path,
        default=None,
        help="Workspace root for the live-verify coverage cross-check "
        "(resolves files[] and compares self-declared markers against "
        "live.covers). Omit to skip that check only.",
    )
    args = parser.parse_args(argv)

    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2

    text = args.path.read_text(encoding="utf-8")
    errors = validate_workmanifest(text, base_path=args.base_path)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    elif errors:
        print(f"WorkManifest contract FAILED ({len(errors)} error(s))\n")
        for err in errors:
            loc = f" @ {err['path']}" if err.get("path") else ""
            print(f"  [{err['code']}]{loc}: {err['message']}")
        return 1
    else:
        print("WorkManifest contract passed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
