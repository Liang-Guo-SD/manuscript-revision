# Harness File Templates

Create only the files the current phase requires. Fill each file with project-specific content; do not copy templates verbatim.

## MANUSCRIPT_ANALYSIS.md

```markdown
# Manuscript Analysis

## Document Summary

- Title:
- Language: [EN / ZH / Mixed]
- Source format: [Markdown / LaTeX / PDF-converted / DOCX-converted]
- Total sections:
- Approximate word count:
- Analysis date:

## Section Inventory

| ID | Title | Words | Format | Claim class | Evidence | Formal dev | Source integrity | Notation |
|---|---|---|---|---|---|---|---|---|
| CH01-S01 | | | | adequate/partial/absent | | | | |

## Faithfulness Anchors

**CH01:** [Author's central argument in their own terms — one or two sentences from the text]

## Priority List (sections with 2+ absent dimensions)

1. CH__-S__ — absent: [dimensions]

## Unresolved Items

- [ ] Sections that could not be read: [list]
- [ ] Sections requiring format conversion: [list]
- [ ] Citations flagged as source-needed: [count and locations]

## Author Approval

- [ ] Author has reviewed and approved this analysis before revision begins.
- Approval date:
- Notes:
```

## REVISION_PLAN.md

```markdown
# Revision Plan

## Faithfulness Constraint

[One paragraph stating the author's intent for the whole manuscript. This is the non-negotiable bound for all transforms. Changes that violate this constraint require explicit author approval before proceeding.]

## Language and Humanizer Configuration

- Language: [EN / ZH / Mixed]
- Humanizer (EN): [blader/humanizer vX.X / claude-native / not applicable]
- Humanizer (ZH): [op7418/Humanizer-zh vX.X / claude-native / not applicable]
- Target register: [e.g., graduate-level technical / practitioner guide / public explainer]

## Chapter Status Overview

One row per source file (chapter). Update as sessions complete.

| Chapter | File | Sections | Transform status | Humanize status | Conflicts |
|---|---|---|---|---|---|
| CH01 | chapter-01.md | 4 | planned/in-progress/complete | planned/in-progress/complete | 0 |

## Per-Section Transform Plan

One row per section across all chapters. Sections from different files share this table; the `CH` prefix in the ID identifies which file they belong to.

| ID | Title | Priority | Claim class | Evidence | Formal dev | Source integrity | Notation | Humanize | Notes |
|---|---|---|---|---|---|---|---|---|---|
| CH01-S01 | | high/med/low | transform/skip | transform/skip | transform/skip | flag/skip | transform/skip | EN/ZH/skip | |

## Approval

- [ ] Author has reviewed and approved this plan before transforms begin.
- Approval date:
- Notes:
```

## REVISION_LOG.md

Append-only. Never delete or edit a prior entry. To supersede a decision, add a new entry referencing the old one.

```markdown
# Revision Log

## Transform Pass

| Date | Section ID | Gate | Action | Faithfulness status | Status |
|---|---|---|---|---|---|
| YYYY-MM-DD | CH01-S01 | claim-classification | Added [hypothesis] marker to paragraph 4 | preserved | complete |
| YYYY-MM-DD | CH02-S03 | formal-development | [FAITHFULNESS CONFLICT] — escalated to author | conflict | open |

## Humanize Pass

| Date | Section ID | Gate | Action | Tool | Status |
|---|---|---|---|---|---|
| YYYY-MM-DD | CH01-S01 | humanize | Processed; 2 passages restored for rigor | humanizer-en v1.2.0 | complete |

## Faithfulness Conflicts

| ID | Section | Original claim | Rigor problem | Options | Resolution | Resolved date |
|---|---|---|---|---|---|---|
| FC-001 | CH02-S03 | | | | | |
```

## PROGRESS.md

```markdown
# Progress

## Current Phase

[Ingest / Diagnose / Plan / Transform / Humanize / Validate / Complete]

## Chapter-Level Summary

| Chapter | File | Sections | Transform | Humanize |
|---|---|---|---|---|
| CH01 | chapter-01.md | 4 | complete | complete |
| CH02 | chapter-02.md | 5 | in-progress | planned |
| CH03 | chapter-03.md | 3 | planned | planned |

*Update this table at the end of each session. It is the fastest way to see where the whole manuscript stands.*

## Last Completed Item

[Section ID and action, or phase name]

## Current Active Item

[Exact section ID and action in progress]

## Next Exact Item

[Section ID and action — precise enough that a fresh agent can resume without this conversation]

## Blockers

- [ ] [Description and what is needed to unblock]

## Validator Status

Last run: [date]
Result: [pass / fail / not yet run]
Outstanding issues: [list or "none"]

## Session Log

| Date | Phase | Completed | Notes |
|---|---|---|---|
| YYYY-MM-DD | | | |
```
