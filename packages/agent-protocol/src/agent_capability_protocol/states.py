"""Normative state-transition checks for protocol v1."""

from __future__ import annotations

TRANSITIONS: dict[str, dict[str, frozenset[str]]] = {
    "task": {
        "created": frozenset({"assigned", "cancelled"}),
        "assigned": frozenset({"running", "blocked", "cancelled"}),
        "running": frozenset({"review_required", "blocked", "cancelled"}),
        "review_required": frozenset({"changes_requested", "passed", "blocked"}),
        "changes_requested": frozenset({"running", "cancelled"}),
        "passed": frozenset({"approval_required", "completed"}),
        "approval_required": frozenset({"completed", "blocked", "cancelled"}),
        "blocked": frozenset({"assigned", "running", "cancelled"}),
        "completed": frozenset(),
        "cancelled": frozenset(),
    },
    "capability": {
        "requested": frozenset({"pending_approval", "denied", "cancelled"}),
        "pending_approval": frozenset({"active", "denied", "expired", "cancelled"}),
        "active": frozenset({"released", "revoked", "expired"}),
        "released": frozenset(),
        "revoked": frozenset(),
        "expired": frozenset(),
        "denied": frozenset(),
        "cancelled": frozenset(),
    },
    "approval": {
        "pending": frozenset({"approved", "rejected", "expired", "superseded"}),
        "approved": frozenset({"consumed", "revoked", "expired", "superseded"}),
        "consumed": frozenset(),
        "rejected": frozenset(),
        "revoked": frozenset(),
        "expired": frozenset(),
        "superseded": frozenset(),
    },
    "lease": {
        "pending": frozenset({"active", "revoked", "expired"}),
        "active": frozenset({"released", "revoked", "expired"}),
        "released": frozenset(),
        "revoked": frozenset(),
        "expired": frozenset(),
    },
    "handoff": {
        "draft": frozenset({"sealed", "rejected"}),
        "sealed": frozenset({"verified", "rejected"}),
        "verified": frozenset({"accepted", "rejected"}),
        "accepted": frozenset(),
        "rejected": frozenset(),
    },
}


class InvalidTransitionError(ValueError):
    """Raised when a state transition is unknown or forbidden."""


def validate_transition(entity: str, current: str, target: str) -> None:
    """Raise when *current* cannot transition to *target* for *entity*."""

    states = TRANSITIONS.get(entity)
    if states is None:
        raise InvalidTransitionError(f"unknown state machine: {entity}")
    if current not in states:
        raise InvalidTransitionError(f"unknown {entity} state: {current}")
    if target not in states[current]:
        raise InvalidTransitionError(f"forbidden {entity} transition: {current} -> {target}")
