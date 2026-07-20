"""Offline, read-only GitHub capability adapter used by protocol tests.

This adapter deliberately has no network client and no mutation methods. It
models the boundary that a future GitHub App or broker must satisfy.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Literal

from .validation import SchemaValidationError, validate_document

ResourceType = Literal["repository", "issue", "pull_request", "check_run"]

_RESOURCE_SCHEMAS: dict[ResourceType, str] = {
    "repository": "github-repository.schema.json",
    "issue": "github-issue.schema.json",
    "pull_request": "github-pull-request.schema.json",
    "check_run": "github-check-run.schema.json",
}
_RESOURCE_ID_FIELDS: dict[ResourceType, str] = {
    "repository": "repository_id",
    "issue": "issue_id",
    "pull_request": "pull_request_id",
    "check_run": "check_run_id",
}


class GitHubCapabilityError(ValueError):
    """Raised when an offline GitHub capability request is invalid."""


@dataclass(frozen=True)
class CapabilityObservation:
    """A read result with an explicit no-side-effect marker."""

    operation: Literal["read"]
    resource_type: ResourceType
    resource_id: str
    document: dict[str, Any]
    side_effect: Literal["none"] = "none"


class FakeGitHubAdapter:
    """Serve validated GitHub fixtures without network or mutation access."""

    def __init__(self, documents: dict[ResourceType, list[dict[str, Any]]]) -> None:
        self._resources: dict[ResourceType, dict[str, dict[str, Any]]] = {}
        for resource_type, schema_name in _RESOURCE_SCHEMAS.items():
            entries = documents.get(resource_type, [])
            index: dict[str, dict[str, Any]] = {}
            for document in entries:
                try:
                    validate_document(schema_name, document)
                except SchemaValidationError as exc:
                    raise GitHubCapabilityError(
                        f"invalid {resource_type} fixture"
                    ) from exc
                resource_id = document[_RESOURCE_ID_FIELDS[resource_type]]
                if resource_id in index:
                    raise GitHubCapabilityError(f"duplicate {resource_type} resource")
                index[resource_id] = deepcopy(document)
            self._resources[resource_type] = index

        repository_ids = set(self._resources["repository"])
        for resource_type in ("issue", "pull_request", "check_run"):
            for document in self._resources[resource_type].values():
                if document["repository_id"] not in repository_ids:
                    raise GitHubCapabilityError(
                        f"{resource_type} references an unknown repository"
                    )

    def read(self, resource_type: ResourceType, resource_id: str) -> CapabilityObservation:
        """Return a defensive copy of one fixture and record no side effect."""

        if resource_type not in _RESOURCE_SCHEMAS:
            raise GitHubCapabilityError(f"unsupported GitHub resource: {resource_type}")
        document = self._resources[resource_type].get(resource_id)
        if document is None:
            raise GitHubCapabilityError(f"unknown {resource_type} resource: {resource_id}")
        return CapabilityObservation(
            operation="read",
            resource_type=resource_type,
            resource_id=resource_id,
            document=deepcopy(document),
        )

    def list(self, resource_type: ResourceType) -> tuple[CapabilityObservation, ...]:
        """Return all fixtures of one type in deterministic ID order."""

        if resource_type not in _RESOURCE_SCHEMAS:
            raise GitHubCapabilityError(f"unsupported GitHub resource: {resource_type}")
        return tuple(
            self.read(resource_type, resource_id)
            for resource_id in sorted(self._resources[resource_type])
        )
