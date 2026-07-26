#!/usr/bin/env python3
"""
diagnose.py — scaffold MANUSCRIPT_ANALYSIS.md from a Markdown or plain-text manuscript.

Usage:
    python3 diagnose.py <manuscript-dir-or-file> [--output <output-dir>]

Reads all .md and .txt files under the given path, inventories sections,
and writes a MANUSCRIPT_ANALYSIS.md skeleton to --output (default: cwd).
"""

import argparse
import os
import re
from datetime import date
from pathlib import Path


HEADING_RE = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
DIMENSION_HEADERS = ["Claim class", "Evidence", "Formal dev", "Source integrity", "Notation"]


def read_files(root: Path) -> list[tuple[Path, str]]:
    if root.is_file():
        return [(root, root.read_text(encoding='utf-8', errors='replace'))]
    files = sorted(
        p for p in root.rglob('*')
        if p.suffix in ('.md', '.txt') and p.is_file()
    )
    return [(f, f.read_text(encoding='utf-8', errors='replace')) for f in files]


def extract_sections(path: Path, content: str, chapter_num: int) -> list[dict]:
    headings = HEADING_RE.findall(content)
    if not headings:
        word_count = len(content.split())
        return [{
            'id': f'CH{chapter_num:02d}-S01',
            'title': path.stem,
            'word_count': word_count,
            'format': 'prose',
            'heading_level': 0,
        }]

    sections = []
    # Split content at each heading
    positions = [m.start() for m in HEADING_RE.finditer(content)]
    positions.append(len(content))

    for idx, (level, title) in enumerate(headings):
        start = positions[idx]
        end = positions[idx + 1]
        chunk = content[start:end]
        word_count = len(chunk.split())
        has_code = '```' in chunk or '    ' in chunk
        has_list = bool(re.search(r'^[\-\*\d]', chunk, re.MULTILINE))
        fmt = 'code-heavy' if has_code else ('list' if has_list else 'prose')
        sections.append({
            'id': f'CH{chapter_num:02d}-S{idx + 1:02d}',
            'title': title.strip(),
            'word_count': word_count,
            'format': fmt,
            'heading_level': len(level),
        })
    return sections


def infer_faithfulness_anchor(content: str) -> str:
    # Return the first non-empty paragraph after a top-level heading, truncated.
    first_para = re.search(r'\n\n([^#\n][^\n]{20,})', content)
    if first_para:
        text = first_para.group(1).strip()
        return text[:200] + ('...' if len(text) > 200 else '')
    return '[author central argument — fill in from text]'


def build_analysis(all_sections: list[dict], anchors: list[str], total_words: int) -> str:
    today = date.today().isoformat()

    # Section table
    row_template = '| {id} | {title} | {word_count} | {format} | partial | partial | partial | partial | partial |'
    rows = '\n'.join(row_template.format(**s) for s in all_sections)

    # Faithfulness anchors
    anchor_lines = '\n'.join(
        f'**CH{i+1:02d}:** {anchor}' for i, anchor in enumerate(anchors)
    )

    # Priority list placeholder
    priority_placeholder = '\n'.join(
        f'{i+1}. {s["id"]} — [review all dimensions]'
        for i, s in enumerate(all_sections[:5])
    )

    return f"""# Manuscript Analysis

## Document Summary

- Title: [fill in]
- Language: [EN / ZH / Mixed]
- Source format: [Markdown / converted]
- Total sections: {len(all_sections)}
- Approximate word count: {total_words}
- Analysis date: {today}

## Section Inventory

| ID | Title | Words | Format | Claim class | Evidence | Formal dev | Source integrity | Notation |
|---|---|---|---|---|---|---|---|---|
{rows}

*Scores are pre-filled as `partial` — replace each with `adequate`, `partial`, or `absent` after manual review.*

## Faithfulness Anchors

{anchor_lines}

## Priority List (sections requiring review)

*(Fill in after scoring — list sections with 2+ absent dimensions)*

{priority_placeholder}

## Unresolved Items

- [ ] Sections that could not be read:
- [ ] Sections requiring format conversion:
- [ ] Citations flagged as source-needed:

## Author Approval

- [ ] Author has reviewed and approved this analysis before revision begins.
- Approval date:
- Notes:
"""


def main():
    parser = argparse.ArgumentParser(description='Scaffold MANUSCRIPT_ANALYSIS.md from a manuscript.')
    parser.add_argument('path', help='Manuscript directory or file')
    parser.add_argument('--output', default='.', help='Output directory (default: cwd)')
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f'Error: {root} does not exist.')
        return 1

    pairs = read_files(root)
    if not pairs:
        print(f'No .md or .txt files found under {root}.')
        return 1

    all_sections = []
    anchors = []
    total_words = 0

    for i, (path, content) in enumerate(pairs, start=1):
        sections = extract_sections(path, content, i)
        all_sections.extend(sections)
        total_words += sum(s['word_count'] for s in sections)
        anchors.append(infer_faithfulness_anchor(content))

    analysis = build_analysis(all_sections, anchors, total_words)

    output_path = Path(args.output) / 'MANUSCRIPT_ANALYSIS.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(analysis, encoding='utf-8')
    print(f'Written: {output_path}')
    print(f'Sections found: {len(all_sections)}')
    print(f'Total word count (approximate): {total_words}')
    print('Review each dimension score manually before approving the analysis.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
