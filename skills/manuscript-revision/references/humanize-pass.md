# Humanize Pass

Use this reference during Pass 3 to apply humanization after the scientific rigor transforms are complete.

## What Humanization Does and Does Not Do

**Does:** Remove AI-generation artifacts — repetitive sentence structures, hedging stacks, filler transitions, unnatural synonym variation, over-formal register for the declared audience.

**Does not:** Change the author's argument, weaken scientific distinctions, collapse claim classifications, remove necessary caveats, or introduce colloquialisms that conflict with the target register.

If a humanized passage weakens a rigor gate outcome (e.g., turns a labeled hypothesis into an asserted fact, or removes a stated assumption), restore the precise scientific language and log the conflict.

## Language Detection

Detect language from the manuscript content or from the `language` field in `REVISION_PLAN.md`. For mixed-language manuscripts, process each language section with the appropriate tool and log them separately.

| Language | Tool | Fallback |
|---|---|---|
| English | blader/humanizer | Claude-native EN humanization |
| Chinese (Simplified/Traditional) | op7418/Humanizer-zh | Claude-native ZH humanization |
| Mixed | Route each section by language | Claude-native for each |

## Tool Availability Check

Run this before the humanize pass:

```bash
# English humanizer (blader/humanizer)
command -v humanizer >/dev/null 2>&1 && echo "humanizer-en: available" || echo "humanizer-en: absent"

# Chinese humanizer (op7418/Humanizer-zh)
python3 -c "import sys; sys.path.insert(0, '/path/to/Humanizer-zh'); import humanizer" 2>/dev/null \
  && echo "humanizer-zh: available" || echo "humanizer-zh: absent"
```

If neither tool is available, proceed with Claude-native humanization (see below) and record `tool: claude-native` in the log.

## Tool Invocation: blader/humanizer (English)

Repository: https://github.com/blader/humanizer

Installation (if not present):
```bash
pip install humanizer  # or follow repo-specific install instructions
```

Invocation pattern:
```bash
humanizer --input <section-file.md> --output <section-humanized.md>
```

If the tool accepts stdin/stdout:
```bash
cat <section-file.md> | humanizer > <section-humanized.md>
```

After invocation:
1. Diff the original and humanized output.
2. Check for rigor gate regressions (see below).
3. Accept the output or restore flagged passages.
4. Log the result.

## Tool Invocation: op7418/Humanizer-zh (Chinese)

Repository: https://github.com/op7418/Humanizer-zh

Installation (if not present):
```bash
git clone https://github.com/op7418/Humanizer-zh
cd Humanizer-zh && pip install -r requirements.txt
```

Invocation pattern (adjust to repo's actual CLI):
```bash
python3 humanizer.py --input <section-file.md> --output <section-humanized.md>
```

Apply the same diff-and-check process as the English tool.

## Claude-Native Humanization

When neither tool is installed or as a supplement after tool processing, apply the following principles directly:

### Sentence rhythm
- Vary sentence length. Break sequences of three or more sentences of similar length.
- Prefer active constructions where the agent is clear. Passive is acceptable when the agent is unknown or irrelevant.
- Avoid starting consecutive sentences with the same word or phrase.

### Hedging and modality
- One hedge per claim is enough. Remove stacked hedges ("it could perhaps be argued that...").
- Preserve hedges that are scientifically necessary (uncertainty, scope limits, hypothesis markers).

### Transitions
- Replace filler transitions ("Furthermore,", "Moreover,", "It is worth noting that") with either a direct statement or a logically necessary connector.
- Use "however", "therefore", "because", "although" only when the logical relation is real.

### Vocabulary
- Choose the simpler word when two words mean the same thing and the simpler one does not sacrifice precision.
- Do not substitute technical terms with non-technical synonyms if the technical term is defined and used consistently.

### Register
- Match the register to the declared audience in `REVISION_PLAN.md` (e.g., graduate-level textbook vs. practitioner guide vs. public-facing explainer).
- Do not add informality for its own sake; aim for natural fluency at the correct register.

## Rigor Gate Regression Check

After any humanization (tool or Claude-native), verify that each of the following is intact for the processed section:

1. All claim classification markers are present and accurate.
2. Hypothesis and interpretation labels have not been softened into assertions.
3. Stated assumptions and validity domains are not deleted.
4. Citations and `[citation needed]` placeholders are unchanged.
5. Notation and defined terms are used consistently.

If a regression is found, restore the precise language from the transform-complete version and log the restoration.

## REVISION_LOG.md Entries for Humanize Pass

```
| section_id | gate | action | tool | status |
| CH01-S01 | humanize | Processed with blader/humanizer v1.2.0; 3 passages restored for rigor | humanizer-en | complete |
| CH02-S03 | humanize | Claude-native humanization applied; no regressions | claude-native | complete |
| CH03-S02 | humanize | Processed with op7418/Humanizer-zh; 1 hedge stack removed | humanizer-zh | complete |
```

## Completion Criteria for Pass 3

The humanize pass is complete when:
- Every section in `REVISION_PLAN.md` has a humanize log entry.
- No rigor regressions remain open.
- The tool field in each log entry is recorded (tool name and version, or `claude-native`).

Run `python3 scripts/validate_revision.py <project-dir>` after completing the pass.
