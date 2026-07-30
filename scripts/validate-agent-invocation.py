#!/usr/bin/env python3
"""スキルのエージェント発動導線を検証する。

検証項目:
  1. SKILL.md の subagent_type="X" の X が .claude/agents/** に実在するか
     （Claude Code / Anthropic の組み込みエージェントはホワイトリストで許容）
  2. 内蔵 agents/ を持つスキルの allowed-tools に Task があるか
  3. 内蔵 agents/ の名前が .claude/agents/ と重複していないか（二重定義）
  4. subagent_type を使うスキルの allowed-tools に Task があるか

規約: .claude/docs/agent-invocation-patterns.md
使い方: python3 scripts/validate-agent-invocation.py [--root DIR]
終了コード: 違反があれば 1、なければ 0
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Claude Code / Anthropic 組み込みで .claude/agents/ に定義がなくても解決するもの
BUILTIN_AGENTS = {
    "general-purpose",
    "Explore",
    "Plan",
    "claude",
    "statusline-setup",
    "universal-security-reviewer",
    "universal-performance-analyzer",
    "universal-maintainability-analyzer",
    "claude-code-guide",
}

RESERVED_AGENT_FILENAMES = {"README", "COMPANY-VALUES"}

# 説明文中の一般化表記。実際のエージェント名ではない
PLACEHOLDER_NAMES = {"xxx", "yyy", "zzz", "name", "agent", "agent_type", "subagent"}


def global_agent_names(root: Path) -> set[str]:
    agents_dir = root / ".claude" / "agents"
    if not agents_dir.is_dir():
        return set()
    return {
        p.stem for p in agents_dir.rglob("*.md") if p.stem not in RESERVED_AGENT_FILENAMES
    }


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def allowed_tools(fm: str) -> str:
    m = re.search(r"^allowed-tools:\s*(.+)$", fm, re.M)
    return m.group(1) if m else ""


def check(root: Path) -> list[str]:
    violations: list[str] = []
    known = global_agent_names(root) | BUILTIN_AGENTS
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.is_dir():
        return [f"スキルディレクトリが存在しない: {skills_dir}"]

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        skill = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        fm = frontmatter(text)
        tools = allowed_tools(fm)
        has_task = "Task" in tools

        # 1. subagent_type の解決可能性
        #    {agent_type} のようなテンプレート変数は実名ではないため対象外
        used = {
            name
            for name in re.findall(r'subagent_type\s*=\s*"([^"]+)"', text)
            if "{" not in name
        }
        for name in sorted(used - known):
            violations.append(
                f"{skill}: subagent_type=\"{name}\" は .claude/agents/ に存在せず起動できない"
            )

        # 1-1. subagent_type を伴わない Task(名前) 形式は起動できない
        #      （規約の必須要件2「subagent_type を必ず明示する」に違反）
        #      ただしフロー図の略記は許容する。判定は「実際の起動ブロックが
        #      同一ファイル内にあるか」で行い、無ければ略記しか存在しない＝違反。
        inner_names = {
            f.stem
            for f in (skill_md.parent / "agents").glob("*.md")
            if f.stem not in RESERVED_AGENT_FILENAMES
        }
        # インラインコード（`Task(x)`）は過去の誤りを引用した記述であり違反ではない。
        # 「失敗の記録と反映」節でかつての誤記を引用するため、除外しないと自己言及で誤検出する。
        scannable = re.sub(r"`[^`\n]*`", "", text)
        for name in sorted(set(re.findall(r"Task\(\s*([a-z][a-z0-9_-]*)\s*\)", scannable))):
            if name in PLACEHOLDER_NAMES:
                continue
            if name in used:
                continue
            # 形式B/C は素材名で図示し、実体は別の subagent_type で起動する。
            # 実際の起動ブロックがあるなら図の略記として許容する。
            if used and name in inner_names:
                continue
            violations.append(
                f"{skill}: Task({name}) は subagent_type がなく起動できない"
                f"（形式A/B/C のいずれかで subagent_type を明示すること）"
            )

        # 1-2. prompt 内で参照する内蔵素材（agents/*.md）が実在するか
        for ref in sorted(set(re.findall(r"\.claude/skills/([a-z0-9-]+)/agents/([a-z0-9-]+)\.md", text))):
            ref_skill, ref_agent = ref
            if not (skills_dir / ref_skill / "agents" / f"{ref_agent}.md").is_file():
                violations.append(
                    f"{skill}: 参照先の素材 .claude/skills/{ref_skill}/agents/{ref_agent}.md が存在しない"
                )

        # 1-3. グローバルエージェントへのパス参照が実在するか
        #      表や散文の `.claude/agents/{category}/{name}.md` 形式も対象にする
        #      （subagent_type= の形でなくても、導線として書かれている以上は実在が必要）
        agents_root = root / ".claude" / "agents"
        for ref in sorted(set(re.findall(r"\.claude/agents/([a-z0-9-]+)/([a-z0-9-]+)\.md", text))):
            ref_cat, ref_agent = ref
            if not (agents_root / ref_cat / f"{ref_agent}.md").is_file():
                violations.append(
                    f"{skill}: 参照先のエージェント .claude/agents/{ref_cat}/{ref_agent}.md が存在しない"
                )

        # 4. subagent_type を使うなら allowed-tools に Task が必要
        if used and not has_task:
            violations.append(
                f"{skill}: subagent_type を使用しているが allowed-tools に Task がない"
            )

        # 2 / 3. 内蔵 agents/ の検査
        inner = sorted(
            p.stem
            for p in (skill_md.parent / "agents").glob("*.md")
            if p.stem not in RESERVED_AGENT_FILENAMES
        )
        if inner and not has_task:
            violations.append(
                f"{skill}: 内蔵 agents/ を持つが allowed-tools に Task がない"
            )
        for name in inner:
            if name in global_agent_names(root):
                violations.append(
                    f"{skill}: 内蔵 agents/{name}.md が .claude/agents/ と二重定義になっている"
                )

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="検証対象のリポジトリルート")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    violations = check(root)

    if violations:
        print(f"エージェント発動導線の違反 {len(violations)} 件:\n")
        for v in violations:
            print(f"  - {v}")
        print("\n規約: .claude/docs/agent-invocation-patterns.md")
        return 1

    print("エージェント発動導線: 違反なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
