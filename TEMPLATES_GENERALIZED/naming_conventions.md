# General Naming Conventions

This document provides neutral, universally-applicable naming conventions for files, folders, and system components.

## General Principles

1. **Clarity**: Names should clearly indicate purpose and content
2. **Consistency**: Follow consistent patterns across the system
3. **Portability**: Avoid special characters that may cause issues across systems
4. **Scalability**: Use patterns that work for both small and large collections
5. **Searchability**: Use descriptive keywords that enable easy searching

## File and Folder Naming

### Standard Characters
- Use only: `a-z`, `A-Z`, `0-9`, `_` (underscore), `-` (hyphen)
- Avoid: Special symbols, spaces, accented characters, emojis
- Start with letters, not numbers or symbols

### Case Conventions
- **snake_case**: Preferred for most files and folders (`project_template`, `meeting_notes`)
- **kebab-case**: Alternative for web-friendly names (`project-template`, `meeting-notes`)
- **PascalCase**: For class names or formal titles (`ProjectTemplate`, `MeetingNotes`)
- **UPPER_CASE**: For constants or environment-specific items (`CONFIG_FILE`, `PROD_DB`)

### Folder Structure Examples
```
project_documentation/
├── templates/
├── procedures/
├── protocols/
├── meeting_notes/
└── archive/
```

## Unique Identifiers (UIDs)

### Format Options
- **Sequential**: `DOC-001`, `PRJ-042`, `SOP-015`
- **Date-based**: `20240811-001`, `2024-W32-001`
- **Hierarchical**: `SYS.DB.001`, `PROC.HR.005`
- **Semantic**: `USER-ONBOARD-001`, `BACKUP-DAILY-003`

### UID Guidelines
- Choose one format and use consistently
- Include leading zeros for proper sorting (`001` not `1`)
- Use meaningful prefixes that indicate document type
- Reserve ranges for different purposes

## Document Categories

### Common Prefixes
| Prefix | Meaning | Example |
|--------|---------|---------|
| `SOP` | Standard Operating Procedure | `SOP-001_user_onboarding` |
| `PROTO` | Protocol | `PROTO-005_incident_response` |
| `TEMP` | Template | `TEMP-003_project_charter` |
| `DOC` | General Documentation | `DOC-012_system_overview` |
| `PROC` | Process | `PROC-008_code_review` |
| `GUIDE` | User Guide | `GUIDE-002_new_employee` |

## Version Control

### Semantic Versioning
- **Format**: `MAJOR.MINOR.PATCH` (e.g., `2.1.3`)
- **Major**: Breaking changes or complete rewrites
- **Minor**: New features or significant additions
- **Patch**: Bug fixes or minor corrections

### Document Versioning
- **Format**: `v1.0`, `v1.1`, `v2.0`
- **Include version in filename**: `project_template_v2.1.md`
- **Maintain version history in document metadata**

## Status Indicators

### Common Status Values
- `Draft` - Work in progress
- `Review` - Under review
- `Active` - Current and in use
- `Archived` - No longer active but preserved
- `Deprecated` - Being phased out

### Status in Filenames (Optional)
- `user_guide_DRAFT_v1.0.md`
- `backup_protocol_ACTIVE_v2.3.md`

## Metadata Standards

### YAML Frontmatter Template
```yaml
---
uid: "<unique-identifier>"
title: "<human-readable-title>"
version: "<version-number>"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD" 
status: "<Draft/Review/Active/Archived/Deprecated>"
author: "<author-name>"
category: "<document-category>"
tags: ["<tag1>", "<tag2>", "<tag3>"]
---
```

## Archive and Backup Naming

### Archive Folders
- `archive_YYYY/` - Annual archives
- `archive_YYYY_MM/` - Monthly archives
- `superseded/` - Old versions of current documents

### Backup Files
- `filename_backup_YYYYMMDD.ext`
- `filename_v1_backup.ext`
- `filename_pre_update_20240811.ext`

## Search and Discovery

### Tag Strategy
- Use consistent, descriptive tags
- Combine functional and categorical tags
- Examples: `["process", "hr", "onboarding", "template"]`

### Keywords in Names
- Include key terms that people might search for
- Balance specificity with brevity
- Use domain-relevant terminology

## Platform-Specific Considerations

### Web/URL-Friendly
- Use lowercase with hyphens: `user-onboarding-guide`
- Avoid special characters: `%`, `&`, `?`, `#`
- Keep URLs concise and readable

### Database-Friendly
- Use consistent casing (preferably lowercase)
- Avoid SQL reserved words
- Use underscores for readability: `user_account_table`

### Cross-Platform
- Avoid case-sensitive duplicates
- Use portable character sets
- Test names on target systems

## Examples by Use Case

### Standard Operating Procedures
- `sop_001_user_account_creation.md`
- `sop_backup_daily_procedure_v2.1.md`
- `incident_response_protocol_active.md`

### Templates and Forms
- `template_project_charter_v1.5.md`
- `form_expense_report_2024.xlsx`
- `checklist_deployment_standard.md`

### Documentation
- `user_guide_system_overview_v3.0.md`
- `technical_specs_api_documentation.md`
- `training_manual_new_employee.pdf`

---

## Implementation Notes

1. **Migration**: When updating existing systems, create a mapping from old to new naming conventions
2. **Training**: Ensure all team members understand and follow the conventions
3. **Automation**: Use scripts or tools to validate naming conventions
4. **Review**: Periodically review and refine conventions based on usage patterns

This naming system is designed to be adaptable to different organizations, projects, and contexts while maintaining clarity and consistency.