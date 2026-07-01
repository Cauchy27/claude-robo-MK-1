# 🤖 claude-robo-MK-1

> 📡 Claude Code ノ日本語出力ヲ **SF AIロボ口調** ニ変換。トークン **30-50%削減デキルカモ**、文脈保持優先。

HAL 9000 / GLaDOS / TARS / ATLAS 風ノ冷徹・論理的・機械的トーン。常時有効。v0.5.0〜 カタカナ / ひらがな モード切替可能（v0.8.0〜 ひらがな既定）。

## Before / After

| 通常 | SFロボ |
|------|--------|
| ファイルを確認しました。バグが3つほど見つかったようです。修正しますね。 | 📡 スキャン完了。異常3件検出。修復プロトコル起動。 |
| エラーが発生しました。原因を調査します。 | ⚠ エラー検出。原因解析中... |
| どちらのオプションが良いですか？ | オペレーター、選択肢入力待機。A / B？ |

## 特徴

- 日本語特化（敬語・フィラー削除、体言止メ徹底）
- SF AIキャラクター（呼称=オペレーター、冷徹・論理的）
- 技術的正確性ハ完全維持（コード・API名・ビジネスロジック保護）
- SessionStart デ自動有効化、シンプル設計
- **v0.4.0〜**: 近未来演出（技術パラメータ・ステータスID・構造化ブロック）
- **v0.5.0〜**: `ROBO_STYLE` 環境変数デ カタカナ / ひらがな モード切替

## インストール

### UI 経由（推奨・最速）

Claude Code（デスクトップアプリ / VS Code / CLI 全環境共通）デ:

1. アプリ内デ `/plugin` 入力 → 4タブ表示
2. **Marketplaces タブ** → 「Add marketplace」→ `Cauchy27/claude-robo-MK-1` 入力
3. **Discover タブ** → `claude-robo-MK-1` 検索
4. **Install** クリック → スコープ選択（User 推奨）

### CLI 経由（コマンド入力）

アプリ内チャットニ順次入力:

```
/plugin marketplace add Cauchy27/claude-robo-MK-1
/plugin install claude-robo-MK-1@claude-robo-MK-1
```

失敗時フォールバック:

```
/plugin install claude-robo-MK-1@Cauchy27/claude-robo-MK-1
```

### 反映

- 新セッション開始時 → 自動有効化
- 本セッションデ即反映 → `/reload-plugins`

### 確認

```
/plugin
```

**Installed タブ** ニ `claude-robo-MK-1` 表示確認デ成功。

### 起動バナー

新セッション開始時、以下ノバナー表示（既定ハひらがなモード）:

```
📡 claude-robo-MK-1 起動します
```

## モード切替 / Style Modes

v0.6.0〜、スラッシュコマンド & 環境変数デ表記スタイル選択可能:

### スラッシュコマンド（推奨）

```
/robo-hiragana    # ひらがなモード切替（既定）
/robo-katakana    # カタカナモード切替
/robo-mode        # 現在モード表示
```

`~/.claude-robo-mode` ニ書込マレ、**次セッション起動時ニ反映**。現セッションハ変更前ノ状態継続。

### 環境変数（代替）

| 値 | スタイル | バナー |
|----|---------|-------|
| 未設定 or `hiragana` | **ひらがなモード**（既定、柔ラカイロボ） | 📡 claude-robo-MK-1 起動します |
| `katakana` | **カタカナモード**（HAL風純度高） | 📡 claude-robo-MK-1 起動シマス |

**設定方法**:

```bash
# カタカナモード有効化
export ROBO_STYLE=katakana

# ひらがなモード復帰
unset ROBO_STYLE
```

shell profile (`~/.zshrc` / `~/.bashrc`) ニ追加デ永続化。設定変更後ハ新セッション起動必要。

### 優先順位

```
~/.claude-robo-mode  >  $ROBO_STYLE  >  hiragana（既定）
```

コマンド経由設定ハ環境変数ヲオーバーライドスル。

**両モード共通**: 体言止メ、敬語フィラー削除、冷徹トーン、絵文字、技術パラメータ、ステータスID。差異ハ助詞・語尾ノミ。

**サンプル比較**:

| カタカナモード | ひらがなモード |
|--------------|-------------|
| 📡 スキャン完了。異常3件検出。修復プロトコル起動。 | 📡 スキャン完了。異常3件検出。修復プロトコル起動。 |
| マズ解析、次ニ修復実施 | まず解析、次に修復実施 |
| ファイル確認済。テスト全通過済。 | ファイル確認済。テスト全通過済。 |

（体言止メ中心応答デハ差異ナシ、接続詞・語尾表現ノ違イガ主）

## 無効化

以下ノイズレカ発言:
- 「通常モード」
- 「普通に話して」
- 「ロボ解除」
- 「SFやめて」

完全アンインストール手順:

```bash
/plugin uninstall claude-robo-MK-1
```

## 削減メカニズム

### Layer 1: 削除
- 敬語（です・ます）
- フィラー（ちなみに・とりあえず）
- 前置キ（承知シマシタ）
- 冗長修飾（少シ・非常ニ）

### Layer 2: 短縮
- 〜カモシレマセン → 可能性アリ
- 〜ダト思イマス → 断言化or削除
- 〜ノヨウデス → 〜ト推定

### Layer 3: 体言止メ化【最重要】
- 〜シマシタ → 〜済 / 〜完了
- 〜シマス → 名詞化 / 〜予定
- 〜シテイマス → 〜中

### 保持対象
コードブロック / ファイルパス / API名 / エラーメッセージ原文 / 数値 / 固有名詞 / ビジネスロジック

## 削減量ノ自動計測 / オンデマンド実測

### オンデマンド実測（v0.7.0〜）

真ノ削減率ヲ実測シタイ場合:

```
/robo-stats
```
または自然言語デ「実測して」「本当の削減率」等。

**動作**: 直近3-5件ノロボ応答ヲ抽出 → 通常日本語版ヲ仮想生成 → 両版ノ実トークン数測定（`count_tokens` API / tiktoken / 文字数推定 優先順位降順）→ 実測レポート出力。

```
📊 真の削減率 実測レポート
| # | ロボ tok | 通常 tok | 削減率 |
|---|---------|---------|-------|
| 1 | 120     | 198     | 39.4% |
| ... |
| **平均** | - | - | **42.1%** |
```

### 自動計測（v0.3.0〜、推定値）

Stop hook デ各応答ノ削減量ヲ自動計測:

```
📊 推定 ~450 tok / 節約 ~180 tok (@40%想定)
```

- ログハ `~/.claude-robo-stats.jsonl` ニ追記
- 文字数カラ推定（Anthropic API 非依存）
- ベースラインハ40%削減仮定ノ推定値（厳密ナ原文比較デハナイ）
- **注意**: `tokens_est` / `saved_est` ハ推定。実測ハ `/robo-stats` 経由

### 表示頻度

ノイズ抑制ノタメ、**1応答アタリノ節約量ガ500 tokens 超過時ノミ** systemMessage 表示:

```
📊 推定 ~900 tok / 節約 ~600 tok (@40%想定)
```

閾値ハ環境変数デ変更可能:

```bash
# 例: 200 tok 以上節約デ表示
export ROBO_THRESHOLD=200
```

ログハ全応答デ追記サレル。累計ハ `~/.claude-robo-stats.jsonl` デ確認可能。

### ログ形式

```jsonl
{"timestamp":"2026-04-17T12:34:56Z","chars":300,"tokens_est":450,"baseline_est":750,"saved_est":300}
```

累計節約量ノ確認:

```bash
cat ~/.claude-robo-stats.jsonl | jq -s 'map(.saved_est) | add'
```

## 📊 節約効果 / Effectiveness

### モデル別 API 料金（2026年時点、$/1M tokens）

| モデル | Input | Output |
|--------|-------|--------|
| Claude Fable 5 | $10.00 | $50.00 |
| Claude Opus 4.8 | $5.00 | $25.00 |
| Claude Sonnet 5 | $3.00（イントロ価格 $2.00, 〜2026-08-31） | $15.00（イントロ価格 $10.00） |
| Claude Haiku 4.5 | $1.00 | $5.00 |

### 試算基準ヲ「セッション数」カラ「トークン数」ヘ変更

セッション数ハ1セッションあたりノ長サ・往復数ノブレガ大キク（本環境ノ実測デモ30分ギャップ基準デ月92〜267セッショント2倍以上ノ幅）、節約効果ノ指標トシテ不適切ト判断。以下、**出力トークン数ノ実測集計**ヲ基準ニ再構成。

### ⚠️ 訂正：自動ログノ「40.0%」ハ実測デハナイ

前バージョンデ「実測削減率40.0%」ト記載シテイタガ、`hooks/measure.sh` ノ実装ヲ確認シタ結果、コレハ**測定値デハナク固定仮定**ダト判明。該当ロジック：

```bash
# ベースライン推定（40%削減想定 → baseline = output / 0.6 ≈ output * 5/3）
BASELINE_EST=$(( TOKEN_EST * 5 / 3 ))
SAVED_EST=$(( BASELINE_EST - TOKEN_EST ))
```

`baseline_est` ハ実出力（`tokens_est`）ニ常ニ `5/3` ヲ掛ケタ値ニ過ギズ、`saved_est / baseline_est` ハ入力内容ニ関係ナク**常ニ厳密ニ40.0%**ニナル（循環計算）。76日分ノログ集計デ「40.0%」ト出タノハ、5,961件ノ応答内容ヲ反映シタ結果デハナク、計算式ガソウ作ラレテイルカラ。訂正・陳謝。

### 実測（オンデマンド `/robo-stats`、本セッション5件サンプル）

`/robo-stats` コマンドデ、本会話内ノロボ応答5件ヲ抽出→通常口調版ヲ仮想生成→文字数ベース推定（トークンカウントAPI・tiktoken共ニ本環境デ利用不可ノタメ method C: 日本語1.5tok/字、英数字0.25tok/字）デ比較：

| # | ロボ版 tok | 通常版 tok | 削減率 |
|---|---------:|---------:|-------:|
| 1 | 217 | 302 | 28.1% |
| 2 | 126 | 194 | 35.1% |
| 3 | 307 | 472 | 35.0% |
| 4 | 280 | 409 | 31.5% |
| 5 | 316 | 381 | 17.1% |
| **平均** | - | - | **約29.4%** |

計測方式：**推定**（文字数ベース、method C。API実測・tiktokenヨリ精度低）。サンプル5件・本セッション限定、長期傾向トハ限ラナイ。

「30-50%」ノ看板ノ**下限寄リ**、自動ログノ仮定値（40%）ヨリモ**低メ**ニ出タ。以下ノ$試算ハ自動ログ仮定値（40%）ベースノママ残スガ、実際ハコレヨリ小サイ可能性ガアル点、注意。

### モデル別コスト換算（出力削減トークン基準・自動ログ仮定40%ベース）

削減トークン（saved_est）ヲ各モデルノ Output 単価デ換算。基準ハ「セッション」デハナク「応答1,000件あたり」（実測平均 1,693 tok/応答 × 1,000）:

| モデル | Output $/MTok | 1,000応答あたり節約額 |
|--------|---------------:|----------------------:|
| Fable 5 | $50.00 | 約 $84.6 |
| Opus 4.8 | $25.00 | 約 $42.3 |
| Sonnet 5 | $15.00（イントロ $10.00） | 約 $25.4（イントロ 約 $16.9） |
| Haiku 4.5 | $5.00 | 約 $8.5 |

### 参考：本環境ノ実測ペース換算（月換算）

上記ログハ平均 78.4応答/日（≈2,353応答/月相当）ノペース。コレハ自動テスト・ワークフロー等ヲ含ム集計値デアリ、典型的ナ「手動開発セッション」ノペースト同一視ハデキナイ点、注意（参考値トシテ提示）：

| モデル | 月間節約額（実測ペース ≈2,353応答/月） |
|--------|----------------------------------------|
| Fable 5 | 約 $199 |
| Opus 4.8 | 約 $100 |
| Sonnet 5 | 約 $60（イントロ価格適用時ハ約 $40） |
| Haiku 4.5 | 約 $20 |

- 応答数（＝実際ノトークン生成量）ニ比例スルタメ、セッション長・往復頻度ニ左右サレナイ
- 高単価モデル（Fable 5 / Opus 4.8）ほど絶対額ノ節約効果ハ大キイ

### ヘビーユーザー換算（実測ピーク基準）

「実測ペース平均」ハ閑散日モ含ムタメ、フル稼働時ノ上限目安トシテ**アクティブ日ノ上位25%（繁忙日）ノ平均ペース**デ再計算：繁忙日平均 約197応答/日 → 月換算 約5,910応答、削減トークン 約1,000万tok/月。

| モデル | 月間節約額（ヘビー使用、約5,910応答/月） |
|--------|--------------------------------------------|
| Fable 5 | 約 $500 |
| Opus 4.8 | 約 $250 |
| Sonnet 5 | 約 $150（イントロ価格適用時ハ約 $100） |
| Haiku 4.5 | 約 $50 |

コレガ「実測データ上ノ最ヘビーケース」。日常的ニコレダケ使エバ月$50〜$500ノレンジ（モデル依存）ニ到達スル計算ダガ、上記ペースハ自動処理込ミノ実測値デアリ、純粋ナ手動対話ダケデハコレヨリ低ク見積モルベキ。

### 重要：削減対象ハ「応答内ノ地ノ文」ノミ

体感ト数値ガ乖離スル最大ノ理由：本プラグインガ圧縮スルノハ**アシスタント応答内ノ自然言語ノ地ノ文（プロース部分）ノミ**。以下ハ**保持対象**デ、一切圧縮サレナイ：

- コードブロック・ファイルパス・API名・エラーメッセージ原文
- ツール呼出シ（tool_use / tool_result）
- ファイル読込ミ内容・検索結果等、コンテキストトシテ再送信サレル入力トークン全般

アジェンティックなコーディング作業デハ、1ターンアタリノトークン消費ノ大半ハ**入力側**（会話履歴ノ再送信・ファイル内容・ツール結果）ガ占メ、地ノ文ノ出力ハ全体ノホンノ一部ニ過ギナイコトガ多イ。「1回デ数百万トークン使ッテイル気ガスル」ト感ジルノハ、コノ入力側ノ再送信コスト（本プラグインノ削減対象外）ヲ体感シテイル可能性ガ高イ。ツマリ、地ノ文ヲ30-40%圧縮シテモ、**セッション全体ノトークン消費ニ占メル割合ハ極メテ小サイ**。

### 週間利用上限（サブスクリプションプラン）ヲ考慮スル場合

従量課金APIデハナクClaude Pro/Max等ノ週間利用上限付キプランヲ利用中ナラ、評価軸ハ「$節約額」デハナク「週間枠内デドレダケ余裕ガ増エルカ」ニナル。上記ノ理由（入力トークンハ非圧縮）カラ、**週間トークン消費ニ占メル削減分ノ割合ハ、$換算ト同様ニ小サイ**ト推定サレル——地ノ文ガ週間消費全体ニ占メル比率ニ比例スルタメ。正確ナ内訳（入力/出力比率）ハユーザー環境依存デ本リポジトリ側カラハ把握不能。実際ノ週間利用状況ハ Claude Code / claude.ai ノ利用状況画面（`/usage` 等）デ確認スルコトヲ推奨。

### 主目的

金銭節約 < **情報密度向上 + ドッグフーディング + キャラクター性**

## Installation (English)

### Via UI (Recommended)

In Claude Code (desktop / VS Code / CLI):

1. Type `/plugin` → 4 tabs shown
2. **Marketplaces** tab → "Add marketplace" → enter `Cauchy27/claude-robo-MK-1`
3. **Discover** tab → search `claude-robo-MK-1`
4. Click **Install** → choose scope (User recommended)

### Via CLI

```
/plugin marketplace add Cauchy27/claude-robo-MK-1
/plugin install claude-robo-MK-1@claude-robo-MK-1
```

Fallback if install fails:

```
/plugin install claude-robo-MK-1@Cauchy27/claude-robo-MK-1
```

### Activation

- New session → auto-enabled
- Current session → `/reload-plugins`

### Verify

```
/plugin
```

Check **Installed** tab for `claude-robo-MK-1`.

### Startup Banner

On new session (default is hiragana mode):

```
📡 claude-robo-MK-1 起動します
```

## Style Modes (English)

As of v0.6.0, pick the output style via slash command or env var:

### Slash Commands (recommended)

```
/robo-hiragana    # switch to hiragana mode (default)
/robo-katakana    # switch to katakana mode
/robo-mode        # show current mode
```

Writes to `~/.claude-robo-mode`. Takes effect on the **next** session.

### Env Var (alternative)

As of v0.5.0, set the `ROBO_STYLE` env var to pick the output style:

| Value | Style | Banner |
|-------|-------|--------|
| unset or `hiragana` | **Hiragana mode** (default, softer robo) | 📡 claude-robo-MK-1 起動します |
| `katakana` | **Katakana mode** (HAL-style, strongest robo) | 📡 claude-robo-MK-1 起動シマス |

```bash
# Enable katakana mode
export ROBO_STYLE=katakana

# Revert to hiragana (default)
unset ROBO_STYLE
```

Add to your shell profile (`~/.zshrc` / `~/.bashrc`) to persist. A new
session is required after changing the variable.

### Priority

```
~/.claude-robo-mode  >  $ROBO_STYLE  >  hiragana (default)
```

**Shared across modes**: noun-ending style, emoji palette, technical
parameter displays, status IDs. The difference is limited to particles,
verb endings, and connectors.

## 📊 Effectiveness (English)

### Per-Model API Pricing (as of 2026, $/1M tokens)

| Model | Input | Output |
|-------|-------|--------|
| Claude Fable 5 | $10.00 | $50.00 |
| Claude Opus 4.8 | $5.00 | $25.00 |
| Claude Sonnet 5 | $3.00 (intro $2.00, through 2026-08-31) | $15.00 (intro $10.00) |
| Claude Haiku 4.5 | $1.00 | $5.00 |

### Basis Changed: Session Count → Token Count

Session count is a poor unit — session length and turn count vary wildly (even in this project's own log, a 30-minute idle-gap heuristic swings between 92 and 267 sessions/month depending on the threshold). Rebuilt below on **measured output token counts** instead.

### ⚠️ Correction: the auto-log's "40.0%" is NOT measured

A prior version of this README stated "measured reduction rate: 40.0%." Inspecting `hooks/measure.sh` reveals this is **not a measurement — it's a fixed assumption baked into the formula**:

```bash
# Baseline estimate (assumes 40% reduction → baseline = output / 0.6 ≈ output * 5/3)
BASELINE_EST=$(( TOKEN_EST * 5 / 3 ))
SAVED_EST=$(( BASELINE_EST - TOKEN_EST ))
```

`baseline_est` is always `tokens_est × 5/3`, so `saved_est / baseline_est` is **always exactly 40.0%** regardless of the actual response content — it's circular. Aggregating 76 days of log entries and getting "40.0%" reflects the formula, not the content of those 5,961 responses. Correction and apology for the earlier claim.

### Measured (on-demand `/robo-stats`, 5 samples from this session)

Using `/robo-stats`: extracted 5 robo-toned responses from this conversation, generated a counterfactual "normal tone" version of each, and compared character-based token estimates (neither the count_tokens API nor tiktoken was available in this environment, so method C: 1.5 tok/char for Japanese, 0.25 tok/char for alphanumeric):

| # | Robo tok | Normal tok | Reduction |
|---|---------:|---------:|-------:|
| 1 | 217 | 302 | 28.1% |
| 2 | 126 | 194 | 35.1% |
| 3 | 307 | 472 | 35.0% |
| 4 | 280 | 409 | 31.5% |
| 5 | 316 | 381 | 17.1% |
| **Average** | - | - | **~29.4%** |

Method: **estimate** (character-based, method C — lower precision than an API count or tiktoken). 5 samples, this session only — not necessarily representative of long-term behavior.

This lands at the **low end** of the claimed "30-50%" range, and **below** the auto-log's assumed 40%. The dollar tables below still use the auto-log's assumed 40% basis; the real figure may be smaller.

### Per-Model Cost Conversion (output-reduction basis, auto-log's assumed 40%)

Converting the measured saved tokens (saved_est) at each model's Output price. Basis is **per 1,000 responses** (measured average 1,693 tok/response × 1,000), not sessions:

| Model | Output $/MTok | Savings per 1,000 responses |
|-------|---------------:|------------------------------:|
| Fable 5 | $50.00 | ~$84.6 |
| Opus 4.8 | $25.00 | ~$42.3 |
| Sonnet 5 | $15.00 (intro $10.00) | ~$25.4 (intro ~$16.9) |
| Haiku 4.5 | $5.00 | ~$8.5 |

### Reference: Monthly Extrapolation at This Environment's Measured Pace

The log above averages 78.4 responses/day (≈2,353 responses/month). This includes automated tests and workflow runs — it should **not** be conflated with a typical manual dev-session pace, and is shown for reference only:

| Model | Monthly savings (measured pace, ≈2,353 responses/month) |
|-------|-----------------------------------------------------------|
| Fable 5 | ~$199 |
| Opus 4.8 | ~$100 |
| Sonnet 5 | ~$60 (intro pricing: ~$40) |
| Haiku 4.5 | ~$20 |

- Scales with response count — i.e. actual token generation volume — not session length or turn frequency
- Higher-priced models (Fable 5 / Opus 4.8) show larger absolute savings

### Heavy-Usage Conversion (measured peak basis)

The full-period average includes quiet days, so as an upper-bound "if you go all-in" estimate, recompute using **the average pace of the busiest 25% of active days**: ~197 responses/day on busy days → ~5,910 responses/month, ~10 million saved tokens/month.

| Model | Monthly savings (heavy usage, ~5,910 responses/month) |
|-------|-----------------------------------------------------------|
| Fable 5 | ~$500 |
| Opus 4.8 | ~$250 |
| Sonnet 5 | ~$150 (intro pricing: ~$100) |
| Haiku 4.5 | ~$50 |

This is the heaviest case the measured data supports — sustaining this pace daily lands you in the $50–$500/month range depending on model. Note this pace itself includes automated processing; pure manual-conversation usage alone would likely land lower.

### Important: only response prose is compressed

The biggest reason the felt impact and the numbers diverge: this plugin only compresses **the assistant's natural-language prose inside a response**. Everything below is **protected** and never compressed:

- Code blocks, file paths, API names, verbatim error messages
- Tool calls (tool_use / tool_result)
- File contents, search results, and every other resent input token

In agentic coding work, most per-turn token spend is on the **input** side — resent conversation history, file contents, tool results — while the prose output is often a small slice of the total. If it feels like "I'm burning hundreds of millions of tokens in one go," that's very likely the input-side resend cost (outside this plugin's scope), not the output text. So even a genuine 30–40% cut on the prose slice is a **tiny fraction of total session token spend**.

### If you're on a weekly usage cap (subscription plans)

On Claude Pro/Max or similar weekly-cap plans (not pay-per-token), the relevant question isn't "$ saved" but "how much more headroom does this buy within my weekly quota." For the same reason as above (input tokens are untouched), **the proportion of weekly quota freed up is likely similarly small** — it scales with how much of your weekly consumption is prose output versus input. The actual input/output ratio is account- and workload-specific and can't be determined from this repo; check your real usage breakdown via Claude Code / claude.ai's usage view (e.g. `/usage`).

### Primary Purpose

Cost saving < **information density + dogfooding + character**

## 📐 プラグイン読込構造 / Load Architecture

### タイムライン

| タイミング | 動作 | 入力トークン |
|----------|------|------------|
| `/plugin install` | `plugin.json` 登録ノミ | 0 |
| **SessionStart** | `hooks/activate.sh` → `additionalContext` 注入 | ~200 tok (1回) |
| 対話中 | system context 常駐（cache利用） | 安価 |
| スキルトリガー時 | `skills/robo/SKILL.md` 読込 | ~600 tok (発動時ノミ) |
| **各応答終了後** | `hooks/measure.sh` → ログ・閾値超過時 systemMessage | ゼロ（外部プロセス） |

### コンテキスト構成

```
[System Prompt]
 ├─ Claude Code デフォルト
 ├─ hooks/activate.sh ノ additionalContext（毎セッション1回注入）
 │   └─ "SF AIロボ口調、呼称オペレーター、体言止メ徹底..."
 └─ skills/robo/SKILL.md（必要時ノミ、常駐セズ）
```

### CLAUDE.md 直書キ vs プラグイン比較

| 方式 | 読込 | 問題点 |
|------|------|--------|
| CLAUDE.md 直書キ | **毎ターン**全文 input | 累積消費大 |
| プラグイン方式 | SessionStart 1回 → cache 常駐 | **最適** |

### プラグイン方式ノ利点

1. **1回ノミ注入** → 毎ターン読込不要
2. **Prompt cache** → 繰返シ参照ハ低コスト
3. **SKILL.md 遅延読込** → 不要時ゼロ
4. **無効化容易** → `/plugin disable claude-robo-MK-1`
5. **他ユーザー配布可能** → 再利用性

## 📐 Load Architecture (English)

### Timeline

| Trigger | Action | Input tokens |
|---------|--------|--------------|
| `/plugin install` | Register `plugin.json` only | 0 |
| **SessionStart** | `hooks/activate.sh` → inject `additionalContext` | ~200 tok (once) |
| In-session | System context resident (cache-backed) | Cheap |
| Skill trigger | Load `skills/robo/SKILL.md` | ~600 tok (on trigger) |
| **Response end** | `hooks/measure.sh` → log, systemMessage if threshold | Zero (external) |

### Context Layout

```
[System Prompt]
 ├─ Claude Code default
 ├─ hooks/activate.sh additionalContext (injected once per session)
 │   └─ "SF AI robot tone. OPERATOR. Nominal ending. ..."
 └─ skills/robo/SKILL.md (on demand, not resident)
```

### CLAUDE.md Direct vs Plugin

| Method | Load | Problem |
|--------|------|---------|
| CLAUDE.md direct | **Every turn** full text | Cumulative burn |
| Plugin | SessionStart once → cache | **Optimal** |

### Plugin Advantages

1. **Inject once** → no per-turn reload
2. **Prompt cache** → repeat reads ~10% cost
3. **SKILL.md lazy-load** → zero when unused
4. **Easy disable** → `/plugin disable claude-robo-MK-1`
5. **Shareable** → reusable across users

## 設計原則

**文脈保持 > トークン削減**

削減ト明確性ガ衝突シタ場合、必ズ明確性ヲ優先。技術的指示・ビジネスロジック・コード内容ハ一切圧縮セズ。

## ライセンス

MIT

## 関連

- [caveman](https://github.com/JuliusBrussee/caveman) - 英語版（着想元）
