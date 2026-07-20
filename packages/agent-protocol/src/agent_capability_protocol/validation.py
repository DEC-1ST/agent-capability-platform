"""JSON Schema loading and validation for protocol v1."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError
from referencing import Registry, Resource


class SchemaValidationError(ValueError):
    """Raised when a schema or protocol document is invalid."""


@lru_cache(maxsize=1)
def _schema_documents() -> dict[str, dict[str, Any]]:
    directory = files("agent_capability_protocol").joinpath("schemas", "v1")
    documents: dict[str, dict[str, Any]] = {}
    for path in directory.iterdir():
        if path.name.endswith(".schema.json"):
            documents[path.name] = json.loads(path.read_text(encoding="utf-8"))
    return documents


@lru_cache(maxsize=1)
def _registry() -> Registry:
    resources = []
    for schema in _schema_documents().values():
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validate_schema_set() -> None:
    """Validate every bundled schema against JSON Schema 2020-12."""

    try:
        for schema in _schema_documents().values():
            Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise SchemaValidationError("invalid bundled JSON Schema") from exc


def validate_document(schema_name: str, document: Any) -> None:
    """Validate *document* against a bundled schema filename."""

    schema = _schema_documents().get(schema_name)
    if schema is None:
        raise SchemaValidationError(f"unknown schema: {schema_name}")
    try:
        Draft202012Validator(schema, registry=_registry()).validate(document)
    except ValidationError as exc:
        path = ".".join(str(item) for item in exc.absolute_path) or "$"
        raise SchemaValidationError(f"schema validation failed at {path}: {exc.message}") from exc
