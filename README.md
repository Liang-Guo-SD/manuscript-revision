# manuscript-revision

A Claude skill that transforms an existing manuscript into one that meets scientific rigor standards, then humanizes the result so it reads naturally.

## What it does

1. **Ingests** the existing manuscript (Markdown, plain text, LaTeX, DOCX-converted, PDF-converted).
2. **Diagnoses** gaps against five rigor dimensions: claim classification, evidence match, formal development, source integrity, and notation hygiene.
3. **Plans** per-section transforms that respect the author's original intent (the faithfulness constraint).
4. **Transforms** the manuscript — classifying claims, matching evidence, formalizing development, flagging missing sources — without changing the author's argument.
5. **Humanizes** the result using [blader/humanizer](https://github.com/blader/humanizer) (English) or [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) (Chinese), with a Claude-native fallback if neither is installed.
6. **Validates** structural completeness and checks that no faithfulness conflicts remain open.

## Installation

### Claude Code

Place the skill folder in your Claude Code skills directory:

```bash
cp -r skills/manuscript-revision ~/.claude/skills/
```

Or add the whole repo as a skills source in your Claude Code settings.

### Claude.ai

1. Zip the `skills/manuscript-revision/` folder.
2. Go to Settings > Capabilities > Skills.
3. Upload the zip.

## Optional dependencies

| Tool | Language | Purpose |
|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | English | Post-processing humanization |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | Chinese | Post-processing humanization |

The skill functions without either tool using Claude-native humanization.

## Scripts

```bash
# Scaffold MANUSCRIPT_ANALYSIS.md from a Markdown manuscript
python3 skills/manuscript-revision/scripts/diagnose.py <manuscript-dir> --output <project-dir>

# Validate structural completeness of a revision project
python3 skills/manuscript-revision/scripts/validate_revision.py <project-dir>
```

## Trigger phrases

- "revise my manuscript"
- "make this more scientific"
- "improve my book"
- "rewrite for rigor"
- "humanize this text"
- "my book needs work"
- "scientific revision"
- "turn my draft into a proper textbook"
- "make my writing less AI-sounding"

## License

MIT
