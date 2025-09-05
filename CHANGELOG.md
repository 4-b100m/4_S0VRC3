# CHANGELOG.md  
_This file documents structural changes, naming updates, and vault configuration decisions for `4_S0VRC3`._

---

### [v2025-09-05] Repository fact checker

**Date:** 2025-09-05
**Status:** ✅ Active
**Changes:**
- Added `fact_check_repo.py` to flag filename/content mismatches and duplicate files.
- Generated `fact_check_report.csv` summarizing detected issues.

---

### [v2025-08-29] Keyword walk integrity check

**Date:** 2025-08-29
**Status:** ✅ Active
**Changes:**
- Extended `walk_compare.py` to compute SHA256 hashes and traverse nested zip archives.
- Added `verify_report.py` to confirm hashes in `walk_report.csv`.
- Regenerated `walk_report.csv` with checksum records for all scanned files.

---

### [v2025-08-28] Vault walk and keyword audit

**Date:** 2025-08-28
**Status:** ✅ Active
**Changes:**
- Added `walk_compare.py` utility to traverse the vault and log protocol/SOP/naming/process keyword matches.
- Generated `walk_report.csv` capturing 312 files with name/content comparisons.

---

### [v2025-05-04] Initialization of `4_S0VRC3`

**Date:** 2025-05-04 21:43:10
**Status:** ✅ Locked & Active  
**Author:** Anthony James Padavano  
**Location:** `/Users/anthonyjamespadavano/Documents/4_S0VRC3`

---

### 🔁 Structural Changes
- Renamed vault from `4JP` → `4_S0VRC3` (read: “A Source”)
- Changed Obsidian Sync target to this vault
- Designated `4_S0VRC3` as new root of recursive system
- Vault moved out of `_4JP_`; now functions as **topmost** terminal
- Obsidian iCloud support deprecated — replaced by **Obsidian Sync**

---

### 🗂️ Folder/Content Notes
- `_4JP_` now exists **conceptually as a sublayer** (optional future use)
- Contents map in README updated accordingly
- Git integration flagged for future setup
- Plugins prompting API warnings (OpenAI model) — noted for configuration

---

### 🧭 Next To-Do Items
- [ ] Update README and vault_state to reflect new hierarchy
- [ ] Resolve GPT-4 plugin API key issue
- [ ] Build THREAD_DIGEST archive system
