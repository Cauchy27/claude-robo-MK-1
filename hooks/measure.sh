#!/usr/bin/env bash
# claude-robo-MK-1 Stop hook - token reduction measurement
# stdin から JSON を受け取り、transcript から最新 assistant message を抽出し
# 文字数・トークン推定・削減推定を計算してログ追記。systemMessage で表示。

set -e

STATS_FILE="${HOME}/.claude-robo-stats.jsonl"
INPUT=$(cat)

# jq 存在チェック
if ! command -v jq >/dev/null 2>&1; then
  echo '{}'
  exit 0
fi

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")

if [ -z "$TRANSCRIPT_PATH" ] || [ ! -f "$TRANSCRIPT_PATH" ]; then
  # transcript未取得時は静かに終了
  echo '{}'
  exit 0
fi

# 逆順読み取り: macOS は tac 無しのため tail -r または awk で代替
reverse_lines() {
  if command -v tac >/dev/null 2>&1; then
    tac "$1"
  elif command -v tail >/dev/null 2>&1 && tail -r </dev/null >/dev/null 2>&1; then
    tail -r "$1"
  else
    awk '{a[NR]=$0} END{for(i=NR;i>=1;i--) print a[i]}' "$1"
  fi
}

# 最新の assistant message のテキストを抽出
# 末尾から走査し、最初に見つかった assistant role の行を取得
LAST_ASSISTANT_LINE=$(reverse_lines "$TRANSCRIPT_PATH" 2>/dev/null | \
  awk '/"role":"assistant"/ {print; exit}')

if [ -z "$LAST_ASSISTANT_LINE" ]; then
  echo '{}'
  exit 0
fi

# content 配列内の text ブロックを結合
LAST_TEXT=$(printf '%s\n' "$LAST_ASSISTANT_LINE" | \
  jq -r '(.message.content // .content // []) | if type=="array" then map(select(.type=="text") | .text) | join(" ") else (. | tostring) end' 2>/dev/null || echo "")

if [ -z "$LAST_TEXT" ] || [ "$LAST_TEXT" = "null" ]; then
  echo '{}'
  exit 0
fi

# 文字数（マルチバイト対応: wc -m）
CHAR_COUNT=$(printf '%s' "$LAST_TEXT" | wc -m | tr -d ' ')

if [ "$CHAR_COUNT" -lt 20 ]; then
  # 極端に短い応答は記録しない
  echo '{}'
  exit 0
fi

# トークン推定（日本語平均 1.5 tok/char）
TOKEN_EST=$(( CHAR_COUNT * 3 / 2 ))
# ベースライン推定（40%削減想定 → baseline = output / 0.6 ≈ output * 5/3）
BASELINE_EST=$(( TOKEN_EST * 5 / 3 ))
SAVED_EST=$(( BASELINE_EST - TOKEN_EST ))

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ログ追記
mkdir -p "$(dirname "$STATS_FILE")"
printf '{"timestamp":"%s","chars":%d,"tokens_est":%d,"baseline_est":%d,"saved_est":%d}\n' \
  "$TIMESTAMP" "$CHAR_COUNT" "$TOKEN_EST" "$BASELINE_EST" "$SAVED_EST" >> "$STATS_FILE"

# systemMessage 出力
printf '{"systemMessage":"📊 推定 ~%d tok / 節約 ~%d tok (@40%%想定)"}\n' \
  "$TOKEN_EST" "$SAVED_EST"
