# Scientific Rigor Transforms

Use this reference during Pass 2 to plan and execute per-section rigor transforms. Read `MANUSCRIPT_ANALYSIS.md` and `REVISION_PLAN.md` before making any changes.

## The Faithfulness Constraint

Every transform must preserve the author's faithfulness anchor for that chapter. Before applying any change, ask:

> Does this change preserve what the author is arguing, or does it alter the argument?

If a rigor fix would require changing the argument (e.g., a claim is scientifically incorrect and cannot be preserved), do not resolve it silently. Record a `[FAITHFULNESS CONFLICT]` entry in `REVISION_LOG.md` with:
- the section ID
- the original claim
- the rigor problem
- the options (weaken the claim, add a caveat, delete, or escalate to author)

Leave it `open` until the author decides. Do not proceed past a conflict on the same section.

## Transform Rules by Dimension

### Claim Classification Transforms

**Absent or partial:** Insert a classification marker at the first substantive use of each claim type.

Standard markers:
- Established results: no marker needed unless the claim is contested — then add a citation.
- Sourced empirical: add `[citation needed: <what kind of source>]` as a placeholder if no source is present.
- Interpretations: add phrasing such as "This suggests...", "One reading is...", or "The author interprets this as..." where the text currently asserts without attribution.
- Hypotheses: add "We propose...", "This work conjectures...", or an explicit hypothesis label.

Do not change the content of a claim when classifying it. Classification is labeling, not editing.

### Evidence Match Transforms

**Absent:** Flag the claim with `[evidence needed: <type>]`. Do not invent evidence.

**Partial:** Strengthen the framing to match the evidence available:
- If strong evidence is cited but the claim overstates it, weaken the claim language to fit.
- If weak evidence is cited but the claim is modest, add a note on generalizability limits.

Evidence types by claim strength:

| Claim type | Minimum evidence |
|---|---|
| Universal or causal | Proof, controlled experiment, or systematic meta-analysis |
| Probabilistic or typical | Empirical study with stated sample and method |
| Illustrative or plausible | Single example or analogy, explicitly labeled |
| Definitional | Derivation or established convention with source |

### Formal Development Transforms

**Term undefined before use:** Add a definition at the term's first appearance. Check `NOTATION.md` or `GLOSSARY.md` if the project maintains registries; if not, create inline definitions.

Definition format: *[Term]* (also: *[synonyms if any]*) — [plain-language meaning]. [Formal statement if the domain requires one.]

**Central result stated without derivation:** Add a derivation sketch or a justification sentence. If the full derivation is out of scope, add: "A proof appears in [source]; the key step is [one-line sketch]." Do not assert that a derivation exists if it cannot be located.

**Assumption unstated:** Add an assumption block before the result that depends on it: "Assume [condition]. This holds when [validity domain]."

### Source Integrity Transforms

**`source-needed` flags from diagnosis:** Insert `[citation needed: <type>]` placeholder. Do not fabricate a citation. If the author has a working bibliography, cross-reference it and insert the correct key.

**`source-unverified` flags:** Mark the citation `[UNVERIFIED]` and note what verification would require. Do not remove citations during revision; flag them for author review.

Source transform rule: the revision skill does not search the web or retrieve papers. Source integrity transforms are structural placeholders and flags. Actual verification is the author's responsibility or requires a dedicated source-checking step with live search tools.

### Notation Hygiene Transforms

**Symbol introduced without definition:** Add an introducer sentence: "where [symbol] denotes [meaning in plain language]."

**Inconsistent usage:** Standardize to the first occurrence. Record the decision in `REVISION_LOG.md` so later sessions do not re-randomize.

**Conflict with field convention:** Flag as `[NOTATION CONFLICT: standard usage is X]`. Do not change without author approval — the author may be using intentional non-standard notation.

## Evidence Coverage Matrix

For dense chapters, maintain an internal matrix to verify that every central concept has at least one adequate evidence entry before marking the chapter transform as complete.

| Central concept | Explanatory case | Contrasting or boundary case | Empirical or formal check | Limitation stated |
|---|---|---|---|---|

Not every cell must be filled. Every central concept must have at least one cell that reaches `adequate` on the evidence-match dimension.

## REVISION_LOG.md Entry Format

```
| section_id | gate | action | faithfulness_status | status |
| CH02-S03 | claim-classification | Added [hypothesis] marker to paragraph 4 | preserved | complete |
| CH02-S05 | source-integrity | Inserted [citation needed: empirical study] | preserved | complete |
| CH03-S01 | formal-development | [FAITHFULNESS CONFLICT] Claim overstates evidence; escalated to author | conflict | open |
```

Update the log immediately after each section; do not batch updates.

## Completion Criteria for Pass 2

A section is transform-complete when:
- All `absent` and `partial` gaps from `MANUSCRIPT_ANALYSIS.md` have a log entry.
- No `[FAITHFULNESS CONFLICT]` entries for this section remain `open`.
- The section still conveys the faithfulness anchor recorded during diagnosis.

Update `PROGRESS.md` to the next section after each completion.
