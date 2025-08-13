
# NAME_STRUCTURE_OVERVIEW.md

This document formalizes the naming conventions, UID structure, and style logic across the RE:GE_OS system.

---

## ✅ NAMING CONVENTIONS

### 📁 Folder & File Names (System Safe)
- All lowercase
- Only `a–z`, numbers, `_`, and `-` allowed
- No colons `:`, pipes `|`, brackets `[]`, or special symbols
- Examples:
  - `met4morf_os`
  - `rege_os`
  - `char_engine`
  - `canon_timeline`
  - `qvv33r`

### 🪞 Display Titles (UI/Markdown Readable)
- Stylized using caps, leet, underscores, colons (optional)
- Examples:
  - `Qvv33R`
  - `MET4MORF-0_S_`
  - `RE:GE_OS`

---

## 🧷 UID SYSTEM (Folder / Project ID)
Each major folder/project receives a UID in format `[AA00]`:
- 2-letter prefix based on function or cluster
- 2-digit index

### Examples:
| UID   | Folder Name     | Use Case                        |
|-------|------------------|----------------------------------|
| `RG01`| `rege_os`        | Core system protocol            |
| `MT01`| `met4morf_os`    | Myth-based transformation engine |
| `QV01`| `qvv33r`         | Queer narrative and theory       |
| `BL01`| `abloom`         | Philosophical creative expansion |

---

## 🔁 LEGACY TO CANONICAL MAP

| Legacy Name                  | Canonical Folder  |
|-----------------------------|-------------------|
| `:: job = {application}`     | `canon_timeline`  |
| `SY.ST3MS__TH30RY`           | `rege_os`         |
| `M3T4-M0RF-0_S_`             | `met4morf_os`     |
| `GRINDER`                    | `gr1nd3r`         |
| `QUEER`                      | `qvv33r`          |
| `floating_points`            | `canon_timeline`  |
| `etCETER4`                   | `etceter4`        |
| `⊢judge arbitrate...⊣`       | `theory_crit`     |
| `☿:🜁🜂...` (symbolic)         | `naming_spells`   |

---

## 🔧 Additional Notes
- Each folder includes a `README.md` with UID and symbolic notes
- All symbolic/stylized names are tracked separately in a vault map file (`SYST3M__M4P.md`)
- Dataview queries can extract all `UID:` YAML fields to auto-generate nav trees

