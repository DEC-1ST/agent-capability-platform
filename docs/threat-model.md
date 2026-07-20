# Threat model

## Assets

- capability scope, workspace commit, and expiry;
- approval decisions and authority proofs;
- audit and handoff integrity;
- agent task and artifact confidentiality;
- private deployment credentials and runtime state.

## Adversaries

- a compromised or confused role agent;
- a malicious task payload or adapter;
- a stale or replayed approval;
- a compromised bridge or supervisor;
- a contributor attempting public/private repository contamination;
- a dependency or GitHub Actions supply-chain compromise;
- an unavailable reviewer incorrectly represented as a pass.

## Primary mitigations

1. Canonical JSON rejects ambiguous signed inputs.
2. Parameter binding includes task, capability, workspace, commit, request,
   approval, policy, profile, and lifetime.
3. Scope and binding hashes are checked independently of caller-provided
   labels.
4. State transitions are explicit and fail closed.
5. Public examples are synthetic and scanned for credential-like material.
6. The privileged supervisor is a separate trust boundary, not a Python
   module imported by an agent.
7. Approval and reviewer outcomes distinguish unavailable from passed.
8. GitHub branch protection and security scanning protect the public supply
   chain; CI action versions should be pinned before production use.

## Residual risks

- Schema validation does not verify signatures or trust roots.
- A transport can still duplicate a remote side effect; exactly-once is not
  implied by a local lease.
- A root supervisor can observe more than a normal agent and requires a
  separate deployment review.
- CI and package registries remain external dependencies and need provenance,
  lock files, and update review.

## Live integration gate

No live SSH, Feishu, Gateway, staging, or production integration is authorized
by a protocol schema PASS. Those operations require an independently scoped
approval and a reviewed implementation of the privileged trust boundary.
