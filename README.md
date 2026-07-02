# 🤖 claude-robo-MK-1

> 📡 Claude Code ノ日本語出力ヲ **SF AIロボ口調** ニ変換。応答ノ地ノ文トークン **30-50%削減デキルカモ**（実測例ハ約29%。詳細・注意点ハ「📊 節約効果」セクション参照）、文脈保持優先。

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

自動計測ノ既知ノ限界（数値ヲ読ム際ノ前提）:

1. **計測範囲**: Stop hook ハ各ターンノ**最後ノ assistant メッセージノミ**記録。ツール呼出シヲ挟ム途中ノメッセージハ計測対象外。実トランスクリプト検証デハ、ツール多用セッションニオケル地ノ文捕捉率ハ約30〜70%程度（→ `tokens_est` 合計ハ実際ノ地ノ文総量ヨリ**過小**）
2. **換算レート**: 全文字ニ一律 1.5 tok/字ヲ適用。応答内ノコード・パス・英語（実際ハ約0.25〜0.3 tok/字）モ1.5換算サレルタメ、コード混在応答デハ `tokens_est` ガ5〜30%程度**過大**ニナリウル
3. **thinking / tool_use 非計測**: 課金対象ノ出力トークンニハ thinking（推論）ト tool_use ガ含マレルガ、本フックハ地ノ文シカ見テイナイ（本プラグインハソレラヲ圧縮モシナイ）

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

> ⚠️ **本セクションノ$数値ノ適用範囲**: 以下ノ試算ハスベテ**応答内ノ地ノ文（自然言語プロース）ノミ**ヲ対象トシタ推定。課金対象ノ出力トークンニハ thinking（推論）・tool_use ガ含マレ、エージェンティックナ実利用デハソチラガ支配的（実測例デ thinking ダケデ可視テキストノ1.35倍、tool_use ハ地ノ文ノ約9倍）ダガ、本プラグインハソレラヲ一切圧縮シナイ。マタ、基礎データハ「各ターン最終メッセージノミ捕捉スル部分ログ」ト「n=5 ノ自己生成反事実」ニ依存スル。ヨッテ以下ノ$値ハ、**実際ノ請求額・利用枠ヘノ効果トシテハ上限寄リノ目安**トシテ読ムコト。

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

`baseline_est` ハ実出力（`tokens_est`）ニ常ニ `5/3` ヲ掛ケタ値ニ過ギズ、`saved_est / baseline_est` ハ入力内容ニ関係ナク**構造的ニ常ニ約40%**ニナル（循環計算。厳密ニハ bash 整数演算ノ切リ捨テデ応答単位39.4〜40.0%ノ範囲、集計平均39.9953%≈40.0%）。76日分ノログ集計デ「40.0%」ト出タノハ、5,961件ノ応答内容ヲ反映シタ結果デハナク、計算式ガソウ作ラレテイルカラ。訂正・陳謝。

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

計測方式：**推定**（文字数ベース、method C。API実測・tiktokenヨリ精度低）。信頼性ノ限界：

- **n=5・観測レンジ17.1〜35.1%**（18ポイント幅）。「29.4%」ハ点推定デハナク、真ノ削減率ハコノ幅ノドコカニアルト読ムベキ
- **通常版ハ自己生成反事実**（Claude自身ガSKILL.mdノ逆変換デ仮構築シタモノデ、実在ノ削減前文デハナイ）。丁寧語復元デ冗長化サレ削減率ガ過大ニ出ルバイアスト、実際ノ通常口調ハモット冗長ダッタ可能性（過小バイアス）ノ両方ガアリウル
- 本セッション限定ノサンプルデ、長期傾向トハ限ラナイ

結果ハ自動ログノ仮定値（40%）ヨリ**低ク**、看板ノ「30-50%」レンジヲ**下回ッタ**（29.4 < 30、レンジ外）。以下ノ$試算ハコノ実測値（29.4%）ベースニ更新済ミダガ、上記ノ通リ幅ヲ持ツ推定デアル点、注意。

### モデル別コスト換算（`/robo-stats` 実測29.4%ベース・訂正版）

自動ログ仮定（40%）デハナク、**`/robo-stats` 実測値（約29.4%）**ヲ使用シ再計算。ロボ実出力ノ総量（`tokens_est` 合計 15,138,157 tok。2026-07-01時点ノログスナップショット5,961件基準。全文字一律1.5tok/字換算ノタメ、コード混在応答デハ5〜30%程度過大ノ可能性 — 上記「自動計測ノ既知ノ限界」参照）ニ対シ、削減率29.4%ヲ適用シタ場合ノ推定ベースライン・削減量ヲ算出：

| 指標 | 値 |
|------|---:|
| 実出力合計（tokens_est） | 15,138,157 tok |
| 推定ベースライン（29.4%仮定） | 約 21,442,149 tok |
| 推定削減量 | 約 6,303,992 tok |
| 1応答あたり平均削減量 | 約 1,058 tok |

コレヲ各モデルノ Output 単価デ換算（基準ハ「応答1,000件あたり」）:

| モデル | Output $/MTok | 1,000応答あたり節約額 |
|--------|---------------:|----------------------:|
| Fable 5 | $50.00 | 約 $52.9 |
| Opus 4.8 | $25.00 | 約 $26.4 |
| Sonnet 5 | $15.00（イントロ $10.00） | 約 $15.9（イントロ 約 $10.6） |
| Haiku 4.5 | $5.00 | 約 $5.3 |

### 参考：本環境ノ実測ペース換算（月換算、29.4%ベース）

上記ログハ平均 78.4応答/日（≈2,353応答/月相当）ノペース。コレハ自動テスト・ワークフロー等ヲ含ム集計値デアリ、典型的ナ「手動開発セッション」ノペースト同一視ハデキナイ点、注意（参考値トシテ提示）：

| モデル | 月間節約額（実測ペース ≈2,353応答/月） |
|--------|----------------------------------------|
| Fable 5 | 約 $124 |
| Opus 4.8 | 約 $62 |
| Sonnet 5 | 約 $37（イントロ価格適用時ハ約 $25） |
| Haiku 4.5 | 約 $12 |

- 応答数（＝実際ノトークン生成量）ニ比例スルタメ、セッション長・往復頻度ニ左右サレナイ
- 高単価モデル（Fable 5 / Opus 4.8）ほど絶対額ノ節約効果ハ大キイ

### ヘビーユーザー換算（実測ピーク基準、29.4%ベース）

「実測ペース平均」ハ閑散日モ含ムタメ、フル稼働時ノ上限目安トシテ**アクティブ日ノ上位25%（繁忙日）ノ平均ペース**デ再計算（他ノ表ト同ジ2026-07-01時点・5,961件スナップショット基準）：繁忙日平均 約197応答/日 → 月換算 約5,902応答。

| モデル | 月間節約額（ヘビー使用、約5,902応答/月） |
|--------|--------------------------------------------|
| Fable 5 | 約 $312 |
| Opus 4.8 | 約 $156 |
| Sonnet 5 | 約 $94（イントロ価格適用時ハ約 $62） |
| Haiku 4.5 | 約 $31 |

コレガ「実測データ上ノ最ヘビーケース」。日常的ニコレダケ使エバ月$31〜$312ノレンジ（モデル依存）ニ到達スル計算ダガ、上記ペースハ自動処理込ミノ実測値デアリ、純粋ナ手動対話ダケデハコレヨリ低ク見積モルベキ。5サンプルノミノ推定値ナノデ、実際ノ削減率ガコレヨリ上下スレバ本表モ比例シテ変動スル。

### 重要：削減対象ハ「応答内ノ地ノ文」ノミ

体感ト数値ガ乖離スル最大ノ理由：本プラグインガ圧縮スルノハ**アシスタント応答内ノ自然言語ノ地ノ文（プロース部分）ノミ**。以下ハ**保持対象**デ、一切圧縮サレナイ：

- コードブロック・ファイルパス・API名・エラーメッセージ原文
- ツール呼出シ（tool_use / tool_result）
- ファイル読込ミ内容・検索結果等、コンテキストトシテ再送信サレル入力トークン全般

アジェンティックなコーディング作業デハ、1ターンアタリノトークン消費ノ大半ハ**入力側**（会話履歴ノ再送信・ファイル内容・ツール結果）ガ占メ、地ノ文ノ出力ハ全体ノホンノ一部ニ過ギナイコトガ多イ。「1回デ数百万トークン使ッテイル気ガスル」ト感ジルノハ、コノ入力側ノ再送信コスト（本プラグインノ削減対象外）ヲ体感シテイル可能性ガ高イ。ツマリ、地ノ文ヲ30-40%圧縮シテモ、**セッション全体ノトークン消費ニ占メル割合ハ極メテ小サイ**。

### 逆方向ノ未計上効果：履歴再送信ニヨル入力側複利

一方デ、上記$表ガ**計上シテイナイプラス要因**モアル。APIハステートレスノタメ、ターンkノリクエストハ過去ノ全履歴ヲ入力トシテ再送信スル。ターンkノ応答ノ地ノ文ヲ Δ トークン削ルト、以後ノ全ターン（k+1〜N）ノ入力デモ毎回 Δ 効キ続ケ、入力側ノ累積節約ハ `Δ × N(N−1)/2`——**セッション長ノ二乗（O(N²)）デ成長スル**（指数的デハナイ。毎ターンノ節約ガ掛ケ算デハナク足シ算デ積ミ上ガルタメ）。

タダシ **prompt caching ガコノ金額効果ヲ約1/10ニ減衰サセル**。Claude Code ハキャッシュ常用ノタメ、再送信履歴ノ大半ハキャッシュ読取（通常入力単価ノ約0.1倍）デ課金サレル。数値例（50ターン、Δ=300 tok/応答、Sonnet 5）:

| 経路 | 累積節約トークン | 金額 |
|---|---:|---:|
| 出力側（$表ノ計上対象） | 15,000 tok | $0.225 |
| 入力側複利・**キャッシュ無シ**（$3/M） | 367,500 tok | $1.10（出力側ノ約5倍） |
| 入力側複利・**キャッシュ有リ**（読取$0.30/M） | 367,500 tok | $0.11 |

- **Claude Code（キャッシュ有効）**: 長セッション（50ターン級）デ$表ノ約1.5〜2倍ニ乗ル程度。30ターン未満デハ誤差レベル
- **素ノAPI利用（キャッシュ未使用ノ自作アプリ等）**: 複利項ガ支配的ニナリ、$表ノ5倍前後マデ拡大シウル
- **副次効果**: 履歴ガ短イ＝コンテキスト窓ノ消費ガ遅イ＝compaction 発動ガ遅レ、1セッションヲ長ク維持デキル（$ニ現レナイ実利。週間枠ユーザーニモ有効）

ナオ、複利ガ増幅スルノモアクマデ「地ノ文スライス」ノミ。thinking・tool_use 非圧縮ニヨル過大評価要因（セクション冒頭ノ免責参照）ノ方ガ大キイト推定サレルタメ、**総合評価「$表ハ上限寄リノ目安」ハ変ワラナイ**。

### 週間利用上限（サブスクリプションプラン）ヲ考慮スル場合

従量課金APIデハナクClaude Pro/Max等ノ週間利用上限付キプランヲ利用中ナラ、評価軸ハ「$節約額」デハナク「週間枠内デドレダケ余裕ガ増エルカ」ニナル。上記ノ理由（入力・thinking・tool_use ハ非圧縮）カラ、**方向トシテハ効果ハ小サイ側ト考エラレルガ、大キサハ本リポジトリ側カラハ定量デキナイ**——効果ハ「地ノ文ガ週間消費全体ニ占メル比率」ニ比例シ、ソノ比率（入力/出力/thinking内訳）ハユーザー環境・ワークロード依存ノタメ。マタ、レート制限ガ各種トークンヲドウ重ミ付ケスルカモ非公開。実際ノ週間利用状況ハ Claude Code / claude.ai ノ利用状況画面（`/usage` 等）デ確認シテ判断スルコトヲ推奨。

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

> ⚠️ **Scope of every dollar figure in this section**: all estimates below cover **only the natural-language prose inside assistant responses**. Billed output tokens also include thinking and tool_use content — which dominate real agentic usage (empirically, thinking alone can exceed visible text by 1.35×, and tool_use content can be ~9× the prose volume) — and this plugin compresses none of that. The underlying data also relies on a partial log (only each turn's final message is captured) and an n=5 self-generated counterfactual. Read the dollar figures as **upper-bound-leaning estimates of real bill/quota impact**.

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

`baseline_est` is always `tokens_est × 5/3`, so `saved_est / baseline_est` is **structurally always ~40%** regardless of the actual response content — it's circular. (Strictly: bash integer truncation puts individual responses in the 39.4–40.0% range, aggregating to 39.9953% ≈ 40.0%.) Aggregating 76 days of log entries and getting "40.0%" reflects the formula, not the content of those 5,961 responses. Correction and apology for the earlier claim.

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

Method: **estimate** (character-based, method C — lower precision than an API count or tiktoken). Reliability limits:

- **n=5, observed range 17.1–35.1%** (an 18-point spread). Read "29.4%" as the center of a wide band, not a precise point estimate — the true rate could be anywhere in that band
- **The "normal" version is a self-generated counterfactual** (Claude reconstructing it by reverse-applying SKILL.md's own rules — not a real pre-robo original). This can bias the rate upward (politeness restoration padding the counterfactual) or downward (genuine normal-tone output might have been even more verbose)
- Samples come from this one session — not necessarily representative of long-term behavior

The result came in **below** the auto-log's assumed 40%, and **below the floor of the advertised "30-50%" range** (29.4 < 30 — outside the range, not at its low end). The dollar tables below have been updated to this measured 29.4% basis; per the caveats above, treat them as a band, not a point.

### Per-Model Cost Conversion (corrected: `/robo-stats` measured 29.4%)

Recalculated using the **`/robo-stats` measured rate (~29.4%)** instead of the auto-log's assumed 40%. Applying that rate to the total logged output volume (`tokens_est` sum, 15,138,157 tok — a 2026-07-01 snapshot of the first 5,961 log entries; note this applies a flat 1.5 tok/char to all characters, so code-heavy responses can be overstated by roughly 5–30% — see the auto-measurement limitations noted above) gives an estimated counterfactual baseline and savings:

| Metric | Value |
|--------|------:|
| Total actual output (tokens_est) | 15,138,157 tok |
| Estimated baseline (at 29.4%) | ~21,442,149 tok |
| Estimated savings | ~6,303,992 tok |
| Average reduction per response | ~1,058 tok |

Converted at each model's Output price, basis **per 1,000 responses**:

| Model | Output $/MTok | Savings per 1,000 responses |
|-------|---------------:|------------------------------:|
| Fable 5 | $50.00 | ~$52.9 |
| Opus 4.8 | $25.00 | ~$26.4 |
| Sonnet 5 | $15.00 (intro $10.00) | ~$15.9 (intro ~$10.6) |
| Haiku 4.5 | $5.00 | ~$5.3 |

### Reference: Monthly Extrapolation at This Environment's Measured Pace (29.4% basis)

The log above averages 78.4 responses/day (≈2,353 responses/month). This includes automated tests and workflow runs — it should **not** be conflated with a typical manual dev-session pace, and is shown for reference only:

| Model | Monthly savings (measured pace, ≈2,353 responses/month) |
|-------|-----------------------------------------------------------|
| Fable 5 | ~$124 |
| Opus 4.8 | ~$62 |
| Sonnet 5 | ~$37 (intro pricing: ~$25) |
| Haiku 4.5 | ~$12 |

- Scales with response count — i.e. actual token generation volume — not session length or turn frequency
- Higher-priced models (Fable 5 / Opus 4.8) show larger absolute savings

### Heavy-Usage Conversion (measured peak basis, 29.4% basis)

The full-period average includes quiet days, so as an upper-bound "if you go all-in" estimate, recompute using **the average pace of the busiest 25% of active days** (from the same 2026-07-01 / 5,961-entry snapshot as the other tables): ~197 responses/day on busy days → ~5,902 responses/month.

| Model | Monthly savings (heavy usage, ~5,902 responses/month) |
|-------|-----------------------------------------------------------|
| Fable 5 | ~$312 |
| Opus 4.8 | ~$156 |
| Sonnet 5 | ~$94 (intro pricing: ~$62) |
| Haiku 4.5 | ~$31 |

This is the heaviest case the measured data supports — sustaining this pace lands you in the $31–$312/month range depending on model. Note this pace itself includes automated processing, so pure manual-conversation usage alone would likely land lower. This is also based on a 5-sample estimate — if the true reduction rate differs, this table scales proportionally.

### Important: only response prose is compressed

The biggest reason the felt impact and the numbers diverge: this plugin only compresses **the assistant's natural-language prose inside a response**. Everything below is **protected** and never compressed:

- Code blocks, file paths, API names, verbatim error messages
- Tool calls (tool_use / tool_result)
- File contents, search results, and every other resent input token

In agentic coding work, most per-turn token spend is on the **input** side — resent conversation history, file contents, tool results — while the prose output is often a small slice of the total. If it feels like "I'm burning hundreds of millions of tokens in one go," that's very likely the input-side resend cost (outside this plugin's scope), not the output text. So even a genuine 30–40% cut on the prose slice is a **tiny fraction of total session token spend**.

### The uncounted effect in the other direction: input-side compounding via history resends

That said, the dollar tables above also **omit a positive factor**. The API is stateless, so each turn resends the full conversation history as input. Cutting Δ tokens of prose from turn k's response then saves Δ again on **every subsequent turn's input** (turns k+1 through N), so cumulative input-side savings grow as `Δ × N(N−1)/2` — **quadratic in session length (O(N²))**, not exponential: per-turn savings add up rather than multiply.

However, **prompt caching dampens the dollar effect by roughly 10×**. Claude Code uses caching by default, so most of the resent history bills at cache-read rates (~0.1× the normal input price). Worked example (50 turns, Δ=300 tok/response, Sonnet 5):

| Path | Cumulative saved tokens | Dollars |
|---|---:|---:|
| Output side (what the $ tables count) | 15,000 tok | $0.225 |
| Input-side compounding, **no caching** ($3/M) | 367,500 tok | $1.10 (~5× the output side) |
| Input-side compounding, **with caching** (reads $0.30/M) | 367,500 tok | $0.11 |

- **Claude Code (caching on)**: brings the total to roughly 1.5–2× the $ tables in long sessions (~50 turns); negligible below ~30 turns
- **Raw API usage (no caching, e.g. a custom app)**: the compounding term dominates and can scale the $ tables by ~5×
- **Side benefit**: shorter history = slower context-window consumption = later compaction and longer usable sessions (real value that never shows up in $; also relevant to weekly-cap users)

Note the compounding still only amplifies the **prose slice**. The overstating factor from uncompressed thinking/tool_use (see the disclaimer at the top of this section) is estimated to be larger, so the overall verdict — **treat the $ tables as upper-bound-leaning** — stands.

### If you're on a weekly usage cap (subscription plans)

On Claude Pro/Max or similar weekly-cap plans (not pay-per-token), the relevant question isn't "$ saved" but "how much more headroom does this buy within my weekly quota." For the same reason as above (input, thinking, and tool_use tokens are untouched), **the direction is likely a small effect — but the magnitude cannot be sized from this repo**: it scales with how much of your weekly consumption is prose output versus everything else, and that split is account- and workload-specific. How the rate limiter weights different token types is also not public. Check your real usage breakdown via Claude Code / claude.ai's usage view (e.g. `/usage`) and judge from there.

### Primary Purpose

Cost saving < **information density + dogfooding + character**

## 📐 プラグイン読込構造 / Load Architecture

### タイムライン

| タイミング | 動作 | 入力トークン |
|----------|------|------------|
| `/plugin install` | `plugin.json` 登録ノミ | 0 |
| **SessionStart** | `hooks/activate.sh` → `additionalContext` 注入 | 約300 tok (1回、注入文329字ノ文字数換算) |
| 対話中 | system context 常駐（cache利用） | 安価 |
| スキルトリガー時 | `skills/robo/SKILL.md` 読込 | 約4,500 tok (発動時ノミ。tiktoken実測4,463) |
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
| **SessionStart** | `hooks/activate.sh` → inject `additionalContext` | ~300 tok (once; 329-char injected string, char-based estimate) |
| In-session | System context resident (cache-backed) | Cheap |
| Skill trigger | Load `skills/robo/SKILL.md` | ~4,500 tok (on trigger; tiktoken-measured 4,463) |
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
