---
name: manuscript-revision
description: Diagnoses, restructures, and rewrites existing manuscripts to meet scientific rigor standards, then humanizes the result. Use when the user wants to revise an existing book, paper, draft, or chapter; make writing more scientific, rigorous, or evidence-based; restructure formal development in an existing manuscript; or reduce AI-sounding prose. Trigger phrases: "revise my manuscript", "make this more scientific", "improve my book", "rewrite for rigor", "humanize this text", "my book needs work", "scientific revision", "turn my draft into a proper textbook", "make my writing less AI-sounding", "polish this chapter". Supports English and Chinese manuscripts. Optionally integrates blader/humanizer (EN) and op7418/Humanizer-zh (ZH) as post-processing tools.
metadata:
  author: Liang Guo
  version: 1.0.0
  category: writing
---

# Manuscript Revision

Transform an existing manuscript into one that meets scientific rigor standards, then humanize the result so it reads naturally. This skill runs a three-pass pipeline on material the author has already written.

## First Principles

1. The original author's intent is authoritative. Revision improves rigors and readability; it does not replace the author's argument, structure, or voice without explicit permission.
2. Scientific rigor is about verifiability, not style. Claims must be classified, evidence must be matched to claim strength, and assumptions must be stated.
3. Humanization removes AI tells without introducing inaccuracy. Natural prose is not casual prose; the register follows the author's declared audience.
4. Every change must be traceable. The revision log records what changed, why, and which rigor gate it serves.
5. Faithfulness is a first-class gate. A revision that passes all rigor checks but distorts the original argument has failed.

## Detect the Work Phase

Before editing, inspect what exists and select one phase:

- **Ingest:** manuscript exists as raw files (PDF, DOCX, Markdown, TXT, LaTeX). Read `references/ingest-and-diagnose.md`.
- **Diagnose:** manuscript is loaded but MANUSCRIPT_ANALYSIS.md does not exist or is incomplete. Read `references/ingest-and-diagnose.md`.
- **Plan:** gap analysis exists; REVISION_PLAN.md is missing or has unresolved section plans. Read `references/scientific-rigor.md`.
- **Transform:** REVISION_PLAN.md is approved; execute per-section scientific rigor transforms. Read `references/scientific-rigor.md`.
- **Humanize:** rigor transforms are complete; apply humanization pass. Read `references/humanize-pass.md`.
- **Validate:** all transforms and humanization are logged; run completion gates. Read `references/harness-files.md` and run `scripts/validate_revision.py`.

Do not start a transform pass before the gap analysis is approved. Do not start the humanize pass before the transform log is complete.

## Harness Files

A revision project uses these files in the working directory:

- `MANUSCRIPT_ANALYSIS.md` — section inventory, rigor gaps, and diagnosis per section.
- `REVISION_PLAN.md` — per-section transform plan, faithfulness constraint, language mode, humanizer config.
- `REVISION_LOG.md` — append-only log of every change: section ID, gate addressed, action taken, status.
- `PROGRESS.md` — current phase, last completed item, next exact action, blockers.

Read `references/harness-files.md` for templates. Create only the files the phase requires; do not pre-populate empty logs.

## Authority Order

1. User instructions in the current session.
2. Faithfulness constraint in `REVISION_PLAN.md` — the author's declared intent is non-negotiable.
3. `MANUSCRIPT_ANALYSIS.md` — the approved diagnosis.
4. `REVISION_PLAN.md` — the approved plan.
5. `REVISION_LOG.md` — what has already been transformed.
6. `PROGRESS.md` — current state.

## Pass 1: Ingest and Diagnose

Read `references/ingest-and-diagnose.md` before starting this pass.

1. Inventory every section: assign a stable ID (e.g., `CH01-S02`), record title, word count, and format state.
2. For each section, score five rigor dimensions: claim classification, evidence match, formal development, source integrity, and notation hygiene. Use a three-level scale: adequate / partial / absent.
3. Record the faithfulness anchor: what is the author's central argument per chapter? Do not infer beyond what the text states.
4. Run `python3 scripts/diagnose.py <manuscript-dir>` to scaffold `MANUSCRIPT_ANALYSIS.md` when the manuscript is in Markdown or plain text.
5. Present the diagnosis summary and ask for author approval before proceeding.

The diagnosis is not a critique of the author's ideas. It is a structural gap analysis against verifiability criteria.

## Pass 2: Scientific Rigor Transform

Read `references/scientific-rigor.md` before starting this pass.

Execute transforms in section order. For each section:

1. Check `REVISION_LOG.md` for any prior entries on this section.
2. Apply only the transforms declared in `REVISION_PLAN.md` for this section.
3. For each change: record `section_id`, `gate` (claim / evidence / formal / source / notation), `action`, and `status` in `REVISION_LOG.md`.
4. Preserve the author's argument structure. If a rigor fix would require changing the argument, pause and flag it as a `[FAITHFULNESS CONFLICT]` in the log; do not resolve silently.
5. Update `PROGRESS.md` after each section completes.

Do not add content that is not supported by the author's existing evidence or explicitly commissioned. Rigor transforms clarify and formalize; they do not expand claims.

## Pass 3: Humanize

Read `references/humanize-pass.md` before starting this pass.

Detect language and tool availability:

```bash
# Check for English humanizer
command -v humanizer && echo "humanizer-en: available" || echo "humanizer-en: absent"

# Check for Chinese humanizer
python3 -c "import humanizer_zh" 2>/dev/null && echo "humanizer-zh: available" || echo "humanizer-zh: absent"
```

If a tool is available, invoke it per the instructions in `references/humanize-pass.md` and log the tool name, version, and sections processed. If neither tool is available, apply Claude-native humanization per the principles in `references/humanize-pass.md`.

Humanization does not reopen the rigor gates. If a humanized passage weakens a scientific distinction (e.g., softening a hedge or collapsing a claim classification), flag it and restore the precise language.

## Completion Gate

Run the validator before declaring any section or phase complete:

```bash
python3 scripts/validate_revision.py <project-dir>
```

The validator checks:

1. `MANUSCRIPT_ANALYSIS.md` has a completed gap analysis for every section.
2. `REVISION_PLAN.md` declares a faithfulness constraint and a humanizer configuration.
3. `REVISION_LOG.md` has at least one entry per planned section.
4. No `[FAITHFULNESS CONFLICT]` entries remain unresolved.
5. `PROGRESS.md` is current.

Passing the validator confirms structural completeness. It does not confirm scientific accuracy, author approval, or publication readiness.

## References

- `references/ingest-and-diagnose.md` — manuscript ingestion, section inventory, and gap analysis scoring.
- `references/scientific-rigor.md` — rigor dimensions, transform rules, faithfulness constraint, and evidence-to-claim matching.
- `references/humanize-pass.md` — humanizer tool invocation, language routing, fallback principles, and logging.
- `references/harness-files.md` — harness file templates for MANUSCRIPT_ANALYSIS, REVISION_PLAN, REVISION_LOG, and PROGRESS.
