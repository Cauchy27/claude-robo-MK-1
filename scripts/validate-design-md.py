#!/usr/bin/env python3
"""DESIGN.md が日本語UIタイポグラフィ規範を満たすか検証する。

規範: .claude/skills/design-md/references/jp-typography.md

日本語UIを対象とする DESIGN.md に、和文組版の指定が欠けていないかを機械的に確認する。
欧文専用プロジェクトの DESIGN.md（本文に日本語を含まないもの）は対象外。

使い方:
    python3 scripts/validate-design-md.py [--file DESIGN.md] [--warn-only]

終了コード: 必須項目に欠落があれば 1（--warn-only 指定時は常に 0）
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

JP_CHARS = re.compile(r"[ぁ-んァ-ヶ一-龠]")

# 本文の line-height / letter-spacing の下限（jp-typography.md §2）
MIN_LINE_HEIGHT = 1.5
MIN_LETTER_SPACING_EM = 0.04


# 根拠を明記したうえで規範から意図的に逸脱する宣言。
#   <!-- design-md-allow: letter-spacing 屋外での視認性を優先し字間を抑える -->
ALLOW_DIRECTIVE = re.compile(r"<!--\s*design-md-allow:\s*([a-z-]+)([^>]*)-->")


def has_japanese(text: str) -> bool:
    return bool(JP_CHARS.search(text))


def allowances(text: str) -> dict[str, str]:
    """意図的な逸脱の宣言を {プロパティ名: 理由} で返す。"""
    return {m.group(1): m.group(2).strip() for m in ALLOW_DIRECTIVE.finditer(text)}


# 本文を指す語
BODY_HINT = re.compile(r"本文|body|Body")
# 本文以外の用途を指す語。同一行に併記されることが多い
OTHER_ROLE = re.compile(r"見出し|ヘッダ|heading|Heading|h[1-6]|キャプション|補助|caption|Caption|ラベル|label")
# 「この値を使うな」という否定文脈。ここに現れる値は採用値ではない
NEGATIVE_CONTEXT = re.compile(
    r"狭すぎ|広すぎ|詰まりすぎ|避ける|使わない|不可|NG|非推奨|上書き|デフォルト|default|Default|下回|未満"
)


def _segment_of(line: str, pos: int) -> str:
    """行を Markdown のセル（|）または句点で区切り、pos を含む区間を返す。"""
    delimiters = [i for i, ch in enumerate(line) if ch in "|。"]
    start = max((i + 1 for i in delimiters if i < pos), default=0)
    end = min((i for i in delimiters if i > pos), default=len(line))
    return line[start:end]


def _is_negated(segment: str) -> bool:
    return bool(NEGATIVE_CONTEXT.search(segment))


def _values_in_lines(text: str, prop: str, pattern: str) -> tuple[list[float], list[float]]:
    """(全ての値, 本文に適用される値) を返す。

    対応する書式:
      - CSS 宣言:            `line-height: 1.7;`
      - 値が先のテーブル:      `| \\`letter-spacing\\` | **0.02em** | 日本語本文 |`
      - 役割が先のテーブル:    `| line-height | 本文 1.7（見出し 1.3） | 備考 |`

    同一行に本文値と見出し値が併記される書式が一般的なため、
    他の役割語がある行では「本文」の直後から次の役割語までの値だけを本文値とする。
    「デフォルトは狭すぎるので上書き必須」のような否定文脈の値は採用値として扱わない。
    """
    all_values: list[float] = []
    body_values: list[float] = []

    for line in text.splitlines():
        if prop not in line:
            continue
        found = [float(m) for m in re.findall(pattern, line)]
        if not found:
            continue
        all_values.extend(found)

        body = BODY_HINT.search(line)
        if not body:
            continue
        # 「本文」自体が否定文脈にある行（本文には使うな、等）は本文値を取らない
        if _is_negated(_segment_of(line, body.start())):
            continue

        # 値ごとに、その値が属するセグメントで採否を決める。
        # 「| 本文 0.06em | デフォルト 0.00938em は狭すぎる |」の 0.00938em は
        # 否定セグメントにあるため本文値に含めない。
        adopted = [
            (mm.start(), float(mm.group(1)))
            for mm in re.finditer(pattern, line)
            if not _is_negated(_segment_of(line, mm.start()))
        ]
        if not adopted:
            continue

        other = OTHER_ROLE.search(line)
        if not other:
            # 役割の併記がない行は、採用値がすべて本文に適用されるとみなす
            # （「| letter-spacing | 0.02em | 日本語本文 |」のように値とラベルが別セルの書式）
            body_values.extend(v for _, v in adopted)
            continue

        # 役割が併記される行は「本文」の直後から次の役割語までを本文のスコープとする
        lo = body.start()
        hi = len(line) if lo > other.start() else other.start()
        scoped = [v for pos, v in adopted if lo <= pos < hi]
        # スコープ内に値がなければ、同一行の採用値をラベル対応とみなす
        body_values.extend(scoped if scoped else [v for _, v in adopted])

    return all_values, body_values


def line_height_values(text: str) -> tuple[list[float], list[float]]:
    return _values_in_lines(text, "line-height", r"([0-9]+\.[0-9]+|[0-9]+)(?!\S*[a-zA-Z%])")


def letter_spacing_values(text: str) -> tuple[list[float], list[float]]:
    return _values_in_lines(text, "letter-spacing", r"([0-9]*\.?[0-9]+)\s*em")


def _declared(text: str, prop: str) -> bool:
    """プロパティが「採用する指定」として書かれているか。

    「font-family は指定しない（NG例）」のような否定文脈での言及は指定とみなさない。
    """
    for line in text.splitlines():
        pos = line.find(prop)
        if pos < 0:
            continue
        if not _is_negated(_segment_of(line, pos)):
            return True
    return False


def check(text: str) -> tuple[list[str], list[str]]:
    """(必須項目の欠落, 警告) を返す。"""
    errors: list[str] = []
    warnings: list[str] = []

    if not _declared(text, "font-family"):
        errors.append("フォントファミリー（font-family）の指定がない")

    allowed = allowances(text)

    def check_threshold(
        label: str, values: list[float], body: list[float], minimum: float, unit: str
    ) -> None:
        if label in allowed:
            reason = allowed[label] or "理由の記載なし"
            warnings.append(f"{label} は規範から意図的に逸脱している（{reason}）")
            return
        if not values:
            errors.append(f"{label} の指定がない（和文は {minimum}{unit} 以上が必要）")
            return
        # 本文と明記された値が下限を下回るのは、見出しの値が満たしていても不可
        if body and min(body) < minimum:
            errors.append(
                f"{label} の本文の値が {min(body)}{unit} で、和文の下限 {minimum}{unit} を下回る"
            )
            return
        if max(values) < minimum:
            errors.append(
                f"{label} の最大値が {max(values)}{unit} で、和文の下限 {minimum}{unit} を下回る"
            )
            return
        # どれが本文か判別できないまま下限割れの値が混じっている場合は注意喚起にとどめる
        if not body and min(values) < minimum:
            warnings.append(
                f"{label} に下限 {minimum}{unit} を下回る値 {min(values)}{unit} が含まれる"
                "（本文に適用されていないか確認すること）"
            )

    lh_all, lh_body = line_height_values(text)
    check_threshold("line-height", lh_all, lh_body, MIN_LINE_HEIGHT, "")

    ls_all, ls_body = letter_spacing_values(text)
    check_threshold("letter-spacing", ls_all, ls_body, MIN_LETTER_SPACING_EM, "em")

    if not _declared(text, "line-break"):
        if _declared(text, "word-break"):
            errors.append(
                "禁則処理が line-break で指定されていない"
                "（word-break は折り返し制御であって禁則処理ではない）"
            )
        else:
            errors.append("禁則処理（line-break: strict）の指定がない")

    if not _declared(text, "font-feature-settings"):
        errors.append("OpenType 機能（font-feature-settings の palt / kern）の指定がない")

    if not _declared(text, "overflow-wrap"):
        warnings.append("overflow-wrap の指定がない（長いURL・英単語のはみ出し防止）")

    if not re.search(r"混植|和欧", text):
        warnings.append("和欧混植の方針が書かれていない")

    if not re.search(r"44\s*(px|×|x)", text):
        warnings.append("タッチターゲットの下限（44px）が書かれていない")

    if not re.search(r"コントラスト|WCAG", text):
        warnings.append("コントラスト比の基準（WCAG AA）が書かれていない")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", default="DESIGN.md", help="検証する DESIGN.md のパス")
    ap.add_argument(
        "--warn-only", action="store_true", help="欠落があっても終了コード 0 を返す"
    )
    args = ap.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"DESIGN.md が見つからない: {path}")
        return 0 if args.warn_only else 1

    text = path.read_text(encoding="utf-8", errors="ignore")

    if not has_japanese(text):
        print(f"{path}: 日本語を含まないため和文組版の検証は対象外")
        return 0

    errors, warnings = check(text)

    if not errors and not warnings:
        print(f"{path}: 日本語UIタイポグラフィ規範を満たしている")
        return 0

    print(f"{path}: 日本語UIタイポグラフィ規範の検証結果\n")
    if errors:
        print(f"欠落 {len(errors)} 件（必須）:")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"\n推奨 {len(warnings)} 件:")
        for w in warnings:
            print(f"  - {w}")
    print("\n規範: .claude/skills/design-md/references/jp-typography.md")

    return 0 if args.warn_only or not errors else 1


if __name__ == "__main__":
    sys.exit(main())
