# ADR 0002: Use a restricted canonical JSON profile

## Decision

Protocol v1 uses ACP Canonical JSON v1: sorted keys, UTF-8, no floats, safe
integers, NFC strings, strict duplicate-key rejection, and UTC-second timestamps.

## Rationale

A rejected ambiguous value is safer than a language runtime silently serializing
it differently before an approval or artifact hash is computed.

## Consequence

Future implementations in other languages must implement the same profile and
pass the published vectors before they can sign or verify protocol documents.
