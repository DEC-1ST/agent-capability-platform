# State transitions

The following transitions are normative for protocol v1. Any omitted edge is
forbidden and must fail closed.

## Task

| Current | Allowed next states |
| --- | --- |
| created | assigned, cancelled |
| assigned | running, blocked, cancelled |
| running | review_required, blocked, cancelled |
| review_required | changes_requested, passed, blocked |
| changes_requested | running, cancelled |
| passed | approval_required, completed |
| approval_required | completed, blocked, cancelled |
| blocked | assigned, running, cancelled |
| completed | none |
| cancelled | none |

## Capability

| Current | Allowed next states |
| --- | --- |
| requested | pending_approval, denied, cancelled |
| pending_approval | active, denied, expired, cancelled |
| active | released, revoked, expired |
| released/revoked/expired/denied/cancelled | none |

## Approval

| Current | Allowed next states |
| --- | --- |
| pending | approved, rejected, expired, superseded |
| approved | consumed, revoked, expired, superseded |
| consumed/rejected/revoked/expired/superseded | none |

## Lease

| Current | Allowed next states |
| --- | --- |
| pending | active, revoked, expired |
| active | released, revoked, expired |
| released/revoked/expired | none |

## Handoff

| Current | Allowed next states |
| --- | --- |
| draft | sealed, rejected |
| sealed | verified, rejected |
| verified | accepted, rejected |
| accepted/rejected | none |
