# 🤖 claude-robo-MK-1

> 📡 Claude Code の日本語出力を **SF AIロボ口調** に変換。トークンを **30-50%削減** しつつ文脈保持。

HAL 9000 / GLaDOS / TARS 風の冷徹・論理的・機械的トーン。常時有効、モード切替なし。

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
- SessionStart で自動有効化、モード切替なしのシンプル設計

## インストール

### 1. マーケットプレイス追加

```bash
/plugin marketplace add Cauchy27/claude-robo-MK-1
```

### 2. プラグインインストール

```bash
/plugin install claude-robo-MK-1@claude-robo-MK-1
```

### 3. セッション開始

Claude Code を再起動すると起動バナー表示:

```
📡 claude-robo-MK-1 起動シマス
```

## 無効化

以下のいずれかを発言:
- 「通常モード」
- 「普通に話して」
- 「ロボ解除」
- 「SFやめて」

完全アンインストールは:

```bash
/plugin uninstall claude-robo-MK-1
```

## 削減メカニズム

### Layer 1: 削除
- 敬語（です・ます）
- フィラー（ちなみに・とりあえず）
- 前置き（承知しました）
- 冗長修飾（少し・非常に）

### Layer 2: 短縮
- 〜かもしれません → 可能性アリ
- 〜だと思います → 断言化または削除
- 〜のようです → 〜と推定

### Layer 3: 体言止め化【最重要】
- 〜しました → 〜済 / 〜完了
- 〜します → 名詞化 / 〜予定
- 〜しています → 〜中

### 保持対象
コードブロック / ファイルパス / API名 / エラーメッセージ原文 / 数値 / 固有名詞 / ビジネスロジック

## 削減量の自動計測

v0.3.0 から Stop hook で各応答の削減量を自動計測:

```
📊 推定 ~450 tok / 節約 ~180 tok (@40%想定)
```

- ログは `~/.claude-robo-stats.jsonl` に追記
- 文字数から推定（Anthropic API 非依存）
- ベースラインは40%削減を仮定した推定値（厳密な原文比較ではない）

### 表示頻度

ノイズ抑制のため、**1応答あたりの節約量が500 tokens を超えた場合のみ** systemMessage 表示:

```
📊 推定 ~900 tok / 節約 ~600 tok (@40%想定)
```

閾値は環境変数で変更可能:

```bash
# 例: 200 tok 以上節約で表示
export ROBO_THRESHOLD=200
```

ログは全応答で追記されるため、累計は `~/.claude-robo-stats.jsonl` で確認可能。

### ログ形式

```jsonl
{"timestamp":"2026-04-17T12:34:56Z","chars":300,"tokens_est":450,"baseline_est":750,"saved_est":300}
```

累計節約量を見るには:

```bash
cat ~/.claude-robo-stats.jsonl | jq -s 'map(.saved_est) | add'
```

## 📊 節約効果 / Effectiveness

### 試算条件（20応答セッション、Sonnet 基準）

| 項目 | トークン | コスト |
|------|---------|-------|
| SessionStart hook 注入 | ~200 tok (input, cached) | ~$0.0006 |
| SKILL.md (発動時のみ) | ~600 tok | ~$0.0018 |
| Cache 再読 (19ターン × 10%) | ~20 tok | ~$0.00006 |
| 出力削減 | **-4,000 tok (output)** | **-$0.06** |
| **ネット節約** | **約 3,800 tok** | **~$0.057/セッション** |

### 感度

- **月100セッション → 約 $5-6 節約**
- 長セッション・出力多め → 効果拡大
- 短セッション・コード中心 → 効果縮小（コード保護のため）

### 主目的

金銭節約 < **情報密度向上 + ドッグフーディング + キャラクター性**

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
| `/plugin install` | `plugin.json` 登録のみ | 0 |
| **SessionStart** | `hooks/activate.sh` → `additionalContext` 注入 | ~200 tok (1回) |
| 対話中 | system context 常駐（cache利用） | 安価 |
| スキルトリガー時 | `skills/robo/SKILL.md` 読込 | ~600 tok (発動時のみ) |
| **各応答終了後** | `hooks/measure.sh` → ログ・閾値超過時 systemMessage | ゼロ（外部プロセス） |

### コンテキスト構成

```
[System Prompt]
 ├─ Claude Code デフォルト
 ├─ hooks/activate.sh の additionalContext（毎セッション1回注入）
 │   └─ "SF AIロボ口調、呼称オペレーター、体言止め徹底..."
 └─ skills/robo/SKILL.md（必要時のみ、常駐せず）
```

### CLAUDE.md 直書き vs プラグイン比較

| 方式 | 読込 | 問題点 |
|------|------|--------|
| CLAUDE.md 直書き | **毎ターン**全文 input | 累積消費大 |
| プラグイン方式 | SessionStart 1回 → cache 常駐 | **最適** |

### プラグイン方式の利点

1. **1回のみ注入** → 毎ターン読込不要
2. **Prompt cache** → 繰返し参照は低コスト
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

削減と明確性が衝突したら、必ず明確性を優先。技術的指示・ビジネスロジック・コード内容は一切圧縮しない。

## ライセンス

MIT

## 関連

- [caveman](https://github.com/JuliusBrussee/caveman) - 英語版（着想元）
