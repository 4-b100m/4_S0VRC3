"""Fact-check repository file names vs contents and detect duplicates.

Scans repository using ``walk_compare.analyze`` and produces a
``fact_check_report.csv`` summarizing any mismatches between filenames and
content keywords as well as duplicate files (matching SHA256 hashes).
"""

import csv
from collections import defaultdict
from pathlib import Path
from walk_compare import analyze


def main() -> None:
    report, max_depth = analyze('.')

    mismatches = []
    hashes: dict[str, list[str]] = defaultdict(list)
    for item in report:
        if item['mismatch']:
            mismatches.append(item['path'])
        hashes[item['sha256']].append(item['path'])

    duplicates = {digest: paths for digest, paths in hashes.items() if len(paths) > 1}

    out_path = Path('fact_check_report.csv')
    with out_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['issue_type', 'path', 'details'])
        for path in mismatches:
            writer.writerow(['name/content mismatch', path, ''])
        for digest, paths in duplicates.items():
            first = paths[0]
            for other in paths[1:]:
                writer.writerow(['duplicate', other, f'same as {first}'])

    print(f'Max depth: {max_depth}')
    print(f'Mismatches: {len(mismatches)}')
    print(f'Duplicate groups: {len(duplicates)}')
    print(f'Report written to {out_path}')


if __name__ == '__main__':
    main()
