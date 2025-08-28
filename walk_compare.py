import csv
import glob
from pathlib import Path

# Files to parse
CROSSWALK_FILE = Path('THREAD_PROJECT_CROSSWALK.md')
DIGEST_GLOB = 'ARCHIVAL_STACK/PR*_THREAD_DIGEST.md'
OUTPUT_FILE = Path('thread_protocol_index.csv')

def parse_markdown_table(file_path):
    """Parse markdown table rows for thread entries.

    Expects rows formatted like:
    | THxxx | Title | timestamp | ... |
    Returns list of dicts with thread_id, title, timestamp.
    """
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('| TH'):
                # remove leading/trailing '|'
                parts = [p.strip() for p in line.strip('|').split('|')]
                if len(parts) >= 3:
                    rows.append({
                        'thread_id': parts[0],
                        'title': parts[1],
                        'timestamp': parts[2],
                        'source_file': str(file_path)
                    })
    return rows

def build_index():
    rows = []
    # parse crosswalk
    if CROSSWALK_FILE.exists():
        rows.extend(parse_markdown_table(CROSSWALK_FILE))
    # parse digest files
    for digest_file in sorted(glob.glob(DIGEST_GLOB)):
        rows.extend(parse_markdown_table(Path(digest_file)))
    # write CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['thread_id', 'title', 'timestamp', 'source_file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    build_index()
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
