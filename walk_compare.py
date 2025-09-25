"""Utility for scanning digest files for protocol-related keywords.

The script walks ``ARCHIVAL_STACK`` for ``PR*_THREAD_DIGEST.md`` files, reads
the thread table contained in each, and records rows whose titles mention one
of the target keywords.  Results are appended to ``keyword_matches.csv`` with
the thread ID, digest path, title, and the keyword that triggered the match.

The behaviour can be customised via command-line arguments.  Run

``python walk_compare.py --help``

for details.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

DEFAULT_KEYWORDS = ["protocol", "SOP", "process", "naming"]


def _match_keyword(title: str, keywords: Iterable[str]) -> Optional[str]:
    """Return the first keyword found in ``title`` or ``None``."""

    lower_title = title.lower()
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in lower_title:
            return kw_lower
    return None


def _scan_file(path: Path, keywords: Iterable[str]) -> List[Tuple[str, str, str, str]]:
    """Return matches from a single digest file.

    Each match is a tuple of ``(thread_id, digest_path, title, keyword)``.
    """

    row_re = re.compile(r"^\|\s*(TH\d+)\s*\|\s*([^|]+?)\s*\|")
    matches: List[Tuple[str, str, str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            m = row_re.match(line)
            if not m:
                continue
            thread_id, title = m.groups()
            kw = _match_keyword(title, keywords)
            if kw:
                matches.append((thread_id, str(path), title.strip(), kw))
    return matches


def scan_digests(
    digest_dir: Path = Path("ARCHIVAL_STACK"),
    report_path: Path = Path("keyword_matches.csv"),
    keywords: Iterable[str] = DEFAULT_KEYWORDS,
) -> None:
    """Scan ``digest_dir`` for keyword matches and append them to ``report_path``."""

    digest_files = sorted(Path(digest_dir).glob("PR*_THREAD_DIGEST.md"))
    matches: List[Tuple[str, str, str, str]] = []
    for path in digest_files:
        matches.extend(_scan_file(path, keywords))

    # track existing entries to avoid duplicates
    existing = set()
    if report_path.exists():
        with report_path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing.add((row["thread_id"], row["digest_path"]))

    write_header = not report_path.exists()
    with report_path.open("a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["thread_id", "digest_path", "title", "keyword"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for thread_id, dpath, title, keyword in matches:
            key = (thread_id, dpath)
            if key not in existing:
                writer.writerow(
                    {
                        "thread_id": thread_id,
                        "digest_path": dpath,
                        "title": title,
                        "keyword": keyword,
                    }
                )
                existing.add(key)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan digest files for protocol-related keywords."
    )
    parser.add_argument(
        "--digest-dir", default="ARCHIVAL_STACK", help="Directory containing digest files"
    )
    parser.add_argument(
        "--report",
        default="keyword_matches.csv",
        help="CSV file to append matches to",
    )
    parser.add_argument(
        "--keywords",
        default=",".join(DEFAULT_KEYWORDS),
        help="Comma-separated list of keywords to search for",
    )
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    scan_digests(Path(args.digest_dir), Path(args.report), keywords)


if __name__ == "__main__":
    main()
