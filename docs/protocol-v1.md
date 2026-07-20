# Protocol v1

## Canonical JSON profile

ACP Canonical JSON v1 is a deliberately restricted profile:

- UTF-8 output;
- object keys sorted lexicographically;
- no insignificant whitespace;
- no duplicate object keys;
- no floating-point values or non-finite numbers;
- integers limited to the interoperable safe range `[-2^53+1, 2^53-1]`;
- strings must already be Unicode NFC;
- timestamps are UTC seconds in `YYYY-MM-DDTHH:MM:SSZ` form;
- digests are tagged lower-case SHA-256 values such as
  `sha256:0123...`.

The profile is intentionally narrower than general JSON. A canonicalizer must
reject an ambiguous value rather than silently normalize it after signing.

## Parameter binding

Every task, capability, approval, lease, envelope, and handoff binds the same
minimum identity set:

```text
task_id
capability_id
workspace_id
workspace_commit
request_id
approval_id
policy_version
scope_hash
adapter_profile
not_before
expires_at
```

The canonical parameter binding is hashed and the resulting digest is carried
by the enclosing document. The digest is also an input to approval signatures,
artifact manifests, and handoff evidence. A caller-supplied value must not
replace the independently expected binding during verification.

## Proof versus structure

JSON Schema proves shape. The protocol reference implementation additionally
checks declared binding, scope, artifact-manifest, and audit-event hashes. It
does not verify an authority signature or install a trust root; those belong to
the broker/supervisor implementation.

## Reviewer semantics

`passed`, `failed`, and `unavailable` are distinct outcomes. An unavailable or
safety-filtered reviewer is never converted to `passed`.
