"""Deterministic integrity checks for protocol v1 documents.

These checks establish structural consistency. They do not establish trust in
an issuer or verify an Ed25519 signature; those responsibilities belong to the
approval authority and verifier that own the relevant trust root.
"""

from __future__ import annotations

import hmac
from datetime import UTC, datetime
from typing import Any

from .canonical import canonical_hash
from .validation import SchemaValidationError, validate_document


class IntegrityError(ValueError):
    """Raised when a document's declared integrity bindings do not match."""


def hash_projection(document: dict[str, Any], *, omit: frozenset[str]) -> str:
    """Hash a top-level projection without the named fields."""

    return canonical_hash({key: value for key, value in document.items() if key not in omit})


def parameter_binding_hash(binding: dict[str, Any]) -> str:
    """Return the canonical hash used to bind a request and its artifacts."""

    validate_document("parameter-binding.schema.json", binding)
    return canonical_hash(binding)


def _parse_timestamp(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError as exc:
        raise IntegrityError("invalid UTC timestamp") from exc


def verify_parameter_binding(
    document: dict[str, Any],
    *,
    expected: dict[str, Any] | None = None,
) -> None:
    """Verify the binding hash, lifetime ordering, and optional external pins."""

    binding = document.get("parameter_binding")
    declared = document.get("parameter_binding_hash")
    if not isinstance(binding, dict) or not isinstance(declared, str):
        raise IntegrityError("document is missing its parameter binding")

    actual = parameter_binding_hash(binding)
    if not hmac.compare_digest(actual, declared):
        raise IntegrityError("parameter binding hash mismatch")
    if _parse_timestamp(binding["not_before"]) >= _parse_timestamp(binding["expires_at"]):
        raise IntegrityError("parameter binding lifetime must be positive")

    if expected is not None:
        for field, value in expected.items():
            if field not in binding or binding[field] != value:
                raise IntegrityError(f"parameter binding does not match expected {field}")


def verify_document_integrity(
    schema_name: str,
    document: dict[str, Any],
    *,
    expected_binding: dict[str, Any] | None = None,
) -> None:
    """Validate a document and all integrity bindings defined for its schema."""

    try:
        validate_document(schema_name, document)
    except SchemaValidationError as exc:
        raise IntegrityError(str(exc)) from exc

    if "parameter_binding" in document:
        verify_parameter_binding(document, expected=expected_binding)

    if schema_name == "capability.schema.json":
        if not hmac.compare_digest(canonical_hash(document["scope"]), document["scope_hash"]):
            raise IntegrityError("capability scope hash mismatch")
    elif schema_name == "handoff.schema.json":
        if not hmac.compare_digest(
            canonical_hash(document["artifacts"]), document["artifact_manifest_hash"]
        ):
            raise IntegrityError("handoff artifact manifest hash mismatch")
    elif schema_name == "audit-event.schema.json":
        actual = hash_projection(document, omit=frozenset({"event_hash"}))
        if not hmac.compare_digest(actual, document["event_hash"]):
            raise IntegrityError("audit event hash mismatch")
