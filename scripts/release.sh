#!/usr/bin/env bash
# claude-robo-MK-1 release automation
#
# Usage:
#   bash scripts/release.sh           # auto-detect bump from commits since last tag
#   bash scripts/release.sh patch     # force patch bump (x.y.Z)
#   bash scripts/release.sh minor     # force minor bump (x.Y.0)
#   bash scripts/release.sh major     # force major bump (X.0.0)
#   bash scripts/release.sh --dry-run # preview without writing
#
# Conventional Commits mapping:
#   feat!: / BREAKING CHANGE: -> major
#   feat:                      -> minor
#   fix: / perf:               -> patch
#   others (docs/chore/...)   -> no bump (exit 0)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_JSON="${ROOT}/.claude-plugin/plugin.json"

DRY_RUN=0
FORCE_BUMP=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    major|minor|patch) FORCE_BUMP="$arg" ;;
    -h|--help)
      sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

cd "$ROOT"

# 1. Sanity: working tree clean
if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: working tree not clean. commit or stash first." >&2
  exit 1
fi

# 2. Current version
current=$(grep -oE '"version": "[0-9]+\.[0-9]+\.[0-9]+"' "$PLUGIN_JSON" | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
if [[ -z "$current" ]]; then
  echo "error: cannot parse version from $PLUGIN_JSON" >&2
  exit 1
fi
IFS='.' read -r major minor patch <<< "$current"

# 3. Determine bump
bump="$FORCE_BUMP"
if [[ -z "$bump" ]]; then
  last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
  range="${last_tag:+${last_tag}..HEAD}"
  range="${range:-HEAD}"
  msgs=$(git log --pretty=%B $range)

  if echo "$msgs" | grep -qE '^(feat|fix|perf|refactor)(\([^)]+\))?!:' \
     || echo "$msgs" | grep -q 'BREAKING CHANGE:'; then
    bump="major"
  elif echo "$msgs" | grep -qE '^feat(\([^)]+\))?:'; then
    bump="minor"
  elif echo "$msgs" | grep -qE '^(fix|perf)(\([^)]+\))?:'; then
    bump="patch"
  fi
fi

if [[ -z "$bump" ]]; then
  echo "no bump-worthy commits since last tag. nothing to release."
  exit 0
fi

case "$bump" in
  major) major=$((major+1)); minor=0; patch=0 ;;
  minor) minor=$((minor+1)); patch=0 ;;
  patch) patch=$((patch+1)) ;;
esac
new_version="${major}.${minor}.${patch}"

echo "[release] $current -> $new_version ($bump)"

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[release] dry-run: no changes written"
  exit 0
fi

# 4. Apply version bump
tmpfile=$(mktemp)
sed "s/\"version\": \"$current\"/\"version\": \"$new_version\"/" "$PLUGIN_JSON" > "$tmpfile"
mv "$tmpfile" "$PLUGIN_JSON"

# 5. Commit + tag
git add "$PLUGIN_JSON"
git commit -m "release: v${new_version}"
git tag "v${new_version}"

echo "[release] committed and tagged v${new_version}"
echo "[release] run: git push origin main --follow-tags"
