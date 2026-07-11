#!/usr/bin/env python3
"""Deterministic PM-to-engineering handoff state and ripple rules."""

from __future__ import annotations

from typing import Any


EFFECTIVE_STATES = {
    "draft",
    "pending_review",
    "approved",
    "stale",
    "blocked",
    "superseded",
}

RIPPLE_ACTIONS = {
    "continue",
    "open",
    "hold",
    "close",
    "re-draft",
    "re-feasibility",
    "re-plan",
    "human-decision",
}


def effective_state(
    *,
    current_head_sha: str,
    current_prd_digest: str,
    artifact: dict[str, Any],
    approvals: list[dict[str, Any]],
    blocked: bool = False,
    superseded: bool = False,
) -> str:
    """Return the fail-closed effective state for the latest impact map."""
    if superseded:
        return "superseded"
    if blocked:
        return "blocked"
    if not artifact:
        return "draft"

    matching_approval = next(
        (
            review
            for review in reversed(approvals)
            if review.get("state") == "APPROVED"
            and review.get("commit_id") == current_head_sha
            and review.get("map_revision") == artifact.get("map_revision")
            and review.get("prd_digest") == artifact.get("source_prd_digest")
        ),
        None,
    )

    if artifact.get("source_prd_digest") != current_prd_digest:
        return "stale"
    if matching_approval is not None:
        return "approved"
    if approvals:
        return "stale"
    return "pending_review"


def ripple_actions(
    *,
    previous: dict[str, Any] | None,
    current: dict[str, Any] | None,
    in_flight: str = "none",
    dependency_order_changed: bool = False,
) -> list[str]:
    """Return ordered downstream actions for one repository."""
    previous_status = previous.get("status") if previous else None
    current_status = current.get("status") if current else None

    if current_status in {None, "deferred", "not_affected", "blocked"}:
        if in_flight == "merged":
            return ["human-decision"]
        if in_flight != "none":
            return ["hold", "close"]
        return ["hold"]

    if previous_status != "affected" and current_status == "affected":
        return ["open"]

    if previous_status == "affected" and current_status == "affected":
        if previous.get("scope_digest") != current.get("scope_digest"):
            actions = ["re-draft", "re-feasibility"]
            if in_flight in {"plan", "implementation"}:
                actions.append("re-plan")
            return actions
        if dependency_order_changed:
            return ["re-plan"]
        return ["continue"]

    return ["hold"]
