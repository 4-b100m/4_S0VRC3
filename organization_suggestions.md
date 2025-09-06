# ORGANIZATION_SUGGESTIONS

Recommendations for cleaning up duplicates and clarifying the vault layout.

## Duplicate File Candidates
- **THREAD_PROJECT_CROSSWALK files** (`THREAD_PROJECT_CROSSWALK.md`, `THREAD_PROJECT_CROSSWALK_TAGGED.md`, `THREAD_PROJECT_CROSSWALK_FINAL.csv`)
  - Keep the `.csv` as canonical; derive human-readable views from it.
- **FOLDER_CATALOG_FINAL files** (`FOLDER_CATALOG_FINAL.md`, `FOLDER_CATALOG_FINAL.csv`)
  - Consolidate into one source and auto-generate the alternate format.
- **FOLDER_COLLAPSE_PLANNER.csv** vs. **FINAL_FOLDER_COLLAPSE_SNAPSHOT.csv**
  - Archive planner once snapshot is finalized or merge into a single timeline.
- **Untitled canvas files** (`Untitled.canvas`, `Untitled 1.canvas`)
  - Remove or move into a dedicated `drafts/` area.
- **ChatGPT instruction notes** (`ChatGPT-Disable Canvas Tool.md`, `ChatGPT-Merge Project Folders.md`)
  - Combine into a single reference or relocate to `notes/`.
- **Zipped artifacts** (`; RE•GE•OS ; RG•01 ;.zip`, `README_NOTES.zip`)
  - Extract and file under `archive/`; remove the zip once contents are placed.

## Suggested Folder Structure
- `docs/` – READMEs, guides, naming conventions, and root_overview.
- `datasets/` – CSV tables like crosswalks and catalogs.
- `projects/` – active project directories.
- `templates/` – reusable starter files.
- `archive/` – historical snapshots and zipped exports.
- `tags/` – tag dictionaries or mappings.

Adopting these steps will reduce clutter and make the vault easier to navigate.
