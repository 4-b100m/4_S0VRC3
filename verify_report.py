import csv
import hashlib
from io import BytesIO
from pathlib import Path
import zipfile

def hash_path(parts):
    path = Path(parts[0])
    if not path.exists():
        return None
    if len(parts) == 1:
        data = path.read_bytes()
        return hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(path) as zf:
        return hash_in_zip(zf, parts[1:])

def hash_in_zip(zf, parts):
    try:
        data = zf.read(parts[0])
    except KeyError:
        return None
    if len(parts) == 1:
        return hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(BytesIO(data)) as inner:
        return hash_in_zip(inner, parts[1:])

def main():
    mismatches = []
    with open('walk_report.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parts = row['path'].split('!')
            digest = hash_path(parts)
            if digest != row['sha256']:
                mismatches.append(row['path'])
    if mismatches:
        print('Integrity check failed for:')
        for p in mismatches:
            print(f' - {p}')
    else:
        print('All hashes match')

if __name__ == '__main__':
    main()
