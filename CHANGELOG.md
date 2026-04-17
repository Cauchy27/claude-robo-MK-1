# Changelog

All notable changes to claude-robo-MK-1.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [0.3.1] - 2026-04-17

### Changed
- Stop hook の systemMessage 表示を閾値方式に変更（デフォルト: saved_est >= 500 tok）
- 環境変数 `ROBO_THRESHOLD` で閾値調整可能
- ログ追記は全応答で継続（頻度変更なし）

### Rationale
- 短い応答まで毎回表示されていたノイズを抑制
- 意味のある削減量があった応答のみ可視化

## [0.3.0] - 2026-04-17

### Added
- Stop hook による削減量自動計測（`hooks/measure.sh`）
- ログファイル `~/.claude-robo-stats.jsonl` への追記
- systemMessage で応答ごとの削減推定表示
- README に計測仕様・ログ閲覧方法を追記

### Changed
- plugin.json / marketplace.json の description 更新（計測機能明記）
- SKILL.md に計測セクション追加（モデル自身の推定報告は禁止、hook 任せ）

## [0.2.0] - 2026-04-17

### Changed (Breaking)
- モード切替機能を完全廃止（`/robo-lite` `/robo-normal` `/robo-ultra` `/robo-off` `/robo-status` 削除）
- 単一トーン「SF AIロボ口調」に統合
- トーンを HAL 9000 / GLaDOS / TARS 風に刷新
- 呼称: ユーザー = オペレーター

### Added
- 体言止め最優先ルール（動詞削除による最大削減）
- 3レイヤー削減ロジック（削除 / 短縮 / 体言止め化）
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
