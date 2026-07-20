# Agent Protocol

`agent-capability-protocol` contains the provider-neutral contracts used by the
Agent Capability Platform. Version 1 defines deterministic serialization,
schema validation, state transitions, and integrity bindings. It does not
connect to agents, platforms, networks, or privileged services.

The public API is intentionally small:

- `canonical_dumps()` and `canonical_hash()` implement ACP Canonical JSON v1.
- `validate_document()` validates a document against a bundled JSON Schema.
- `validate_transition()` checks protocol state transitions.

Protocol semantics are documented in [`docs/protocol-v1.md`](../../docs/protocol-v1.md).
