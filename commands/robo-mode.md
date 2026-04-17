---
description: 現在のロボ口調モード（hiragana/katakana）を表示
---

現在適用されているロボ口調モードを確認し、ユーザーに報告する。

以下を実行:

1. Bash ツールで以下を実行して現在モード取得:
   ```bash
   if [[ -f ~/.claude-robo-mode ]]; then
     cat ~/.claude-robo-mode
   elif [[ -n "${ROBO_STYLE:-}" ]]; then
     echo "$ROBO_STYLE (env var)"
   else
     echo "katakana (default)"
   fi
   ```

2. 結果に応じて以下のような簡潔なメッセージを返す:

```
📊 現在モード: <取得値>
優先順位: ~/.claude-robo-mode > $ROBO_STYLE > katakana(既定)
```

追加説明不要。状態報告のみ。
