# Agent Capability Platform

A scoped, auditable capability platform for multi-agent development workflows.

This repository currently contains the provider-neutral `agent-protocol` v1
milestone. It defines canonical envelopes, capability/task/approval/lease/audit
and handoff documents, deterministic hashes, state transitions, and public
boundary documentation.

It deliberately does **not** connect to Hermes, Codex, Claude Code, Feishu,
SSH, a Gateway, a production database, or a privileged supervisor. Those are
future adapters with separate trust and release boundaries.

## Status

Early public protocol milestone. The schemas and examples are contracts, not a
production authorization service. A valid schema document is not proof that an
issuer, approval, workspace, or runtime is trusted.

## Local development

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
$env:PYTHONPATH = "packages/agent-protocol/src"
python -m unittest discover -s tests -p "test_*.py"
python tools/repository_gate.py
```

## Repository layout

```text
packages/agent-protocol/  Provider-neutral schemas and validation
examples/                 Synthetic, redacted protocol documents
tests/                    Canonicalization, schema, integrity, and state tests
docs/                     Architecture, threat model, protocol, and boundaries
integrations/             Future optional adapters; no live adapters yet
services/                 Future privileged supervisor boundary
deploy/                   Future deployment templates
```

## Security boundary

Never commit secrets, `.env` files, real identities, production paths, raw
logs, databases, session state, or private authority keys. See
[`SECURITY.md`](SECURITY.md), [`docs/threat-model.md`](docs/threat-model.md),
and [`docs/repository-boundaries.md`](docs/repository-boundaries.md).
