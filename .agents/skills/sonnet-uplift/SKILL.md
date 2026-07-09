---
name: sonnet-uplift
description: |
  【何をするか】このスキルは上位モデル（親セッションモデル）が設計した品質フレームワーク
  （完了条件チェックリスト・自己検証ループ・エスカレーション基準）を model: sonnet / haiku 指定の
  エージェント定義に埋め込み、低コストモデルの実行品質を引き上げる。
  【いつ使うか】sonnet/haiku 指定エージェントの品質強化時、親継承エージェントの sonnet 降格検討時、
  新規エージェント・サブエージェント作成で model を指定する時に自動発動。
  【発動キーワード】「Sonnet強化」「Sonnet最適化」「アップリフト」「uplift」「モデル引き上げ」
  「品質ゲート埋め込み」「検証チェックリスト埋め込み」「エスカレーション基準」「テスト先行アップリフト」「テストファースト委譲」
allowed-tools: Read, Bash, Glob, Grep
execution_type: subagent
version: 1.2.0
updated: 2026-07-10
---

# Sonnet Uplift

Codex / Antigravity (Gemini) 共通の参照ラッパー。

**詳細な手順と運用ルールは、Claude 側の正本である `.claude/skills/sonnet-uplift/SKILL.md` に記載されています。**
エージェントは、必ずファイル読み込みツール（`view_file` など）を使って上記正本を読み込んでから作業を開始してください。

Claude 固有のツール名や手順は、利用可能な同等の手段（例: `run_command`, `invoke_subagent`, `schedule` 等）に読み替えてください。
