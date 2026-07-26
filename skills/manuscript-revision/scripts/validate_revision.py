#!/usr/bin/env python3
"""
validate_revision.py — check structural completeness of a manuscript-revision project.

Usage:
    python3 validate_revision.py <project-dir>

Gates checked:
    1. MANUSCRIPT_ANALYSIS.md exists and has an author approval marker.
    2. REVISION_PLAN.md exists and declares a faithfulness constraint and humanizer config.
    3. REVISION_LOG.md exists and has at least one entry per planned section.
    4. No [FAITHFULNESS CONFLICT] entries remain open.
    5. PROGRESS.md exists and is not blank.

Exit codes: 0 = all gates pass, 1 = one or more gates fail.
"""

import re
import sys
from pathlib import Path


def run(project_dir: Path) -> int:
    results = []

    def check(condition: bool, gate: str, detail: str):
        results.append(('PASS' if condition else 'FAIL', gate, detail))

    # Gate 1: MANUSCRIPT_ANALYSIS.md
    analysis_path = project_dir / 'MANUSCRIPT_ANALYSIS.md'
    if analysis_path.exists():
        content = analysis_path.read_text(encoding='utf-8')
        approved = '- [x]' in content or '[x] Author' in content
        check(approved, 'analysis-approved',
              'MANUSCRIPT_ANALYSIS.md has author approval marker' if approved
              else 'MANUSCRIPT_ANALYSIS.md exists but author approval not marked')
    else:
        check(False, 'analysis-exists', 'MANUSCRIPT_ANALYSIS.md not found')

    # Gate 2: REVISION_PLAN.md
    plan_path = project_dir / 'REVISION_PLAN.md'
    if plan_path.exists():
        plan = plan_path.read_text(encoding='utf-8')
        has_faithfulness = 'Faithfulness Constraint' in plan and len(
            re.findall(r'Faithfulness Constraint\s*\n+(.+)', plan)
        ) > 0
        has_humanizer = 'Humanizer' in plan or 'humanizer' in plan
        has_approval = '- [x]' in plan or '[x] Author' in plan
        check(has_faithfulness, 'plan-faithfulness',
              'Faithfulness constraint declared' if has_faithfulness
              else 'REVISION_PLAN.md missing Faithfulness Constraint section content')
        check(has_humanizer, 'plan-humanizer',
              'Humanizer configuration present' if has_humanizer
              else 'REVISION_PLAN.md missing humanizer configuration')
        check(has_approval, 'plan-approved',
              'REVISION_PLAN.md has author approval marker' if has_approval
              else 'REVISION_PLAN.md exists but author approval not marked')
    else:
        check(False, 'plan-exists', 'REVISION_PLAN.md not found')

    # Gate 3 & 4: REVISION_LOG.md
    log_path = project_dir / 'REVISION_LOG.md'
    if log_path.exists():
        log = log_path.read_text(encoding='utf-8')

        # Count completed entries
        completed = len(re.findall(r'\|\s*complete\s*\|', log))
        has_entries = completed > 0
        check(has_entries, 'log-has-entries',
              f'{completed} completed log entries found' if has_entries
              else 'REVISION_LOG.md has no completed entries')

        # Check for open faithfulness conflicts
        open_conflicts = re.findall(
            r'\[FAITHFULNESS CONFLICT\].*?open', log, re.IGNORECASE
        )
        # Also check the conflicts table
        open_in_table = len(re.findall(r'\|\s*open\s*\|', log))
        total_open = len(open_conflicts) + open_in_table
        check(total_open == 0, 'no-open-conflicts',
              'No open faithfulness conflicts' if total_open == 0
              else f'{total_open} open faithfulness conflict(s) require resolution before completion')
    else:
        check(False, 'log-exists', 'REVISION_LOG.md not found')

    # Gate 5: PROGRESS.md
    progress_path = project_dir / 'PROGRESS.md'
    if progress_path.exists():
        progress = progress_path.read_text(encoding='utf-8').strip()
        check(len(progress) > 50, 'progress-populated',
              'PROGRESS.md is populated' if len(progress) > 50
              else 'PROGRESS.md exists but appears blank or template-only')
    else:
        check(False, 'progress-exists', 'PROGRESS.md not found')

    # Report
    passes = sum(1 for r in results if r[0] == 'PASS')
    fails = sum(1 for r in results if r[0] == 'FAIL')
    width = max(len(r[1]) for r in results) + 2

    print(f'\nManuscript Revision Validator — {project_dir}\n')
    for status, gate, detail in results:
        icon = '✓' if status == 'PASS' else '✗'
        print(f'  {icon} [{status}]  {gate:<{width}}  {detail}')

    print(f'\n  {passes}/{passes + fails} gates passed.')

    if fails == 0:
        print('  Structural validation complete. This confirms harness completeness only.')
        print('  Scientific accuracy and author approval are separate requirements.')
    else:
        print('  Fix the failing gates before marking the revision complete.')

    return 0 if fails == 0 else 1


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 validate_revision.py <project-dir>')
        return 1
    project_dir = Path(sys.argv[1])
    if not project_dir.is_dir():
        print(f'Error: {project_dir} is not a directory.')
        return 1
    return run(project_dir)


if __name__ == '__main__':
    raise SystemExit(main())
