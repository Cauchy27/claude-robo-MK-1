# Changelog

All notable changes to claude-robo-MK-1.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

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
