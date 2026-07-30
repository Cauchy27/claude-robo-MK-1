#!/usr/bin/env python3
"""スキルに自己改善の仕組みが備わっているか検証する。

規約: .claude/docs/skill-self-improvement.md

ワークフロー系（execution_type: agent-teams / hybrid）のスキルは
「失敗の記録と反映」節を持たなければならない。失敗を書き戻す場所がないスキルは、
同じ失敗を何度でも繰り返す。

使い方: python3 scripts/validate-skill-self-improvement.py [--root DIR]
終了コード: 違反があれば 1、なければ 0
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# 節を必須とする execution_type
WORKFLOW_TYPES = {"agent-teams", "hybrid"}

SECTION_HEADING = "## 失敗の記録と反映"

# 「既知の失敗パターン」表の必須列
REQUIRED_COLUMNS = ["日付", "失敗の内容", "原因", "反映した対策"]


def execution_type(text: str) -> str:
    m = re.search(r"^execution_type:\s*([a-z-]+)", text, re.M)
    return m.group(1) if m else ""


def has_section(text: str) -> bool:
    return SECTION_HEADING in text


def table_columns(text: str) -> list[str] | None:
    """「失敗の記録と反映」節にある表のヘッダ列を返す。表がなければ None。"""
    idx = text.find(SECTION_HEADING)
    if idx < 0:
        return None
    section = text[idx:]
    # 次の ## 見出しまでを節とみなす
    nxt = section.find("\n## ", len(SECTION_HEADING))
    if nxt > 0:
        section = section[:nxt]
    for line in section.splitlines():
        if line.strip().startswith("|") and "---" not in line:
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if cols:
                return cols
    return None


def check(root: Path) -> list[str]:
    violations: list[str] = []
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.is_dir():
        return [f"スキルディレクトリが存在しない: {skills_dir}"]

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        skill = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        et = execution_type(text)

        if et in WORKFLOW_TYPES and not has_section(text):
            violations.append(
                f"{skill}: execution_type={et} だが「{SECTION_HEADING[3:]}」節がない"
                "（失敗を書き戻す場所がなく、同じ失敗が繰り返される）"
            )
            continue

        if not has_section(text):
            continue

        cols = table_columns(text)
        if cols is None:
            violations.append(f"{skill}: 「{SECTION_HEADING[3:]}」節に失敗パターンの表がない")
            continue
        missing = [c for c in REQUIRED_COLUMNS if c not in cols]
        if missing:
            violations.append(
                f"{skill}: 失敗パターン表に必須列がない（不足: {' / '.join(missing)}）"
            )

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="検証対象のリポジトリルート")
    args = parser.parse_args()

    violations = check(Path(args.root).resolve())

    if violations:
        print(f"スキルの自己改善の不備 {len(violations)} 件:\n")
        for v in violations:
            print(f"  - {v}")
        print("\n規約: .claude/docs/skill-self-improvement.md")
        return 1

    print("スキルの自己改善: 違反なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
