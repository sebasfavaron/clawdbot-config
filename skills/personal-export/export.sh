#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/sebas/clawd"
OUT_DIR="${1:-$ROOT/exports}"
TS=$(date +"%Y%m%d-%H%M%S")
ZIP_NAME="clawdbot-personal-export-${TS}.zip"
TMP_LIST=$(mktemp)

mkdir -p "$OUT_DIR"

# Build file list (only existing files/dirs)
add_if_exists() {
  local path="$1"
  if [ -e "$path" ]; then
    echo "$path" >> "$TMP_LIST"
  fi
}

add_if_exists "$ROOT/MEMORY.md"
add_if_exists "$ROOT/memory"
add_if_exists "$ROOT/USER.md"
add_if_exists "$ROOT/IDENTITY.md"
add_if_exists "$ROOT/NEXT_STEPS.md"
add_if_exists "$ROOT/HEARTBEAT.md"
add_if_exists "$ROOT/TOOLS.md"

if [ ! -s "$TMP_LIST" ]; then
  echo "No files found to export."
  rm -f "$TMP_LIST"
  exit 1
fi

# Create ZIP
( cd "$ROOT" && zip -r "$OUT_DIR/$ZIP_NAME" $(sed "s|$ROOT/||" "$TMP_LIST") )

rm -f "$TMP_LIST"

echo "✅ Export created: $OUT_DIR/$ZIP_NAME"
