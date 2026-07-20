"""ACP Canonical JSON v1.

The profile is deliberately narrower than general JSON. Rejecting ambiguous
values is easier to verify across runtimes than trying to repair them after a
capability or approval has been signed.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any

MAX_SAFE_INTEGER = 9_007_199_254_740_991


class CanonicalizationError(ValueError):
    """Raised when a value is outside ACP Canonical JSON v1."""


def _reject_float(value: str) -> None:
    raise CanonicalizationError(f"floating-point values are forbidden: {value!r}")


def _reject_constant(value: str) -> None:
    raise CanonicalizationError(f"non-finite numeric value is forbidden: {value!r}")


def _pairs_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"duplicate object key: {key!r}")
        result[key] = value
    return result


def _validate_string(value: str, *, label: str) -> str:
    if unicodedata.normalize("NFC", value) != value:
        raise CanonicalizationError(f"{label} must use Unicode NFC normalization")
    return value


def _validate(value: Any, *, path: str = "$") -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if not -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER:
            raise CanonicalizationError(f"integer at {path} exceeds the safe range")
        return value
    if isinstance(value, float):
        raise CanonicalizationError(f"floating-point value at {path} is forbidden")
    if isinstance(value, str):
        return _validate_string(value, label=f"string at {path}")
    if isinstance(value, Mapping):
        validated: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(f"object key at {path} is not a string")
            _validate_string(key, label=f"object key at {path}")
            validated[key] = _validate(item, path=f"{path}.{key}")
        return validated
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [_validate(item, path=f"{path}[{index}]") for index, item in enumerate(value)]
    raise CanonicalizationError(f"unsupported value at {path}: {type(value).__name__}")


def loads_strict(text: str | bytes | bytearray) -> Any:
    """Parse JSON while rejecting duplicate keys, floats, and non-finite values."""

    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs_without_duplicates,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except CanonicalizationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CanonicalizationError("invalid JSON input") from exc
    return _validate(value)


def canonical_dumps(value: Any) -> str:
    """Return the ACP Canonical JSON v1 representation of *value*."""

    validated = _validate(value)
    return json.dumps(
        validated,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def canonical_bytes(value: Any) -> bytes:
    """Return canonical UTF-8 bytes."""

    return canonical_dumps(value).encode("utf-8")


def canonical_hash(value: Any) -> str:
    """Return a tagged SHA-256 digest of the canonical bytes."""

    return f"sha256:{hashlib.sha256(canonical_bytes(value)).hexdigest()}"
