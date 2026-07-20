from __future__ import annotations

import json
import sys
import unicodedata
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SOURCE = REPOSITORY_ROOT / "packages" / "agent-protocol" / "src"
sys.path.insert(0, str(PACKAGE_SOURCE))

from agent_capability_protocol import (  # noqa: E402
    CanonicalizationError,
    canonical_dumps,
    canonical_hash,
    loads_strict,
)


class CanonicalJsonTests(unittest.TestCase):
    def test_public_vectors(self) -> None:
        vector_path = REPOSITORY_ROOT / "tests" / "vectors" / "v1" / "canonicalization.json"
        vectors = json.loads(vector_path.read_text(encoding="utf-8"))
        for case in vectors["cases"]:
            with self.subTest(case=case["name"]):
                value = loads_strict(case["input_json"])
                self.assertEqual(canonical_dumps(value), case["canonical_json"])
                self.assertEqual(canonical_hash(value), case["digest"])

    def test_duplicate_keys_are_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            loads_strict('{"same":1,"same":2}')

    def test_floats_are_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            loads_strict('{"value":1.5}')

    def test_non_finite_numbers_are_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            loads_strict('{"value":NaN}')

    def test_unsafe_integers_are_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_dumps({"value":9_007_199_254_740_992})

    def test_non_nfc_strings_are_rejected(self) -> None:
        decomposed = unicodedata.normalize("NFD", "é")
        with self.assertRaises(CanonicalizationError):
            canonical_dumps({"value": decomposed})


if __name__ == "__main__":
    unittest.main()
