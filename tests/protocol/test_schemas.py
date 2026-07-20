from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SOURCE = REPOSITORY_ROOT / "packages" / "agent-protocol" / "src"
sys.path.insert(0, str(PACKAGE_SOURCE))

from agent_capability_protocol import (  # noqa: E402
    IntegrityError,
    canonical_hash,
    validate_document,
    validate_schema_set,
    verify_document_integrity,
)


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.examples = REPOSITORY_ROOT / "examples" / "protocol-v1"

    def _load(self, name: str) -> dict:
        return json.loads((self.examples / name).read_text(encoding="utf-8"))

    def test_schema_set_is_valid(self) -> None:
        validate_schema_set()

    def test_parameter_binding_example(self) -> None:
        validate_document("parameter-binding.schema.json", self._load("parameter-binding.json"))

    def test_document_examples_and_integrity(self) -> None:
        cases = {
            "task.json": "task.schema.json",
            "capability.json": "capability.schema.json",
            "approval.json": "approval.schema.json",
            "lease.json": "lease.schema.json",
            "audit-event.json": "audit-event.schema.json",
            "handoff.json": "handoff.schema.json",
            "redacted-envelope.json": "canonical-envelope.schema.json",
        }
        for filename, schema in cases.items():
            with self.subTest(filename=filename):
                verify_document_integrity(schema, self._load(filename))

    def test_parameter_binding_external_pins(self) -> None:
        task = self._load("task.json")
        verify_document_integrity(
            "task.schema.json",
            task,
            expected_binding={
                "workspace_commit": "0123456789abcdef0123456789abcdef01234567",
                "scope_hash": task["parameter_binding"]["scope_hash"],
                "expires_at": "2026-01-01T01:00:00Z",
            },
        )

    def test_substituted_binding_is_rejected(self) -> None:
        task = self._load("task.json")
        task["parameter_binding"]["workspace_commit"] = "f" * 40
        with self.assertRaises(IntegrityError):
            verify_document_integrity("task.schema.json", task)

    def test_substituted_scope_is_rejected(self) -> None:
        capability = self._load("capability.json")
        capability["scope"]["actions"].append("execute")
        with self.assertRaises(IntegrityError):
            verify_document_integrity("capability.schema.json", capability)

    def test_invalid_calendar_date_is_rejected_by_schema(self) -> None:
        task = self._load("task.json")
        task["created_at"] = "2026-02-31T00:00:00Z"
        with self.assertRaises(IntegrityError):
            verify_document_integrity("task.schema.json", task)

    def test_invalid_uri_is_rejected_by_schema(self) -> None:
        handoff = self._load("handoff.json")
        handoff["artifacts"][0]["uri"] = "not-a-uri"
        with self.assertRaises(IntegrityError):
            verify_document_integrity("handoff.schema.json", handoff)

    def test_duplicate_artifact_id_is_rejected(self) -> None:
        handoff = self._load("handoff.json")
        duplicate = dict(handoff["artifacts"][0])
        duplicate["name"] = "other.txt"
        handoff["artifacts"].append(duplicate)
        with self.assertRaises(IntegrityError):
            verify_document_integrity("handoff.schema.json", handoff)

    def test_duplicate_resource_id_is_rejected(self) -> None:
        capability = self._load("capability.json")
        duplicate = dict(capability["scope"]["resources"][0])
        duplicate["mode"] = "read"
        capability["scope"]["resources"].append(duplicate)
        with self.assertRaises(IntegrityError):
            verify_document_integrity("capability.schema.json", capability)

    def test_audit_event_hash_uses_projection(self) -> None:
        event = self._load("audit-event.json")
        declared = event.pop("event_hash")
        self.assertEqual(canonical_hash(event), declared)


if __name__ == "__main__":
    unittest.main()
