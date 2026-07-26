# Manuscript Revision Skill — Complete Tutorial

This tutorial walks you through every phase of the `manuscript-revision` skill, from installing it to producing a fully revised, humanized manuscript. It assumes you have Claude Code installed and basic familiarity with the command line.

---

## Table of Contents

1. [What the skill does](#1-what-the-skill-does)
2. [Installation](#2-installation)
3. [Quick start — your first revision](#3-quick-start--your-first-revision)
4. [Pass 1: Ingest and Diagnose](#4-pass-1-ingest-and-diagnose)
5. [Pass 2: Scientific Rigor Transform](#5-pass-2-scientific-rigor-transform)
6. [Pass 3: Humanize](#6-pass-3-humanize)
7. [Validation and completion](#7-validation-and-completion)
8. [Working with humanizer tools](#8-working-with-humanizer-tools)
9. [Standalone or combined?](#9-standalone-or-combined)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. What the skill does

The `manuscript-revision` skill transforms a manuscript you have already written — a textbook, paper, technical report, or any long-form document — through a structured three-pass pipeline:

```
Pass 1: Ingest & Diagnose
  ↓  Read existing manuscript → inventory sections → score five rigor gaps

Pass 2: Scientific Rigor Transform
  ↓  Classify claims → match evidence → formalize development → flag missing sources → tidy notation

Pass 3: Humanize
  ↓  Invoke blader/humanizer (EN) or op7418/Humanizer-zh (ZH) → or Claude-native fallback
     → check for rigor regressions → finalize

Validate
  ↓  Run validate_revision.py → confirm all gates pass → mark complete
```

**The faithfulness constraint** is what separates this from a rewrite: every transform must preserve the author's original argument. If a rigor fix would change the argument, the skill flags it as a conflict and escalates to you rather than resolving it silently.

---

## 2. Installation

### Claude Code

Copy the skill folder into your Claude Code skills directory:

```bash
cp -r skills/manuscript-revision ~/.claude/skills/
```

Restart Claude Code. The skill triggers automatically when you describe a revision task.

### Claude.ai

1. Zip the `skills/manuscript-revision/` folder (not the whole repo).
2. Go to **Settings → Capabilities → Skills → Upload skill**.
3. Upload the zip file and toggle the skill on.

### Optional: install humanizer tools

For English humanization:
```bash
pip install humanizer   # or follow https://github.com/blader/humanizer
```

For Chinese humanization:
```bash
git clone https://github.com/op7418/Humanizer-zh
cd Humanizer-zh && pip install -r requirements.txt
```

The skill works without either tool using its built-in Claude-native humanization — the tools just add an extra layer of post-processing.

---

## 3. Quick start — your first revision

Suppose you have a textbook draft in `~/my-book/` with chapters written in Markdown. Here is the complete flow:

**Step 1:** Tell Claude what you want.

```
I have a book draft at ~/my-book/ and I want to make it more scientifically rigorous,
then humanize the result. Use the manuscript-revision skill.
```

**Step 2:** Claude detects the phase (Ingest), reads `references/ingest-and-diagnose.md`, and runs the diagnostic script:

```bash
python3 scripts/diagnose.py ~/my-book/ --output ~/my-book-revision/
```

This creates `MANUSCRIPT_ANALYSIS.md` in your project directory — a section-by-section gap analysis skeleton.

**Step 3:** Review and approve the diagnosis.

Claude will present a summary like:

```
Document: ~/my-book/
Sections: 42 | Words: ~65,000
Language: English

Priority sections (2+ absent dimensions):
  CH03-S02 — absent: evidence, source-integrity
  CH07-S01 — absent: claim-classification, formal-development
  CH11-S04 — absent: evidence, notation

Faithfulness anchors:
  CH01: "This book argues that systems design is best understood through
         formal capacity models rather than empirical heuristics."
  ...

Approve this analysis to begin the revision plan?
```

Review the faithfulness anchors carefully — these are what the skill will not change without your explicit permission.

**Step 4:** Approve, and Claude creates `REVISION_PLAN.md` covering every section.

**Step 5:** Run Pass 2 (rigor transforms) and Pass 3 (humanize) — Claude steps through each section and logs every change.

**Step 6:** Validate.

```bash
python3 scripts/validate_revision.py ~/my-book-revision/
```

---

## 4. Pass 1: Ingest and Diagnose

### Accepted input formats

| Format | How to prepare |
|---|---|
| Markdown (.md) | Nothing — read directly |
| Plain text (.txt) | Nothing — read directly |
| LaTeX (.tex) | Nothing — `\section` boundaries used |
| DOCX | Convert first: `pandoc input.docx -o output.md` |
| PDF | Export to text from your PDF reader, or: `pdftotext input.pdf output.txt` |
| Jupyter Notebook | Read directly — Markdown cells treated as prose, code cells as evidence |

### The five rigor dimensions

The diagnosis scores each section on these dimensions:

| Dimension | What it checks |
|---|---|
| **Claim classification** | Are claims labeled? (established result / empirical / interpretation / hypothesis) |
| **Evidence match** | Does the evidence provided match the strength of the claim? |
| **Formal development** | Are terms defined before use? Are central results derived, not just stated? |
| **Source integrity** | Are citations present where needed? Are they real and scoped correctly? |
| **Notation hygiene** | Are symbols introduced before use? Are they used consistently? |

Each dimension scores as **adequate**, **partial**, or **absent**.

### The faithfulness anchor

For each chapter, Claude extracts the author's central argument using only language present in the text. This becomes the non-negotiable constraint for all transforms. Example:

```
CH04 faithfulness anchor:
  "The proposed scheduling algorithm reduces tail latency by bounding
   queue depth rather than by optimizing average throughput."
```

No transform is allowed to change this claim, even if a reviewer would phrase it differently.

### Approving the diagnosis

When Claude presents the `MANUSCRIPT_ANALYSIS.md`, review:

- Are the faithfulness anchors accurate? If one misrepresents your argument, correct it before approving.
- Are there sections marked `UNREADABLE`? These need format conversion before transforms can proceed.
- Are the section IDs stable? They will be used in the revision log, so changing them later is disruptive.

**Do not proceed to Pass 2 without approving the analysis.** This is a checkpoint, not a formality.

---

## 5. Pass 2: Scientific Rigor Transform

### What gets changed (and what does not)

The rigor pass makes five types of changes, all traceable:

**Claim classification** — Adds labels to distinguish claim types:

```
Before:
  "Cache-oblivious algorithms outperform cache-aware algorithms on modern hardware."

After:
  "Cache-oblivious algorithms outperform cache-aware algorithms on modern hardware
   [sourced empirical claim — cite: Frigo et al. 1999, or citation needed]."
```

**Evidence match** — Adjusts the framing to match evidence strength:

```
Before (overstated claim for the evidence):
  "This proves that the approach is optimal."

After (claim weakened to match a single experiment):
  "This experiment suggests the approach is competitive with baselines on the tested
   workloads [illustrative; generalization requires broader evaluation]."
```

**Formal development** — Adds definitions and derivation sketches:

```
Before:
  "Let T be the throughput of the system."

After:
  "Let T denote the steady-state throughput of the system, measured in
   requests per second under the declared load model."
```

**Source integrity** — Inserts placeholders, never fabricates:

```
Before:
  "Studies show that 70% of distributed system failures are caused by
   configuration errors."

After:
  "Studies show that 70% of distributed system failures are caused by
   configuration errors [citation needed: empirical study of production incidents]."
```

**Notation hygiene** — Standardizes and introduces symbols:

```
Before:
  "μ can be computed from N and λ."

After:
  "The service rate μ (requests/second) can be computed from the server
   count N and the arrival rate λ (requests/second)."
```

### The REVISION_LOG.md

Every change is recorded:

```
| Date       | Section ID | Gate                  | Action                                    | Faithfulness | Status   |
| 2026-07-26 | CH03-S02   | claim-classification  | Added [hypothesis] to paragraph 4         | preserved    | complete |
| 2026-07-26 | CH07-S01   | evidence              | Weakened "proves" to "suggests"           | preserved    | complete |
| 2026-07-26 | CH11-S04   | faithfulness-conflict | Author claims algorithm is "optimal";     | conflict     | open     |
|            |            |                       | no proof or citation present — escalated  |              |          |
```

### Faithfulness conflicts

When a rigor fix would change your argument, the skill stops and flags it instead of deciding for you:

```
[FAITHFULNESS CONFLICT FC-003]
Section: CH11-S04
Original claim: "This algorithm is provably optimal."
Rigor problem: No proof or citation is present. The claim cannot be preserved
               as-is without evidence.
Options:
  A. Provide a proof or citation (author action).
  B. Weaken to "We conjecture this algorithm is optimal" [hypothesis].
  C. Delete the optimality claim.
Awaiting author decision.
```

Conflicts must be resolved before the section can be marked complete. The validator enforces this.

---

## 6. Pass 3: Humanize

### What humanization fixes

AI-generated and heavily edited text often has recognizable patterns:

- Repetitive sentence length (all sentences ~20-25 words)
- Stacked hedges: "it could perhaps be argued that it is possible that..."
- Filler transitions: "Furthermore," "Moreover," "It is worth noting that,"
- Synonym variation for its own sake: alternating "method", "approach", "technique", "strategy" for the same concept
- Over-formal register for the declared audience

The humanize pass removes these patterns without weakening the scientific precision established in Pass 2.

### Tool routing

```
Manuscript language → Tool used
────────────────────────────────
English             → blader/humanizer (if installed) → Claude-native fallback
Chinese             → op7418/Humanizer-zh (if installed) → Claude-native fallback
Mixed               → route each section by language
```

### What humanization does NOT do

- Does not remove claim classification markers
- Does not soften hypothesis or interpretation labels
- Does not delete stated assumptions or validity domains
- Does not remove `[citation needed]` placeholders
- Does not change defined notation

If a humanized passage weakens any of these, the skill restores the precise language and records it in the log.

### Example

```
Before (AI-typical):
  "Furthermore, it is worth noting that the proposed methodology demonstrates
   superior performance characteristics when evaluated against established
   baseline approaches in controlled experimental settings."

After (humanized, rigor preserved):
  "The proposed method outperforms established baselines in controlled experiments
   [illustrative; see Table 3]."
```

---

## 7. Validation and completion

Run the validator at the end of each pass, not only at the end:

```bash
python3 scripts/validate_revision.py <project-dir>
```

Sample output when all gates pass:

```
Manuscript Revision Validator — /Users/you/my-book-revision

  ✓ [PASS]  analysis-approved    MANUSCRIPT_ANALYSIS.md has author approval marker
  ✓ [PASS]  plan-faithfulness    Faithfulness constraint declared
  ✓ [PASS]  plan-humanizer       Humanizer configuration present
  ✓ [PASS]  plan-approved        REVISION_PLAN.md has author approval marker
  ✓ [PASS]  log-has-entries      47 completed log entries found
  ✓ [PASS]  no-open-conflicts    No open faithfulness conflicts
  ✓ [PASS]  progress-populated   PROGRESS.md is populated

  7/7 gates passed.
  Structural validation complete. This confirms harness completeness only.
  Scientific accuracy and author approval are separate requirements.
```

The validator confirms **structural completeness** — that every section has been processed and logged. It does not verify that the scientific content is correct or that the author is satisfied. Those are your responsibility.

---

## 8. Working with humanizer tools

### blader/humanizer (English)

Installation:
```bash
# Follow the repo for the current install method
pip install humanizer
```

The skill invokes it as:
```bash
humanizer --input section.md --output section-humanized.md
```

After processing, Claude diffs the original and humanized output and checks for rigor regressions before accepting.

### op7418/Humanizer-zh (Chinese)

Installation:
```bash
git clone https://github.com/op7418/Humanizer-zh
cd Humanizer-zh && pip install -r requirements.txt
```

Invocation:
```bash
python3 humanizer.py --input section.md --output section-humanized.md
```

### Claude-native fallback

If neither tool is installed, Claude applies humanization directly using the principles in `references/humanize-pass.md`. The result is slightly less aggressive than a dedicated tool but still effective for removing common AI patterns. The log records `tool: claude-native` so you know which method was used.

---

## 9. Standalone or combined?

### As a standalone skill

**Yes — this skill is fully self-contained.** It has no hard dependencies beyond Python 3 (for the scripts) and Claude. You can revise any manuscript without installing either humanizer tool or using any other skill.

A typical standalone workflow:

```
1. Drop your manuscript files into a folder.
2. Invoke: "Revise my manuscript at ~/my-book/ for scientific rigor."
3. Approve the diagnosis and plan.
4. Watch each section transform and humanize.
5. Run the validator.
6. Review the revised output.
```

### Combining with other skills

**`scientific-textbook` (complementary pair)**

These two skills form a complete authoring system:

| Situation | Use |
|---|---|
| Starting a new book from scratch | `scientific-textbook` |
| Improving a draft you already have | `manuscript-revision` |
| Built a book with `scientific-textbook`, now want a final polish pass | `manuscript-revision` (humanize pass only) |
| Have an existing book, want to restructure it as a proper learning system | Both: `manuscript-revision` for rigor, then `scientific-textbook` for curriculum redesign |

**Web search / source-retrieval skills**

The rigor pass inserts `[citation needed: <type>]` placeholders but does not search for sources. Pairing with a web-search skill or a source-retrieval workflow lets you fill those placeholders in the same session.

**Document conversion (Pandoc)**

For DOCX and PDF input, run Pandoc before invoking this skill:

```bash
pandoc manuscript.docx -o manuscript.md --wrap=none
```

This is not a skill dependency — it is a one-line preprocessing step. But pairing with a document-handling skill or MCP server can make the conversion seamless.

### When NOT to combine

Do not run `scientific-textbook` and `manuscript-revision` simultaneously on the same project. Their authority orders and harness structures are different and will conflict. Use one at a time; sequence them intentionally.

---

## 10. Troubleshooting

**The skill does not trigger automatically.**

Add a more explicit trigger phrase: "Use the manuscript-revision skill to revise my book." If the skill is installed correctly, this always loads it.

**`diagnose.py` produces too many sections.**

This happens when the manuscript has many low-level headings. Pass `--min-level 2` if supported, or manually merge rows in `MANUSCRIPT_ANALYSIS.md` before approving the analysis.

**A faithfulness conflict is blocking progress.**

Read the conflict entry in `REVISION_LOG.md`. Choose one of the options listed (provide evidence, weaken the claim, or delete it) and tell Claude your decision. It will apply the chosen resolution and update the conflict status to `resolved`.

**The validator reports `analysis-approved: FAIL` even after I approved.**

The validator looks for `- [x]` or `[x] Author` in `MANUSCRIPT_ANALYSIS.md`. Make sure you or Claude updated the checkbox: change `- [ ] Author has reviewed` to `- [x] Author has reviewed` in the file.

**Humanizer tool not found.**

The skill falls back to Claude-native humanization automatically. If you want to use the tool, install it (see Section 8) and tell Claude: "Re-run the humanize pass using blader/humanizer."

**The revised output changed something I didn't want changed.**

Check `REVISION_LOG.md` for the section. Every change has an entry. If a change was incorrect, tell Claude: "Revert CH03-S02 claim-classification transform" — it will undo that specific entry and log the revert.
