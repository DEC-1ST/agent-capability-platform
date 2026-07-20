"""Fail closed when public examples contain credential-like material."""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = (
    REPOSITORY_ROOT / "examples",
    REPOSITORY_ROOT / "tests" / "vectors",
)

FORBIDDEN_FILENAMES = frozenset(
    {
        ".env",
        "auth.json",
        "authorized_keys",
        "id_dsa",
        "id_ecdsa",
        "id_ed25519",
        "id_rsa",
        "state.db",
    }
)

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("feishu-identity", re.compile(r"\b(?:ou|oc)_[A-Za-z0-9]{16,}\b")),
    (
        "websocket-credential",
        re.compile(r"(?i)(?:access_key|ticket|device_id|conn_id)=[^\s&\"']+"),
    ),
    (
        "credential-assignment",
        re.compile(
            r"(?im)^\s*(?:[A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|API_KEY)[A-Z0-9_]*)\s*=\s*\S+"
        ),
    ),
)


@dataclass(frozen=True)
class Finding:
    path: Path
    rule: str


def _iter_files(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if root.is_file():
            yield root
        elif root.is_dir():
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    yield path


def scan_paths(roots: Iterable[Path]) -> list[Finding]:
    """Return credential-like findings without returning matched values."""

    findings: list[Finding] = []
    for path in _iter_files(roots):
        if path.name in FORBIDDEN_FILENAMES:
            findings.append(Finding(path=path, rule="forbidden-filename"))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            findings.append(Finding(path=path, rule="non-public-or-unreadable-content"))
            continue
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(path=path, rule=name))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    roots = tuple(args.paths) or DEFAULT_ROOTS
    findings = scan_paths(roots)
    for finding in findings:
        try:
            display = finding.path.resolve().relative_to(REPOSITORY_ROOT)
        except ValueError:
            display = Path("<external-test-input>")
        print(f"{display}: blocked by {finding.rule}")
    if findings:
        print(f"repository_gate=failed findings={len(findings)}")
        return 1
    print("repository_gate=passed findings=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
