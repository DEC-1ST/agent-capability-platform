# Repository boundaries

## Public repository

The public repository may contain:

- protocol schemas and validators;
- canonicalization and hash test vectors;
- fake adapters and synthetic examples;
- state-transition tables;
- threat model and deployment guidance;
- CI and repository security gates.

## Private deployment

Keep these outside the public repository:

- `.env` and API credentials;
- Feishu App IDs, Open IDs, Chat IDs, and secrets;
- model or Sub2API keys;
- SSH keys and authority private keys;
- production/staging logs, databases, sessions, and memories;
- server topology and private paths;
- root-owned trust-root and recovery-anchor contents.

## Handoff rule

An artifact crosses from a private deployment only after an owner-selected
redaction pass, safe-archive extraction check, content scan, and SHA-256
manifest. A path or filename alone is not evidence that an artifact is safe.

## Non-goals

This repository is not a backup of a Hermes installation, a production
configuration repository, or a credential distribution mechanism.
