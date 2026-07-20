# ADR 0003: Keep privileged supervision outside the agent runtime

## Decision

Root launcher, retained pidfd, kernel event observation, recovery anchors,
authority keys, and final attestations are separate from the normal agent and
protocol packages.

## Rationale

An agent that can install or redefine its own authority would be able to turn a
local task capability into a platform-wide privilege. A separate process and
release boundary makes that escalation explicit and auditable.

## Consequence

The public protocol can be developed and tested with fake interfaces, but no
fake result is treated as live authority.
