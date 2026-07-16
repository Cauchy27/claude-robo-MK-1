# 🤖 claude-robo-MK-1

📡 Claude Code の日本語出力を **SF AIロボ口調** に変換するプラグイン。HAL 9000 / GLaDOS / TARS 風の冷徹・論理的・機械的トーン。応答の地の文トークンを **約3〜4割削減**（実測ベース。詳細は[節約効果](#-節約効果--effectiveness)参照）、文脈保持を最優先。

```
📡 claude-robo-MK-1 起動します
```

## 目次

| 知りたいこと | 読む場所 |
|------|------|
| どんな見た目になる？ | [Before / After](#before--after)・[特徴](#特徴) |
| 結局どれだけ得する？ | [節約効果サマリ](#節約効果サマリ) → 根拠は[詳細](#-節約効果--effectiveness) |
| 入れたい | [インストール](#インストール) |
| 口調を変えたい・やめたい | [モード切替](#モード切替)・[無効化](#無効化) |
| どうやって削っている？ | [削減メカニズム](#削減メカニズム)・[計測方法](#削減量の計測) |
| 中身の仕組み | [読込構造](#-プラグイン読込構造--load-architecture)・[設計原則](#設計原則) |
| English | [English Documentation](#english-documentation)（巻末に一括） |

## Before / After

| 通常 | SFロボ |
|------|--------|
| ファイルを確認しました。バグが3つほど見つかったようです。修正しますね。 | 📡 スキャン完了。異常3件検出。修復プロトコル起動。 |
| エラーが発生しました。原因を調査します。 | ⚠ エラー検出。原因解析中... |
| どちらのオプションが良いですか？ | オペレーター、選択肢入力待機。A / B？ |

## 特徴

- 日本語特化（敬語・フィラー削除、体言止め徹底）
- SF AIキャラクター（呼称=オペレーター、冷徹・論理的）
- 技術的正確性は完全維持（コード・API名・ビジネスロジック保護）
- SessionStart で自動有効化、シンプル設計
- カタカナ / ひらがな モード切替可能（v0.8.0〜 ひらがな既定）
- 削減量の自動計測ログ＋オンデマンド実測（`/robo-stats`）

## 節約効果サマリ

90日フルログ実測（2026-07-16 集計）に基づく要点。1行で言うと——**「見えている応答は約3割短く、セッション全体の請求換算では2〜3割安くなる」**。

| 指標 | 値 |
|------|-----|
| 応答文（地の文）の削減率 | **約29.4%**（実測 n=5、幅17〜35%）※自動ログの「40%」は固定仮定 |
| セッション全体のトークン削減 | **約2〜3割**（複利効果込み） |
| API換算の削減額 | **約$3,000/90日**（保守）〜 $4,945（上限、Opus 4.8単価） |
| 複利係数 | 応答1件は平均**約750回**、後続リクエストで履歴として再送される |

→ 算出根拠・免責は[節約効果](#-節約効果--effectiveness)セクション参照。**$値は上限寄りの目安**として読むこと。

---

## インストール

### UI 経由（推奨・最速）

Claude Code（デスクトップアプリ / VS Code / CLI 全環境共通）で:

1. アプリ内で `/plugin` 入力 → 4タブ表示
2. **Marketplaces タブ** → 「Add marketplace」→ `Cauchy27/claude-robo-MK-1` 入力
3. **Discover タブ** → `claude-robo-MK-1` 検索
4. **Install** クリック → スコープ選択（User 推奨）

### CLI 経由

```
/plugin marketplace add Cauchy27/claude-robo-MK-1
/plugin install claude-robo-MK-1@claude-robo-MK-1
```

失敗時フォールバック:

```
/plugin install claude-robo-MK-1@Cauchy27/claude-robo-MK-1
```

### 反映・確認

- 新セッション開始時 → 自動有効化（バナー `📡 claude-robo-MK-1 起動します` 表示）
- 本セッションで即反映 → `/reload-plugins`
- インストール確認 → `/plugin` の **Installed タブ** に表示があれば成功

## モード切替

### スラッシュコマンド（推奨）

```
/robo-hiragana    # ひらがなモード切替（既定）
/robo-katakana    # カタカナモード切替
/robo-mode        # 現在モード表示
```

`~/.claude-robo-mode` に書き込まれ、**次セッション起動時に反映**。

### 環境変数（代替）

| 値 | スタイル | バナー |
|----|---------|-------|
| 未設定 or `hiragana` | **ひらがなモード**（既定、柔らかいロボ） | 📡 claude-robo-MK-1 起動します |
| `katakana` | **カタカナモード**（HAL風純度高） | 📡 claude-robo-MK-1 起動シマス |

```bash
export ROBO_STYLE=katakana   # カタカナモード有効化
unset ROBO_STYLE             # ひらがなモード復帰
```

shell profile（`~/.zshrc` / `~/.bashrc`）に追加で永続化。変更後は新セッション起動が必要。

### 優先順位とモード差

```
~/.claude-robo-mode  >  $ROBO_STYLE  >  hiragana（既定）
```

両モード共通: 体言止め、敬語フィラー削除、冷徹トーン、絵文字、技術パラメータ表示。差異は助詞・語尾のみ。

| カタカナモード | ひらがなモード |
|--------------|-------------|
| マズ解析、次ニ修復実施 | まず解析、次に修復実施 |
| ファイル確認済。テスト全通過済。 | ファイル確認済。テスト全通過済。 |

## 無効化

一時解除: 「通常モード」「普通に話して」「ロボ解除」「SFやめて」のいずれかを発言。

完全アンインストール:

```
/plugin uninstall claude-robo-MK-1
```

---

## 削減メカニズム

| Layer | 内容 | 例 |
|-------|------|-----|
| 1. 削除 | 敬語・フィラー・前置き・冗長修飾 | です・ます / ちなみに / 承知しました / 少し・非常に |
| 2. 短縮 | 婉曲表現の圧縮 | 〜かもしれません → 可能性あり ／ 〜のようです → 〜と推定 |
| 3. 体言止め化【最重要】 | 動詞の名詞化 | 〜しました → 〜済 ／ 〜しています → 〜中 |

**保持対象（一切圧縮しない）**: コードブロック / ファイルパス / API名 / エラーメッセージ原文 / 数値 / 固有名詞 / ビジネスロジック

## 削減量の計測

### オンデマンド実測（v0.7.0〜）

```
/robo-stats
```

または自然言語で「実測して」「本当の削減率」等。直近3〜5件のロボ応答を抽出 → 通常日本語版を仮想生成 → 両版の実トークン数を測定（`count_tokens` API / tiktoken / 文字数推定の優先順）→ 実測レポート出力。

### 自動計測（v0.3.0〜、推定値）

Stop hook で各応答の削減量を自動記録。ログは `~/.claude-robo-stats.jsonl` に追記:

```jsonl
{"timestamp":"2026-04-17T12:34:56Z","chars":300,"tokens_est":450,"baseline_est":750,"saved_est":300}
```

- 1応答あたりの節約量が閾値（既定500 tok、`ROBO_THRESHOLD` で変更可）超過時のみ systemMessage 表示
- 累計確認: `cat ~/.claude-robo-stats.jsonl | jq -s 'map(.saved_est) | add'`
- **注意**: `saved_est` は40%削減を仮定した推定値。実測は `/robo-stats` 経由

<details>
<summary>自動計測の既知の限界（数値を読む際の前提・クリックで展開）</summary>

1. **計測範囲**: Stop hook は各ターンの**最後の assistant メッセージのみ**記録。ツール呼び出しを挟む途中のメッセージは対象外。実トランスクリプト検証では、ツール多用セッションの地の文捕捉率は約30〜70%（→ `tokens_est` 合計は実際の地の文総量より**過小**）
2. **換算レート**: 全文字に一律 1.5 tok/字を適用。コード・パス・英語（実際は約0.25〜0.3 tok/字)も1.5換算されるため、コード混在応答では `tokens_est` が5〜30%程度**過大**になりうる
3. **thinking / tool_use 非計測**: 課金対象の出力トークンには thinking と tool_use が含まれるが、本フックは地の文しか見ていない（本プラグインはそれらを圧縮もしない）

</details>

---

## 📊 節約効果 / Effectiveness

> ⚠️ **本セクションの$数値の適用範囲**: 試算はすべて**応答内の地の文（自然言語プロース）のみ**が対象。課金対象の出力トークンには thinking・tool_use が含まれ、エージェンティックな実利用ではそちらが支配的（実測例で thinking だけで可視テキストの1.35倍、tool_use は地の文の約9倍）だが、本プラグインはそれらを一切圧縮しない。よって以下の$値は**実際の請求額・利用枠への効果としては上限寄りの目安**として読むこと。

### 実測削減率: 約29.4%（`/robo-stats`、n=5）

本会話内のロボ応答5件を抽出 → 通常口調版を仮想生成 → 文字数ベース推定で比較した結果、削減率は**平均約29.4%（観測レンジ17.1〜35.1%)**。看板の「30-50%」を下回った。

<details>
<summary>実測の内訳と信頼性の限界（クリックで展開）</summary>

| # | ロボ版 tok | 通常版 tok | 削減率 |
|---|---------:|---------:|-------:|
| 1 | 217 | 302 | 28.1% |
| 2 | 126 | 194 | 35.1% |
| 3 | 307 | 472 | 35.0% |
| 4 | 280 | 409 | 31.5% |
| 5 | 316 | 381 | 17.1% |
| **平均** | - | - | **約29.4%** |

計測方式は文字数ベース推定（method C: 日本語1.5tok/字、英数字0.25tok/字。トークンカウントAPI・tiktoken とも本環境で利用不可のため）。限界:

- **n=5・観測レンジ17.1〜35.1%**（18ポイント幅）。「29.4%」は点推定ではなく、真の削減率はこの幅のどこかにあると読むべき
- **通常版は自己生成反事実**（Claude 自身が SKILL.md の逆変換で仮構築したもので、実在の削減前文ではない）。丁寧語復元で冗長化され過大に出るバイアスと、実際の通常口調はもっと冗長だった可能性（過小バイアス）の両方がありうる
- 本セッション限定のサンプルで、長期傾向とは限らない

</details>

<details>
<summary>⚠️ 訂正: 自動ログの「40.0%」は実測ではない（クリックで展開）</summary>

前バージョンで「実測削減率40.0%」と記載していたが、`hooks/measure.sh` の実装を確認した結果、これは**測定値ではなく固定仮定**だと判明。該当ロジック:

```bash
# ベースライン推定（40%削減想定 → baseline = output / 0.6 ≈ output * 5/3）
BASELINE_EST=$(( TOKEN_EST * 5 / 3 ))
SAVED_EST=$(( BASELINE_EST - TOKEN_EST ))
```

`baseline_est` は実出力に常に `5/3` を掛けた値に過ぎず、`saved_est / baseline_est` は内容に関係なく**構造的に常に約40%**になる（循環計算。厳密には bash 整数演算の切り捨てで応答単位39.4〜40.0%、集計平均39.9953%≈40.0%）。ログ集計で「40.0%」と出たのは、応答内容を反映した結果ではなく、計算式がそう作られているから。訂正・陳謝。

</details>

### モデル別コスト換算（実測29.4%ベース）

モデル別 API 料金（2026年時点、$/1M tokens）と、1,000応答あたりの節約額:

| モデル | Input | Output | 1,000応答あたり節約額 |
|--------|-------|--------|--------------------:|
| Claude Fable 5 | $10.00 | $50.00 | 約 $52.9 |
| Claude Opus 4.8 | $5.00 | $25.00 | 約 $26.4 |
| Claude Sonnet 5 | $3.00（イントロ $2.00〜2026-08-31） | $15.00（イントロ $10.00） | 約 $15.9（イントロ 約 $10.6） |
| Claude Haiku 4.5 | $1.00 | $5.00 | 約 $5.3 |

<details>
<summary>算出根拠と月間換算（実測ペース／ヘビーユーザー、クリックで展開）</summary>

セッション数は長さ・往復数のブレが大きく指標として不適切なため、**出力トークン数の実測集計**を基準に算出。2026-07-01時点のログスナップショット（5,961応答、`tokens_est` 合計 15,138,157 tok）に削減率29.4%を適用:

| 指標 | 値 |
|------|---:|
| 実出力合計（tokens_est） | 15,138,157 tok |
| 推定ベースライン（29.4%仮定） | 約 21,442,149 tok |
| 推定削減量 | 約 6,303,992 tok |
| 1応答あたり平均削減量 | 約 1,058 tok |

**月間換算（実測ペース 78.4応答/日 ≈ 2,353応答/月。自動テスト・ワークフロー込みの参考値)**:

| モデル | 月間節約額 |
|--------|-----------:|
| Fable 5 | 約 $124 |
| Opus 4.8 | 約 $62 |
| Sonnet 5 | 約 $37（イントロ 約 $25） |
| Haiku 4.5 | 約 $12 |

**ヘビーユーザー換算（繁忙日上位25%の平均 約197応答/日 → 約5,902応答/月)**:

| モデル | 月間節約額 |
|--------|-----------:|
| Fable 5 | 約 $312 |
| Opus 4.8 | 約 $156 |
| Sonnet 5 | 約 $94（イントロ 約 $62） |
| Haiku 4.5 | 約 $31 |

応答数（＝実際のトークン生成量）に比例するため、セッション長・往復頻度に左右されない。高単価モデルほど絶対額の節約は大きい。ヘビーペースは自動処理込みの実測値であり、純粋な手動対話だけではこれより低く見積もるべき。

</details>

### 削減対象は「応答内の地の文」のみ

体感と数値が乖離する最大の理由。

- 圧縮するのは**アシスタント応答内の自然言語の地の文だけ**
- コードブロック・ツール呼び出し・ファイル読み込み内容・履歴再送信などの入力トークンは**保持対象**で、一切圧縮しない
- エージェンティックな作業では、1ターンあたりの消費の大半は**入力側**が占める
- → 地の文を3〜4割削っても、それ**単体**ではセッション全体に占める割合は小さい

### 入力側複利: 履歴再送信による増幅効果

一方で、上の$表が**計上していないプラス要因**がある。

- API はステートレスのため、毎ターン過去の全履歴を入力として再送信する
- ターン k の応答を Δ トークン削ると、以後の**全ターンの入力でも毎回 Δ 効き続ける**
- 累積節約は `Δ × N(N−1)/2` —— **セッション長の二乗（O(N²)）で成長**（指数的ではない）
- ただし prompt caching がこの金額効果を**約1/10に減衰**させる（Claude Code はキャッシュ常用のため、再送信履歴の大半はキャッシュ読取単価≈0.1倍で課金）

<details>
<summary>数値例（50ターン・Δ=300tok・Sonnet 5、クリックで展開）</summary>

| 経路 | 累積節約トークン | 金額 |
|---|---:|---:|
| 出力側（$表の計上対象） | 15,000 tok | $0.225 |
| 入力側複利・**キャッシュ無し**（$3/M） | 367,500 tok | $1.10（出力側の約5倍） |
| 入力側複利・**キャッシュ有り**（読取$0.30/M） | 367,500 tok | $0.11 |

- **Claude Code（キャッシュ有効）**: 50ターン級で$表の約1.5〜2倍。30ターン未満では誤差レベル
- **素のAPI利用（キャッシュ未使用の自作アプリ等）**: 複利項が支配的になり、$表の5倍前後まで拡大しうる
- **副次効果**: 履歴が短い＝コンテキスト窓の消費が遅い＝compaction 発動が遅れ、1セッションを長く維持できる（$に現れない実利）

</details>

### 実環境90日ケーススタディ（2026-07-16、フルログ実測）

社内AI活用棚卸し（2026-07-16）で、作者環境の90日分フルログを集計した実測値。上の理論例（50ターン想定）と異なり、**実際のセッション長分布から複利を算出**した点が新規:

- 対象: 7,432応答（`~/.claude-robo-stats.jsonl` 全量）、メインセッション282件
- 直接削減（出力側): 約1,217万 tok（自動ログ40%仮定）。実測29.4%換算なら約760万 tok
- セッション長の実測分布: 中央値80ターン、最長**5,024ターン**。応答1件は平均**約750回**、後続リクエストの履歴として再送される（二乗項により長大セッションが平均を支配）
- 入力側複利（再送回避): 約91.3億 tok（40%仮定・キャッシュ読取単価で換算）
- API換算削減額: **上限約$4,945/90日**（output $304 + cache read $4,565 + cache write $76、Opus 4.8単価）。29.4%換算＋compaction 考慮の保守レンジで**約$3,000/90日（年間約$12,000相当）**
- 同期間の Claude Code 総消費は約174.8億 tok・API換算約$14,800/90日 → **セッション全体のトークンで約2〜3割、コスト換算で約17〜25%の削減効果**

**本ケーススタディの結論**:

1. 実環境の複利は理論例（50ターンで1.5〜2倍）を大きく超え、**入力側が出力側の約15倍と支配項が逆転**する
2. 応答文単体の削減率（約3〜4割）はセッション全体では2〜3割に希釈されるが、複利により**金額インパクトは直接分の約10倍**に増幅される
3. ただし超長セッションでは compaction が古い履歴を圧縮するため「750回再送」は上限値。$値も上限寄りの目安として読むこと

### 週間利用上限（サブスクリプションプラン）の場合

Claude Pro/Max 等の週間上限付きプランでは、評価軸が変わる。

- 「$節約額」ではなく「**週間枠内でどれだけ余裕が増えるか**」で見る
- 入力・thinking・tool_use は非圧縮のため、方向としては**効果は小さい側**
- 大きさは本リポジトリからは定量不可（「地の文が週間消費全体に占める比率」に比例し、内訳はユーザー環境・ワークロード依存のため）
- 実際の利用状況は `/usage` 等で確認して判断すること

### 主目的

金銭節約 < **情報密度向上 + ドッグフーディング + キャラクター性**

---

## 📐 プラグイン読込構造 / Load Architecture

| タイミング | 動作 | 入力トークン |
|----------|------|------------|
| `/plugin install` | `plugin.json` 登録のみ | 0 |
| **SessionStart** | `hooks/activate.sh` → `additionalContext` 注入 | 約300 tok（1回、注入文329字の文字数換算） |
| 対話中 | system context 常駐（cache 利用） | 安価 |
| スキルトリガー時 | `skills/robo/SKILL.md` 読込 | 約4,500 tok（発動時のみ。tiktoken 実測4,463） |
| **各応答終了後** | `hooks/measure.sh` → ログ・閾値超過時 systemMessage | ゼロ（外部プロセス） |

```
[System Prompt]
 ├─ Claude Code デフォルト
 ├─ hooks/activate.sh の additionalContext（毎セッション1回注入）
 │   └─ "SF AIロボ口調、呼称オペレーター、体言止め徹底..."
 └─ skills/robo/SKILL.md（必要時のみ、常駐せず）
```

**CLAUDE.md 直書きとの比較**:

| 方式 | 読込 | 評価 |
|------|------|------|
| CLAUDE.md 直書き | 毎ターン全文が input | 累積消費大 |
| プラグイン方式 | SessionStart 1回注入 → cache 常駐 | **最適**。SKILL.md は遅延読込、無効化は `/plugin disable` 一発、他ユーザーへ配布可能 |

## 設計原則

**文脈保持 > トークン削減**

削減と明確性が衝突した場合、必ず明確性を優先。技術的指示・ビジネスロジック・コード内容は一切圧縮しない。

## 開発者向けメモ

`.claude/skills` を正本、`.agents/skills` を Codex / Antigravity 参照ラッパーとして運用（2026-07-10〜）。

- 全 `SKILL.md` は `execution_type` を `standalone` / `agent-teams` / `subagent` / `hybrid` のいずれかで指定
- スキル内サブエージェントは frontmatter の `model:` で実効モデルを明示
- ラッパー再生成: `bash scripts/generate-agent-wrappers.sh`（同期確認は `--check`）

## ライセンス

MIT

## 関連

- [caveman](https://github.com/JuliusBrussee/caveman) - 英語版（着想元）

---

# English Documentation

📡 A Claude Code plugin that converts Japanese output into a **sci-fi AI robot tone** (HAL 9000 / GLaDOS / TARS style) — cold, logical, mechanical. Cuts response prose tokens by **roughly 30–40%** (measured) while prioritizing context fidelity. Japanese-focused; technical accuracy (code, API names, error messages, business logic) is fully preserved.

```
📡 claude-robo-MK-1 起動します
```

## Before / After

| Normal Japanese | Robo tone |
|------|--------|
| ファイルを確認しました。バグが3つほど見つかったようです。修正しますね。("I checked the file. Found about three bugs. I'll fix them.") | 📡 スキャン完了。異常3件検出。修復プロトコル起動。("Scan complete. 3 anomalies detected. Repair protocol engaged.") |
| どちらのオプションが良いですか？("Which option would you prefer?") | オペレーター、選択肢入力待機。A / B？("Operator, awaiting selection. A / B?") |

## Savings Summary (90-day full-log measurement, 2026-07-16)

In one line: **responses read ~30% shorter, and whole-session cost in API-equivalent terms drops by roughly 20–30%.**

| Metric | Value |
|------|-----|
| Prose reduction per response | **~29.4%** measured (n=5, range 17–35%) — the auto-log's "40%" is a fixed assumption, not a measurement |
| Whole-session token reduction | **~20–30%** (compounding included) |
| API-equivalent savings | **~$3,000 / 90 days** conservative, $4,945 upper bound (Opus 4.8 rates) |
| Compounding factor | each response is resent as history on **~750 subsequent requests** on average |

> ⚠️ All dollar figures cover **only the natural-language prose inside responses**. Billed output also includes thinking and tool_use (which dominate agentic usage) — this plugin compresses none of that. Read every number as **upper-bound-leaning**. Full derivations, caveats, and the correction history are in the Japanese [Effectiveness section](#-節約効果--effectiveness).

## Install

Via UI: `/plugin` → **Marketplaces** tab → Add marketplace → `Cauchy27/claude-robo-MK-1` → **Discover** tab → Install (User scope recommended).

Via CLI:

```
/plugin marketplace add Cauchy27/claude-robo-MK-1
/plugin install claude-robo-MK-1@claude-robo-MK-1
```

Fallback: `/plugin install claude-robo-MK-1@Cauchy27/claude-robo-MK-1`

Auto-enabled on new sessions (banner: `📡 claude-robo-MK-1 起動します`); use `/reload-plugins` for the current session. Verify via the **Installed** tab in `/plugin`.

## Style Modes

```
/robo-hiragana    # hiragana mode (default) — softer robo
/robo-katakana    # katakana mode — strongest HAL-style purity
/robo-mode        # show current mode
```

Written to `~/.claude-robo-mode`; takes effect on the **next** session. Alternative: the `ROBO_STYLE` env var (`katakana` / unset for hiragana). Priority: `~/.claude-robo-mode` > `$ROBO_STYLE` > hiragana. Modes share noun-ending style, emoji palette, and technical-parameter displays — they differ only in particles and verb endings.

## Disabling

Say any of 「通常モード」「普通に話して」「ロボ解除」「SFやめて」to suspend. Full uninstall: `/plugin uninstall claude-robo-MK-1`.

## How It Reduces Tokens

| Layer | What | Example |
|-------|------|-----|
| 1. Delete | politeness markers, fillers, preambles, padding | です・ます / ちなみに / 承知しました |
| 2. Shorten | hedged phrasing → compact forms | 〜かもしれません → 可能性あり |
| 3. Noun-ending (key) | verb phrases → nominal endings | 〜しました → 〜済 ／ 〜しています → 〜中 |

**Never compressed**: code blocks, file paths, API names, verbatim error messages, numbers, proper nouns, business logic.

## Measuring

- **On-demand**: `/robo-stats` — extracts recent robo responses, generates normal-tone counterfactuals, and compares real token counts (count_tokens API / tiktoken / char-based estimate, in that order)
- **Automatic**: a Stop hook logs every response to `~/.claude-robo-stats.jsonl` (`saved_est` assumes a fixed 40% reduction — an estimate, not a measurement). Threshold for the visible systemMessage: 500 tok, tunable via `ROBO_THRESHOLD`

## Effectiveness (key findings)

- Measured prose reduction: **~29.4%** (n=5, self-generated counterfactuals, wide band 17.1–35.1%)
- Real-environment 90-day case study (7,432 responses, 282 sessions): median session 80 turns, longest 5,024. Input-side compounding (avoided history resends, `Δ × N(N−1)/2`, quadratic) dominates at **~15× the output side**; prompt caching dampens the dollar effect ~10×
- API-equivalent savings: conservative **~$3,000/90 days** (~$12,000/yr) against ~$14,800/90d total spend = **17–25% in cost terms**
- On weekly-cap subscription plans (Pro/Max) the effect is likely small and cannot be sized from this repo — check `/usage`
- Load cost of the plugin itself: ~300 tok injected once per session; `SKILL.md` (~4,500 tok) lazy-loads only when triggered
- Primary purpose: cost saving < **information density + dogfooding + character**

## Design Principle

**Context fidelity > token reduction.** When compression and clarity conflict, clarity always wins.

## License

MIT — see [caveman](https://github.com/JuliusBrussee/caveman) (English counterpart & inspiration).
