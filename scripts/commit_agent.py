#!/usr/bin/env python3
"""CommitAgent critiques commit messages and supports safe merges."""

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import List


class CommitAgent:
    """Critiques commit messages and merges branches safely."""

    def run(self, args: List[str]) -> str:
        """Run a command and return stdout."""
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Command failed: {' '.join(args)}\n"
                f"Return code: {e.returncode}\n"
                f"Stdout: {e.stdout.strip() if e.stdout else ''}\n"
                f"Stderr: {e.stderr.strip() if e.stderr else ''}"
            ) from e

    def get_commits(self, base: str = "origin/main") -> List[str]:
        """Return commit messages on current branch not in base."""
        try:
            log = self.run(["git", "log", f"{base}..HEAD", "--pretty=%s"])
        except subprocess.CalledProcessError:
            return []
        return [line.strip() for line in log.splitlines() if line.strip()]

    def critique(self, messages: List[str]) -> List[str]:
        """Provide simple critiques for commit messages."""
        critiques = []
        for message in messages:
            issues: List[str] = []
            if len(message) < 10:
                issues.append("too short")
            if len(message) > 72:
                issues.append("too long")
            if message and not message[0].isupper():
                issues.append("should start with uppercase")
            if not message.endswith("."):
                issues.append("should end with period")
            if issues:
                critiques.append(f"'{message}' -> {', '.join(issues)}")
        return critiques

    def ensure_clean_worktree(self) -> None:
        """Raise if working tree has uncommitted changes."""
        status = self.run(["git", "status", "--porcelain"])
        if status:
            raise RuntimeError("Working tree is not clean:\n" + status)

    def safe_merge(self, source: str, target: str = "main") -> None:
        """Perform a merge with basic safety checks."""
        self.ensure_clean_worktree()
        self.run(["git", "checkout", target])
        self.run(["git", "merge", "--no-ff", source])
        self.run(["git", "checkout", source])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Critique commit messages and perform safe merges."
    )
    parser.add_argument(
        "--base",
        default="origin/main",
        help="base branch to compare commits against",
    )
    parser.add_argument(
        "--merge",
        nargs=2,
        metavar=("SOURCE", "TARGET"),
        help="merge SOURCE into TARGET safely",
    )
    args = parser.parse_args()

    agent = CommitAgent()
    if args.merge:
        source, target = args.merge
        agent.safe_merge(source, target)
        return 0

    commits = agent.get_commits(args.base)
    critiques = agent.critique(commits)
    if critiques:
        print("Commit message issues found:")
        for critique in critiques:
            print("-", critique)
        return 1
    print("All commit messages look good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
