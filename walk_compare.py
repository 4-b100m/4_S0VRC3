import csv
import re
from pathlib import Path

KEYWORDS = ["protocol", "SOP", "process", "naming"]

def scan_digests(digest_dir: str = "ARCHIVAL_STACK", report_path: str = "keyword_matches.csv") -> None:
    digest_files = sorted(Path(digest_dir).glob("PR*_THREAD_DIGEST.md"))
    row_re = re.compile(r"^\|\s*(TH\d+)\s*\|\s*([^|]+?)\s*\|")
    matches = []
    for path in digest_files:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                m = row_re.match(line)
                if not m:
                    continue
                thread_id, title = m.groups()
                title_lower = title.lower()
                if any(keyword.lower() in title_lower for keyword in KEYWORDS):
                    matches.append((thread_id, str(path)))
    report_file = Path(report_path)
    write_header = not report_file.exists()
    with report_file.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["thread_id", "digest_path"])
        writer.writerows(matches)

if __name__ == "__main__":
    scan_digests()
