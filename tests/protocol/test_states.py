from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SOURCE = REPOSITORY_ROOT / "packages" / "agent-protocol" / "src"
sys.path.insert(0, str(PACKAGE_SOURCE))

from agent_capability_protocol import InvalidTransitionError, validate_transition  # noqa: E402


class StateTransitionTests(unittest.TestCase):
    def test_transition_vectors(self) -> None:
        path = REPOSITORY_ROOT / "tests" / "vectors" / "v1" / "state-transitions.json"
        vectors = json.loads(path.read_text(encoding="utf-8"))
        for entity, current, target in vectors["valid"]:
            with self.subTest(entity=entity, current=current, target=target):
                validate_transition(entity, current, target)
        for entity, current, target in vectors["invalid"]:
            with self.subTest(entity=entity, current=current, target=target), self.assertRaises(
                InvalidTransitionError
            ):
                validate_transition(entity, current, target)

    def test_unknown_state_machine_is_rejected(self) -> None:
        with self.assertRaises(InvalidTransitionError):
            validate_transition("unknown", "created", "active")


if __name__ == "__main__":
    unittest.main()
