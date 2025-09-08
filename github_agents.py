"""Utilities for interacting with GitHub pull requests.

This module defines lightweight agents that help automate
common pull request workflows:

* ``ReviewResponder`` can post a response when review requests
  are triggered.
* ``PRTestDebugger`` can fetch log information for failing
  checks and comment a summary back on the pull request.

Both classes rely on the GitHub REST API and require a
personal access token with appropriate repository permissions.
The token is expected in the ``GITHUB_TOKEN`` environment
variable.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Iterable, List

import requests

API_ROOT = "https://api.github.com"


@dataclass
class GitHubAgent:
    """Base class that wires up authenticated GitHub requests."""

    repo: str
    token: str | None = None
    api_root: str = API_ROOT

    def __post_init__(self) -> None:  # pragma: no cover - simple wiring
        if not self.token:
            self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github+json",
            }
        )


@dataclass
class ReviewResponder(GitHubAgent):
    """Agent that posts a comment acknowledging review requests."""

    def post_acknowledgement(self, pr_number: int, message: str | None = None) -> dict:
        """Post a short acknowledgement comment on a pull request.

        Parameters
        ----------
        pr_number : int
            Pull request number.
        message : str, optional
            Comment body. Defaults to a simple thank‑you message.
        """

        if message is None:
            message = "Thanks for the review request!"
        url = f"{self.api_root}/repos/{self.repo}/issues/{pr_number}/comments"
        response = self._session.post(url, json={"body": message}, timeout=10)
        response.raise_for_status()
        return response.json()


@dataclass
class Job:
    """A minimal representation of a workflow job."""

    name: str
    url: str


@dataclass
class PRTestDebugger(GitHubAgent):
    """Agent that summarises failing test information."""

    def failing_jobs(self, run_id: int) -> List[Job]:
        """Return failing jobs for a workflow run."""

        url = f"{self.api_root}/repos/{self.repo}/actions/runs/{run_id}/jobs"
        response = self._session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [
            Job(name=j["name"], url=j["html_url"])
            for j in data.get("jobs", [])
            if j.get("conclusion") == "failure"
        ]

    def comment_failures(self, pr_number: int, jobs: Iterable[Job]) -> dict:
        """Comment a summary of failing jobs on the pull request."""

        lines = [f"- [{job.name}]({job.url})" for job in jobs]
        body = "\n".join(lines) or "All jobs passed."
        url = f"{self.api_root}/repos/{self.repo}/issues/{pr_number}/comments"
        response = self._session.post(url, json={"body": body}, timeout=10)
        response.raise_for_status()
        return response.json()

    def latest_run_id(self, pr_number: int) -> int | None:
        """Return the most recent workflow run id for a pull request.

        This convenience helper looks up the PR's head SHA and then finds
        the latest workflow run for that commit.  ``None`` is returned if no
        runs are found, which typically means Actions has not been triggered.
        """

        pr_url = f"{self.api_root}/repos/{self.repo}/pulls/{pr_number}"
        pr_response = self._session.get(pr_url, timeout=10)
        pr_response.raise_for_status()
        sha = pr_response.json()["head"]["sha"]

        runs_url = f"{self.api_root}/repos/{self.repo}/actions/runs"
        runs_response = self._session.get(
            runs_url, params={"per_page": 1, "head_sha": sha}, timeout=10
        )
        runs_response.raise_for_status()
        data = runs_response.json()
        runs = data.get("workflow_runs", [])
        return runs[0]["id"] if runs else None

    def report_latest_failures(self, pr_number: int) -> dict | None:
        """Comment failing jobs for the most recent workflow run of a PR.

        The method fetches the latest workflow run for ``pr_number``, gathers
        its failing jobs (if any) and posts a summarised comment back on the
        pull request.  ``None`` is returned when no workflow run exists yet.
        """

        run_id = self.latest_run_id(pr_number)
        if run_id is None:
            return None
        jobs = self.failing_jobs(run_id)
        return self.comment_failures(pr_number, jobs)

