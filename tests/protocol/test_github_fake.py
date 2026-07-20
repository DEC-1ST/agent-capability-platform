from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SOURCE = REPOSITORY_ROOT / "packages" / "agent-protocol" / "src"
sys.path.insert(0, str(PACKAGE_SOURCE))

from agent_capability_protocol import (  # noqa: E402
    FakeGitHubAdapter,
    GitHubCapabilityError,
)


class FakeGitHubAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        examples = REPOSITORY_ROOT / "examples" / "protocol-v1"

        def load(name: str) -> dict:
            return json.loads((examples / name).read_text(encoding="utf-8"))

        cls.repository = load("github-repository.json")
        cls.issue = load("github-issue.json")
        cls.pull_request = load("github-pull-request.json")
        cls.check_run = load("github-check-run.json")

    def _adapter(self) -> FakeGitHubAdapter:
        return FakeGitHubAdapter(
            {
                "repository": [self.repository],
                "issue": [self.issue],
                "pull_request": [self.pull_request],
                "check_run": [self.check_run],
            }
        )

    def test_read_returns_no_side_effect_observation(self) -> None:
        result = self._adapter().read("pull_request", "github.pr.5")
        self.assertEqual(result.operation, "read")
        self.assertEqual(result.side_effect, "none")
        self.assertEqual(result.document["state"], "merged")

    def test_read_returns_defensive_copy(self) -> None:
        adapter = self._adapter()
        result = adapter.read("repository", "github.dec-1st.agent-capability-platform")
        result.document["name"] = "mutated"
        self.assertEqual(
            adapter.read("repository", "github.dec-1st.agent-capability-platform").document["name"],
            "agent-capability-platform",
        )

    def test_list_is_sorted_and_deterministic(self) -> None:
        result = self._adapter().list("issue")
        self.assertEqual([item.resource_id for item in result], ["github.issue.1"])

    def test_unknown_resource_is_rejected(self) -> None:
        with self.assertRaises(GitHubCapabilityError):
            self._adapter().read("issue", "github.issue.404")

    def test_duplicate_resource_is_rejected(self) -> None:
        with self.assertRaises(GitHubCapabilityError):
            FakeGitHubAdapter(
                {
                    "repository": [self.repository, dict(self.repository)],
                    "issue": [],
                    "pull_request": [],
                    "check_run": [],
                }
            )

    def test_unknown_repository_reference_is_rejected(self) -> None:
        issue = dict(self.issue)
        issue["repository_id"] = "github.unknown.repository"
        with self.assertRaises(GitHubCapabilityError):
            FakeGitHubAdapter(
                {
                    "repository": [self.repository],
                    "issue": [issue],
                    "pull_request": [],
                    "check_run": [],
                }
            )


if __name__ == "__main__":
    unittest.main()
