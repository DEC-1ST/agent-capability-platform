from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.repository_gate import FIXTURE_ROOTS, scan_paths, tracked_files  # noqa: E402


class RepositoryGateTests(unittest.TestCase):
    def test_public_vectors_are_clean(self) -> None:
        self.assertEqual(scan_paths(FIXTURE_ROOTS), [])

    def test_tracked_repository_content_is_clean(self) -> None:
        self.assertEqual(scan_paths(tracked_files()), [])

    def test_credential_like_fixture_is_rejected_without_echoing_value(self) -> None:
        synthetic = "AK" + "IA" + ("A" * 16)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.txt"
            path.write_text(synthetic, encoding="utf-8")
            findings = scan_paths([path])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "aws-access-key")


if __name__ == "__main__":
    unittest.main()
