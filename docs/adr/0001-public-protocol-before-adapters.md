# ADR 0001: Publish the protocol before provider adapters

## Decision

The first public milestone contains only provider-neutral schemas, canonical
hash vectors, state tables, boundary documentation, threat model, and CI gates.

## Rationale

Provider adapters encode credentials, transport retries, external side effects,
and platform-specific identity. Publishing them before the protocol is stable
would couple the public API to a deployment and make security review harder.

## Consequence

SSH, Feishu, Gateway, model-provider, and privileged-supervisor integrations
remain separate follow-up milestones.
