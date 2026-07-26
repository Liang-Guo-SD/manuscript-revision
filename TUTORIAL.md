# Manuscript Revision Skill — Complete Tutorial

This tutorial walks you through every phase of the `manuscript-revision` skill, from installing it to producing a fully revised, humanized manuscript. It assumes you have Claude Code installed and basic familiarity with the command line.

---

## Table of Contents

1. [What the skill does](#1-what-the-skill-does)
2. [Installation](#2-installation)
3. [Organizing your manuscript](#3-organizing-your-manuscript)
4. [Quick start — your first revision](#4-quick-start--your-first-revision)
5. [How the skill processes multiple chapters](#5-how-the-skill-processes-multiple-chapters)
6. [Pass 1: Ingest and Diagnose](#6-pass-1-ingest-and-diagnose)
7. [Pass 2: Scientific Rigor Transform](#7-pass-2-scientific-rigor-transform)
8. [Pass 3: Humanize](#8-pass-3-humanize)
9. [Validation and completion](#9-validation-and-completion)
10. [Working with humanizer tools](#10-working-with-humanizer-tools)
11. [Standalone or combined?](#11-standalone-or-combined)
12. [Troubleshooting](#12-troubleshooting)

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

## 3. Organizing your manuscript

**Before you start, organize your manuscript as one Markdown file per chapter.** This is the single most important setup step. Getting it right prevents context window problems and makes every subsequent step faster and more reliable.

### The golden rule

```
one chapter  =  one .md file
```

Do not put the entire book in a single file. Do not put multiple chapters in one file. One chapter, one file.

### Why this matters

Claude has a large but finite context window. A single chapter — typically 2,000–8,000 words — fits comfortably in one session and leaves room for the revision work itself. An entire book loaded at once competes with the model's working memory, produces lower-quality transforms, and cannot be checkpointed cleanly between sessions.

The one-file-per-chapter structure also maps directly onto the skill's processing model: diagnosis scans all files, but transforms proceed chapter by chapter. Each chapter is a natural unit for author review before moving to the next.

### Recommended file naming

Name files so that alphabetical sort order equals chapter order. The `diagnose.py` script sorts files alphabetically to assign chapter numbers, so this is not just a style preference — it determines the `CH01`, `CH02` IDs that appear throughout the revision log.

```
my-book/
├── 01-introduction.md
├── 02-background.md
├── 03-core-concepts.md
├── 04-methodology.md
├── 05-case-study-a.md
├── 06-case-study-b.md
├── 07-discussion.md
├── 08-conclusion.md
└── appendix-a.md
```

Zero-padded numbers ensure correct sort order up to 99 chapters. For books over 99 chapters, use three digits: `001-`, `002-`, etc.

### Set up a separate revision project folder

Never write the revision outputs into your manuscript folder. Keep the harness files separate:

```
my-book/                      ← your original manuscript (read-only during revision)
│   01-introduction.md
│   02-background.md
│   ...
│
my-book-revision/             ← revision project folder (all harness files go here)
    MANUSCRIPT_ANALYSIS.md    ← created by diagnose.py
    REVISION_PLAN.md          ← created by Claude after diagnosis
    REVISION_LOG.md           ← append-only log of all changes
    PROGRESS.md               ← session bookmark
```

Claude writes all harness files to the revision folder. The manuscript folder is the source of truth for your original text.

### Converting from other formats

**Single large Markdown file:** Split by chapter headings. A quick way:

```bash
# Split on level-1 headings using csplit (adjust the pattern to match your headings)
csplit --prefix=chapter- --suffix-format='%02d.md' my-book.md '/^# /' '{*}'
# Rename to the 01-, 02- format afterward
```

Or ask Claude: "Split this file into one .md per chapter and save them as 01-title.md, 02-title.md, etc."

**DOCX:** Convert the whole book first, then split:

```bash
pandoc manuscript.docx -o manuscript.md --wrap=none
# Then split as above
```

**PDF:** Export to text from your PDF reader, or:

```bash
pdftotext -layout input.pdf output.txt
# Then split by chapter
```

---

## 4. Quick start — your first revision

With your manuscript organized as one .md file per chapter, here is the complete flow:

**Step 1:** Tell Claude what you want.

```
I have a book draft at ~/my-book/ with one Markdown file per chapter.
I want to make it more scientifically rigorous, then humanize the result.
Use the manuscript-revision skill.
```

**Step 2:** Claude detects the phase (Ingest), reads `references/ingest-and-diagnose.md`, and runs the diagnostic script across all chapters at once:

```bash
python3 scripts/diagnose.py ~/my-book/ --output ~/my-book-revision/
```

This scans every `.md` file in the directory and creates a single `MANUSCRIPT_ANALYSIS.md` covering all chapters.

**Step 3:** Review and approve the diagnosis.

Claude presents a summary across all chapters:

```
Document: ~/my-book/
Chapters: 8 files | Sections: 42 | Words: ~65,000
Language: English

Priority sections (2+ absent dimensions):
  CH03-S02 — absent: evidence, source-integrity
  CH07-S01 — absent: claim-classification, formal-development

Faithfulness anchors:
  CH01: "This book argues that systems design is best understood through
         formal capacity models rather than empirical heuristics."
  CH02: "..."
  ...

Approve this analysis to begin the revision plan?
```

Review the faithfulness anchors carefully — these are what the skill will not change without your explicit permission.

**Step 4:** Approve, and Claude creates `REVISION_PLAN.md` covering every chapter and section.

**Step 5:** Work chapter by chapter through Pass 2 (rigor transforms) and Pass 3 (humanize). See [Section 5](#5-how-the-skill-processes-multiple-chapters) for exactly how sessions are paced.

**Step 6:** Validate after all chapters are complete.

```bash
python3 scripts/validate_revision.py ~/my-book-revision/
```

---

## 5. How the skill processes multiple chapters

This is the most important section to understand before you start. The skill uses a **three-tier model** — not all passes work the same way across chapters.

### The three-tier model

| Pass | Scope | Reason |
|---|---|---|
| **Diagnose** (`diagnose.py`) | All chapters at once | You need the full picture to set faithfulness anchors and plan transforms — a gap in Chapter 7 may be caused by a missing definition introduced in Chapter 3 |
| **Transform + Humanize** (Passes 2 & 3) | One chapter per session | Each chapter is the natural author-review unit; `PROGRESS.md` bookmarks position for the next session |
| **Validate** (`validate_revision.py`) | Whole project | Reports the status of all harness files together |

### Session sizing

Claude's context window is large enough to hold one full chapter and the revision work on it comfortably. Do not try to process more chapters than this in a single session — quality degrades as context fills.

| Manuscript size | Recommended strategy |
|---|---|
| ≤ 5 short chapters (< 15,000 words total) | One session may complete the full transform + humanize pass |
| 6–15 chapters | Plan 2–4 chapters per session; use `PROGRESS.md` as the bookmark |
| 15+ chapters | One chapter per session; treat each session as a clean unit |

When in doubt, do one chapter per session. It is faster to start a new session than to recover from a degraded one.

### How `PROGRESS.md` works as a bookmark

At the end of every chapter, Claude updates `PROGRESS.md` with two entries:

```
## Chapter-Level Summary

| Chapter | File              | Transform   | Humanize    |
|---------|-------------------|-------------|-------------|
| CH01    | 01-introduction.md| complete    | complete    |
| CH02    | 02-background.md  | complete    | complete    |
| CH03    | 03-core-concepts.md| in-progress | planned    |
| CH04    | 04-methodology.md | planned     | planned     |
...

## Next Exact Item

CH03-S03 — rigor transform — formal-development gate
(file: ~/my-book/03-core-concepts.md, section "Derivation of the capacity model")
```

When you start a new session, tell Claude:

```
Resume my manuscript revision at ~/my-book-revision/. Read PROGRESS.md first.
```

Claude reads `PROGRESS.md`, finds the next exact item, reads that chapter file, and continues — with no need to re-explain anything from the previous session.

### What to do when Claude's context fills mid-chapter

If Claude signals that context is getting long, or if responses become noticeably shorter or less precise:

1. Ask Claude to update `PROGRESS.md` with the last completed section and the next exact item.
2. End the session.
3. Start a new session and resume from `PROGRESS.md`.

Do not try to push through a full chapter in a degraded context — the rigor pass requires careful attention to claim boundaries and evidence matching that suffers when context is full.

### A complete multi-session example

A 12-chapter book might look like this across sessions:

```
Session 1: diagnose.py → MANUSCRIPT_ANALYSIS.md (all 12 chapters scanned)
           Claude presents summary, you approve → REVISION_PLAN.md created

Session 2: CH01 transform + humanize → REVISION_LOG.md updated, PROGRESS.md updated
Session 3: CH02 transform + humanize
Session 4: CH03 transform + humanize (faithfulness conflict found → pause)
Session 5: You resolve the conflict → CH03 complete, CH04 transform starts
...
Session 13: CH12 transform + humanize → validate_revision.py → all gates pass
```

Each session starts with: "Resume my manuscript revision at ~/my-book-revision/."

---

## 6. Pass 1: Ingest and Diagnose

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

For each chapter file, Claude extracts the author's central argument using only language present in the text. This becomes the non-negotiable constraint for all transforms on that chapter. Example:

```
CH04 faithfulness anchor:
  "The proposed scheduling algorithm reduces tail latency by bounding
   queue depth rather than by optimizing average throughput."
```

No transform is allowed to change this claim, even if a reviewer would phrase it differently.

### Approving the diagnosis

When Claude presents `MANUSCRIPT_ANALYSIS.md`, review:

- Are the faithfulness anchors accurate for each chapter? If one misrepresents your argument, correct it before approving.
- Are there sections marked `UNREADABLE`? These need format conversion before transforms can proceed.
- Are the section IDs stable? They will be used throughout the revision log, so changing them later is disruptive.

**Do not proceed to Pass 2 without approving the analysis.** This is a checkpoint, not a formality.

---

## 7. Pass 2: Scientific Rigor Transform

### What gets changed (and what does not)

The rigor pass makes five types of changes per chapter, all traceable:

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

Every change across all chapters is recorded in a single append-only log:

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

Conflicts are logged and the chapter is paused until you decide. The validator blocks completion on any open conflict.

---

## 8. Pass 3: Humanize

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

## 9. Validation and completion

Run the validator at the end of each chapter pass and again at the end of the whole project:

```bash
python3 scripts/validate_revision.py ~/my-book-revision/
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

## 10. Working with humanizer tools

### blader/humanizer (English)

Installation:
```bash
# Follow the repo for the current install method
pip install humanizer
```

The skill invokes it per chapter:
```bash
humanizer --input chapter-03.md --output chapter-03-humanized.md
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
python3 humanizer.py --input chapter-03.md --output chapter-03-humanized.md
```

### Claude-native fallback

If neither tool is installed, Claude applies humanization directly using the principles in `references/humanize-pass.md`. The result is slightly less aggressive than a dedicated tool but still effective for removing common AI patterns. The log records `tool: claude-native` so you know which method was used for each chapter.

---

## 11. Standalone or combined?

### As a standalone skill

**Yes — this skill is fully self-contained.** It has no hard dependencies beyond Python 3 (for the scripts) and Claude. You can revise any manuscript without installing either humanizer tool or using any other skill.

A typical standalone workflow:

```
1. Organize your manuscript: one .md file per chapter in ~/my-book/.
2. Invoke: "Revise my manuscript at ~/my-book/ for scientific rigor."
3. Approve the diagnosis (all chapters at once) and the revision plan.
4. Work through chapters one by one across sessions.
5. Run the validator after all chapters complete.
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

For DOCX and PDF input, convert and split before invoking this skill:

```bash
# Convert to Markdown
pandoc manuscript.docx -o manuscript.md --wrap=none
# Then split into one file per chapter (see Section 3)
```

### When NOT to combine

Do not run `scientific-textbook` and `manuscript-revision` simultaneously on the same project. Their authority orders and harness structures are different and will conflict. Use one at a time; sequence them intentionally.

---

## 12. Troubleshooting

**The skill does not trigger automatically.**

Add a more explicit trigger phrase: "Use the manuscript-revision skill to revise my book." If the skill is installed correctly, this always loads it.

**`diagnose.py` assigns wrong chapter numbers.**

Chapter numbers are assigned by alphabetical file sort order. If your files are not zero-padded (e.g., `1-intro.md`, `10-conclusion.md`, `2-background.md`), they will sort incorrectly. Rename to zero-padded format: `01-intro.md`, `02-background.md`, `10-conclusion.md`.

**`diagnose.py` produces too many sections within a chapter.**

This happens when a chapter file has many low-level headings (h3, h4). The script captures all heading levels. Before approving the analysis, manually merge minor-heading rows in `MANUSCRIPT_ANALYSIS.md` so only the meaningful sections remain.

**Context fills up mid-chapter.**

Stop immediately — do not push through. Ask Claude to update `PROGRESS.md` with the exact section it last completed and the next section to process. End the session. Start a new session and say: "Resume my manuscript revision at ~/my-book-revision/. Read PROGRESS.md first." Claude will pick up exactly where the previous session left off.

**A faithfulness conflict is blocking progress.**

Read the conflict entry in `REVISION_LOG.md`. Choose one of the options listed (provide evidence, weaken the claim, or delete it) and tell Claude your decision. It will apply the chosen resolution and update the conflict status to `resolved`.

**The validator reports `analysis-approved: FAIL` even after I approved.**

The validator looks for `- [x]` or `[x] Author` in `MANUSCRIPT_ANALYSIS.md`. Make sure the checkbox is updated: change `- [ ] Author has reviewed` to `- [x] Author has reviewed` in the file.

**Humanizer tool not found.**

The skill falls back to Claude-native humanization automatically. If you want to use the tool, install it (see Section 10) and tell Claude: "Re-run the humanize pass on this chapter using blader/humanizer."

**The revised output changed something I didn't want changed.**

Check `REVISION_LOG.md` for the section. Every change has an entry. If a change was incorrect, tell Claude: "Revert CH03-S02 claim-classification transform" — it will undo that specific entry and log the revert.

**My book has 25+ chapters. How long will this take?**

Budget one Claude session per chapter for the transform + humanize pass. A session typically takes 10–30 minutes of active work depending on chapter length and gap density. A 25-chapter book requires roughly 25–27 sessions (one for diagnosis + plan, one per chapter, one for final validation). Use `PROGRESS.md` as your between-session anchor — the overhead of resuming a session is under one minute.
