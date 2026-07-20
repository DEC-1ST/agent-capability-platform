# GitHub Capability v1

This document defines the public protocol boundary for GitHub-backed work. It
does not implement a GitHub client, store credentials, or authorize writes.

## Resource model

The first resource payloads are:

- `github-repository`: repository identity and visibility;
- `github-issue`: a task intake record;
- `github-pull-request`: proposed code change and its immutable refs;
- `github-check-run`: CI status attached to a commit.

Each payload is standalone and can be carried inside an ACP task, audit event,
or handoff. The core envelope message types remain unchanged; GitHub is an
adapter payload, not a new trust domain.

## Capability boundary

The initial capability names are intentionally split by risk:

```text
github.repository.read
github.issue.read
github.pull_request.read
github.check_run.read
github.branch.propose
github.pull_request.propose
github.comment.propose
github.pull_request.merge          # approval required
github.release.publish             # approval required
```

The public protocol only describes these capabilities. A future adapter must
bind every request to the repository, workspace commit, policy version, scope,
and expiry in `parameter_binding`.

## Credential boundary

No GitHub token, App private key, webhook secret, installation ID, or raw API
response belongs in this repository's examples, schemas, handoffs, or logs.
Live access should use a repository-scoped GitHub App or equivalent broker. The
adapter must return redacted ACP payloads and append an audit event for every
write attempt.

## Approval boundary

Reading repository state and proposing a branch or pull request may be
automated. Merge, release, deletion, and deployment remain separate approved
capabilities. A successful CI check is evidence, not authorization.
