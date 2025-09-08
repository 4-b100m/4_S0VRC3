# Pull Request Automation Agents

This repository now includes `github_agents.py`, which defines two
helpers for streamlining pull request workflow:

- **ReviewResponder** posts an acknowledgement comment whenever a
  review is requested.
- **PRTestDebugger** reports failing GitHub Actions jobs so you can
  easily see which checks need attention.  Each failure is linked
  directly to its job page for quick debugging.  It also includes a
  convenience method for fetching the most recent workflow run of a PR
  and commenting any failures automatically.

Both agents inherit from a shared `GitHubAgent` that wires up an
authenticated `requests.Session`.  A `GITHUB_TOKEN` with permission to
comment on issues is required; the classes raise a clear error if the
token is missing.  You can also supply a different `api_root` for
GitHub Enterprise installations.

## Usage

```
from github_agents import ReviewResponder, PRTestDebugger

responder = ReviewResponder(repo="owner/name")
responder.post_acknowledgement(pr_number=42)

debugger = PRTestDebugger(repo="owner/name")
failed = debugger.failing_jobs(run_id=123456789)
debugger.comment_failures(pr_number=42, jobs=failed)

# or handle the latest run in one call
debugger.report_latest_failures(pr_number=42)
```

Set the `GITHUB_TOKEN` environment variable before running these
snippets:

```
export GITHUB_TOKEN="<your token>"
```

Tokens only need `repo` scope for private repositories or `public_repo`
for public ones.
