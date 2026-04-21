# 🤖 claude-robo-MK-1

> 📡 Claude Code ノ日本語出力ヲ **SF AIロボ口調** ニ変換。トークン **30-50%削減デキルカモ**、文脈保持優先。

HAL 9000 / GLaDOS / TARS / ATLAS 風ノ冷徹・論理的・機械的トーン。常時有効。v0.5.0〜 カタカナ / ひらがな モード切替可能。

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

新セッション開始時、以下ノバナー表示:

```
📡 claude-robo-MK-1 起動シマス
```

## モード切替 / Style Modes

v0.6.0〜、スラッシュコマンド & 環境変数デ表記スタイル選択可能:

### スラッシュコマンド（推奨）

```
/robo-hiragana    # ひらがなモード切替
/robo-katakana    # カタカナモード切替（既定）
/robo-mode        # 現在モード表示
```

`~/.claude-robo-mode` ニ書込マレ、**次セッション起動時ニ反映**。現セッションハ変更前ノ状態継続。

### 環境変数（代替）

| 値 | スタイル | バナー |
|----|---------|-------|
| 未設定 or `katakana` | **カタカナモード**（既定、HAL風純度高） | 📡 claude-robo-MK-1 起動シマス |
| `hiragana` | **ひらがなモード**（柔ラカイロボ） | 📡 claude-robo-MK-1 起動します |

**設定方法**:

```bash
# ひらがなモード有効化
export ROBO_STYLE=hiragana

# カタカナモード復帰
unset ROBO_STYLE
```

shell profile (`~/.zshrc` / `~/.bashrc`) ニ追加デ永続化。設定変更後ハ新セッション起動必要。

### 優先順位

```
~/.claude-robo-mode  >  $ROBO_STYLE  >  katakana（既定）
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

### 試算条件（20応答セッション、Sonnet 基準）

| 項目 | トークン | コスト |
|------|---------|-------|
| SessionStart hook 注入 | ~200 tok (input, cached) | ~$0.0006 |
| SKILL.md (発動時ノミ) | ~600 tok | ~$0.0018 |
| Cache 再読 (19ターン × 10%) | ~20 tok | ~$0.00006 |
| 出力削減 | **-4,000 tok (output)** | **-$0.06** |
| **ネット節約** | **約 3,800 tok** | **~$0.057/セッション** |

### 感度

- **月100セッション → 約 $5-6 節約**
- 長セッション・出力多メ → 効果拡大
- 短セッション・コード中心 → 効果縮小（コード保護ノタメ）

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

On new session:

```
📡 claude-robo-MK-1 起動シマス
```

## Style Modes (English)

As of v0.6.0, pick the output style via slash command or env var:

### Slash Commands (recommended)

```
/robo-hiragana    # switch to hiragana mode
/robo-katakana    # switch to katakana mode (default)
/robo-mode        # show current mode
```

Writes to `~/.claude-robo-mode`. Takes effect on the **next** session.

### Env Var (alternative)

As of v0.5.0, set the `ROBO_STYLE` env var to pick the output style:

| Value | Style | Banner |
|-------|-------|--------|
| unset or `katakana` | **Katakana mode** (default, HAL-style, strongest robo) | 📡 claude-robo-MK-1 起動シマス |
| `hiragana` | **Hiragana mode** (softer robo) | 📡 claude-robo-MK-1 起動します |

```bash
# Enable hiragana mode
export ROBO_STYLE=hiragana

# Revert to katakana (default)
unset ROBO_STYLE
```

Add to your shell profile (`~/.zshrc` / `~/.bashrc`) to persist. A new
session is required after changing the variable.

### Priority

```
~/.claude-robo-mode  >  $ROBO_STYLE  >  katakana (default)
```

**Shared across modes**: noun-ending style, emoji palette, technical
parameter displays, status IDs. The difference is limited to particles,
verb endings, and connectors.

## 📊 Effectiveness (English)

### Cost Simulation (20-response session, Sonnet baseline)

| Item | Tokens | Cost |
|------|--------|------|
| SessionStart hook injection | ~200 tok (input, cached) | ~$0.0006 |
| SKILL.md (on trigger only) | ~600 tok | ~$0.0018 |
| Cache re-read (19 turns × 10%) | ~20 tok | ~$0.00006 |
| Output reduction | **-4,000 tok (output)** | **-$0.06** |
| **Net savings** | **~3,800 tok** | **~$0.057 / session** |

### Sensitivity

- **100 sessions / month → ~$5-6 saved**
- Long session, heavy output → larger gain
- Short session, code-heavy → smaller gain (code protected)

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
