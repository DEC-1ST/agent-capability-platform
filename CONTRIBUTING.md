# Contributing

## Scope

The first milestone is provider-neutral protocol work. Pull requests must not
add real SSH, Feishu, Gateway, model-provider, credential, or privileged
supervisor behavior without a separate design and security review.

## Change rules

- Work on a feature branch and submit a pull request to `main`.
- Keep public examples synthetic and redacted.
- Do not weaken canonicalization, parameter binding, or fail-closed tests.
- Do not treat an unavailable or safety-filtered reviewer as a pass.
- Add a test vector for every protocol or state-machine change.
- Report actual test counts; do not hard-code a historical count.

## Local checks

```powershell
$env:PYTHONPATH = "packages/agent-protocol/src"
python -m unittest discover -s tests -p "test_*.py"
python tools/repository_gate.py
python -m compileall -q packages tests tools
```

## Security reports

Do not open a public issue for a vulnerability. Follow `SECURITY.md` and use
GitHub's private vulnerability reporting.
