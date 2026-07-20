# Architecture

## First principle

An agent must not receive an unbounded identity. It receives a capability
whose subject, action, workspace, commit, policy, lifetime, and approval are
bound together and can be audited later.

## Planes

```text
Control plane
  owner / approval authority
        |
        v
  capability broker ---- audit ledger
        |
        v
  task orchestrator ---- policy and handoff state

Execution plane
  role agent ---- bridge ---- Codex / Claude Code / local worker
        |
        v
  workspace / artifact store / test child

Privileged boundary (separate process and release)
  root launcher / supervisor / pidfd / kernel event source
```

The protocol package does not implement any of these transports. It defines
the data that crosses their boundaries.

## Trust boundaries

1. The owner or approval authority signs a decision; an agent cannot approve
   its own capability.
2. The broker checks the canonical parameter binding before issuing a lease.
3. The bridge may transport a task but cannot widen its scope or expiry.
4. A workspace commit is an input to the binding, not a value the worker may
   rewrite after approval.
5. The privileged supervisor is not trusted merely because a process reports
   that it is a supervisor; it requires an independently provisioned trust
   root and attestation contract.

## Public and private planes

The public repository contains contracts, synthetic examples, tests, and
documentation. A private deployment contains credentials, real identities,
runtime state, private logs, databases, and authority keys. Handoff packages
crossing the boundary must be explicitly selected, redacted, hashed, and
reviewed.

## Message lifecycle

```text
task request
  -> capability request
  -> approval decision
  -> bounded lease
  -> task execution
  -> audit events and artifacts
  -> sealed handoff
  -> independent review
```

The protocol does not claim remote exactly-once side effects. Adapters must
state their delivery semantics explicitly.
