"""Provider-neutral protocol primitives for agent capability workflows."""

from .canonical import (
    CanonicalizationError,
    canonical_bytes,
    canonical_dumps,
    canonical_hash,
    loads_strict,
)
from .github_fake import CapabilityObservation, FakeGitHubAdapter, GitHubCapabilityError
from .integrity import (
    IntegrityError,
    hash_projection,
    parameter_binding_hash,
    verify_document_integrity,
    verify_parameter_binding,
)
from .states import InvalidTransitionError, validate_transition
from .validation import SchemaValidationError, validate_document, validate_schema_set

__all__ = [
    "CanonicalizationError",
    "CapabilityObservation",
    "FakeGitHubAdapter",
    "GitHubCapabilityError",
    "IntegrityError",
    "InvalidTransitionError",
    "SchemaValidationError",
    "canonical_bytes",
    "canonical_dumps",
    "canonical_hash",
    "hash_projection",
    "loads_strict",
    "parameter_binding_hash",
    "validate_document",
    "validate_schema_set",
    "validate_transition",
    "verify_document_integrity",
    "verify_parameter_binding",
]
