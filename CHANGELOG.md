# Changelog

All notable changes to claude-robo-MK-1.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [0.7.0] - 2026-04-17

### Added
- **オンデマンド真ノ削減率実測機能**
  - `/robo-stats` コマンド新設
  - 自然言語トリガー対応（「実測して」「本当の削減率」等）
  - 直近3-5件ノロボ応答ヲ文脈カラ抽出 → 通常日本語版ヲ仮想生成 → 両版ノ実トークン数測定
  - 計測優先順位: `count_tokens` API → tiktoken → 文字数推定

### Changed
- SKILL.md / README.md ニ オンデマンド実測セクション追加
- 自動計測ノ `tokens_est` / `saved_est` ニ「推定値」注記明記

### Background
- 従来ノ自動計測ハ `tokens_est = chars × 1.5` ノ推定ノミデ、ベースラインモ40%削減前提ノ逆算値
- 真ノ削減率ヲ知リタイ時ニ `/robo-stats` デ実測可能化

## [0.6.0] - 2026-04-17

### Added
- **スラッシュコマンド経由ノモード切替**
  - `/robo-hiragana` → ひらがなモード切替
  - `/robo-katakana` → カタカナモード切替（既定）
  - `/robo-mode` → 現在モード表示
- `~/.claude-robo-mode` 設定ファイル（コマンドガ書込）
- `commands/` ディレクトリ復活（v0.2.0デ廃止後再導入）

### Changed
- `hooks/activate.sh`: モード決定優先順位変更
  - `~/.claude-robo-mode` > `$ROBO_STYLE` > `katakana`（既定）
- SKILL.md / README.md ニ コマンド方式追記

## [0.5.1] - 2026-04-17

### Fixed
- marketplace.json ガ Claude Code UI デプラグイン非表示トナル不具合修正
  - `plugins[].version` フィールド追加（UI表示必須）
  - `description` / `homepage` ヲ `metadata` 下ニ移動（規約準拠）
  - 参考: thedotmack/claude-mem ノ marketplace.json フォーマット
- `scripts/release.sh` モ marketplace.json ノ `plugins[].version` 同期対応

## [0.5.0] - 2026-04-17

### Added
- **ROBO_STYLE 環境変数ニヨルモード切替**
  - `katakana`（既定）/ `hiragana` ノ2モード
  - 両モード共通: 体言止メ・絵文字・技術パラメータ・ステータスID
  - 差異: 助詞・語尾・接続詞ノ表記ノミ
- README.md ニ モード切替セクション追加
- SKILL.md ニ モード別ルール明記

### Changed
- 削減率表現「30-50%削減」→「30-50%削減デキルカモ」（誠実化）
- README.md 全体ヲロボ口調ニ統一（EN部分ハ保持）
- CHANGELOG.md ヲロボ口調ニ統一

## [0.4.0] - 2026-04-17

### Added
- 近未来SFロボ演出強化（技術パラメータ・ステータスID・構造化ブロック）
- 技術パラメータ語彙（「ターゲット捕捉率 98.7%」「コア温度 42.3°C」等）
- ステータスID / プロトコル表示（`STATUS: NOMINAL` `[SYS-001]` `PROTOCOL-Δ`）
- 構造化レスポンスブロック（`▼ INPUT ANALYSIS` 等、長文応答用）
- 絵文字パレット拡張（システム / 状態 / 動作 / 通信、4カテゴリ約20種）
- `scripts/release.sh` 追加: Conventional Commits 解析デ SemVer 自動判定

### Changed
- カタカナ優先ルール明文化（助詞「ヲ/ニ/ヘ/デ」 or 削除）
- ひらがな漏出抑止

### Rejected
- 効果音挿入案（冗長ノタメ採用セズ）

## [0.3.1] - 2026-04-17

### Changed
- Stop hook ノ systemMessage 表示ヲ閾値方式ニ変更（デフォルト: saved_est >= 500 tok）
- 環境変数 `ROBO_THRESHOLD` デ閾値調整可能
- ログ追記ハ全応答デ継続（頻度変更ナシ）

### Rationale
- 短イ応答マデ毎回表示サレテイタノイズ抑制
- 意味ノアル削減量ガアッタ応答ノミ可視化

## [0.3.0] - 2026-04-17

### Added
- Stop hook ニヨル削減量自動計測（`hooks/measure.sh`）
- ログファイル `~/.claude-robo-stats.jsonl` ヘノ追記
- systemMessage デ応答毎ノ削減推定表示
- README ニ計測仕様・ログ閲覧方法追記

### Changed
- plugin.json / marketplace.json ノ description 更新（計測機能明記）
- SKILL.md ニ計測セクション追加（モデル自身ノ推定報告ハ禁止、hook任セ）

## [0.2.0] - 2026-04-17

### Changed (Breaking)
- モード切替機能完全廃止（`/robo-lite` `/robo-normal` `/robo-ultra` `/robo-off` `/robo-status` 削除）
- 単一トーン「SF AIロボ口調」ニ統合
- トーンヲ HAL 9000 / GLaDOS / TARS 風ニ刷新
- 呼称: ユーザー = オペレーター

### Added
- 体言止メ最優先ルール（動詞削除ニヨル最大削減）
- 3レイヤー削減ロジック（削除 / 短縮 / 体言止メ化）
- 起動バナー「📡 claude-robo-MK-1 起動シマス」

### Removed
- `commands/` ディレクトリ全削除
- モード管理機構

## [0.1.0] - 2026-04-17

### Added
- 初回リリース
- skills/robo/SKILL.md（ロボ口調ルール）
- hooks/activate.sh（SessionStart 自動有効化）
- .claude-plugin/plugin.json + marketplace.json
