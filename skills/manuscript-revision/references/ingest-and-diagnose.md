# Ingest and Diagnose

Use this reference during Pass 1 to load an existing manuscript, inventory its sections, and produce a structured gap analysis.

## Accepted Input Formats

| Format | Approach |
|---|---|
| Markdown (.md) | Read directly; use headings as section boundaries |
| Plain text (.txt) | Read directly; infer sections from blank-line clusters or numbered headings |
| LaTeX (.tex) | Read directly; use `\section`, `\subsection` as boundaries |
| PDF | Ask user to export to text or Markdown; do not hallucinate content from unreadable PDF |
| DOCX | Ask user to export to Markdown via Pandoc: `pandoc input.docx -o output.md` |
| Jupyter Notebook | Read .ipynb; treat Markdown cells as prose sections, code cells as evidence artifacts |

Never infer content the file does not contain. If a section is illegible or truncated, mark it `UNREADABLE` in the analysis and flag it to the author.

## Section Inventory

Assign each section a stable ID with the pattern `CHxx-Syy` (chapter-section) or `Syy` for flat documents. Record:

- `id`: stable identifier
- `title`: heading text or inferred label
- `word_count`: approximate
- `format`: prose / list / mixed / code-heavy / figure-heavy
- `status`: readable / partial / unreadable

Run `python3 scripts/diagnose.py <manuscript-dir>` to scaffold the inventory automatically for Markdown and text files.

## Gap Analysis Dimensions

Score each section on five dimensions. Use three levels: **adequate** (criterion is met), **partial** (criterion is present but incomplete), **absent** (criterion is not addressed).

### 1. Claim Classification

Is each claim clearly labeled as one of:
- **Established result** — widely accepted in the field; citation not required unless contested
- **Sourced empirical claim** — depends on external data or literature; source must be cited
- **Interpretation** — the author's reading of evidence; must be marked as such
- **Hypothesis or proposal** — the author's conjecture; must be explicitly flagged

Partial: claims exist but are not distinguished from each other. Absent: all claims are stated as fact without classification.

### 2. Evidence Match

Does the evidence provided match the strength of the claim?

- Strong claims (universal, causal) require strong evidence (controlled experiment, proof, systematic review).
- Weaker claims (illustrative, plausible) may use examples, analogies, or pilot data if labeled correctly.

Partial: some claims have supporting evidence; others are asserted without it. Absent: no evidence is offered for any non-trivial claim.

### 3. Formal Development

Are key terms defined before use? Are central results derived or justified rather than stated? Are assumptions and validity domains declared?

Partial: some terms defined; others used without definition. Absent: no definitions; results stated without derivation or justification.

### 4. Source Integrity

Are citations present where needed? Are cited sources real, traceable, and appropriately scoped?

Do not verify citations during diagnosis. Flag sections that make empirical or literature-dependent claims without citations as `source-needed`. Flag sections that cite sources that cannot be verified on inspection as `source-unverified`.

### 5. Notation Hygiene

Are symbols and abbreviations introduced before use? Are they used consistently throughout the section? Do they conflict with standard usage in the field?

Partial: most symbols defined; some introduced without explanation. Absent: symbols used without definition; inconsistent usage.

## Faithfulness Anchor

For each chapter (or the whole document if flat), record the author's central argument in one or two sentences using only language present in the text. Do not infer intent beyond what is stated.

Format:
```
CH01 faithfulness anchor: [author's stated argument in their own terms]
```

This anchor is the primary constraint for all subsequent transforms. A revision that changes the faithfulness anchor requires explicit author approval.

## MANUSCRIPT_ANALYSIS.md Output

After completing the inventory and gap analysis, write `MANUSCRIPT_ANALYSIS.md` with:

1. **Document summary:** title, language, format, total sections, word count estimate.
2. **Section table:** one row per section — ID, title, word count, format, and scores for each of the five dimensions.
3. **Faithfulness anchors:** one per chapter.
4. **Priority list:** sections scored `absent` on two or more dimensions, listed by section ID.
5. **Unresolved items:** unreadable sections, missing citations flagged for author input, format conversion notes.

Present the analysis to the author and ask for approval before creating `REVISION_PLAN.md`. Do not begin transforms without approval.
