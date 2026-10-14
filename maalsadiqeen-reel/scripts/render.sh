#!/usr/bin/env bash
# bash scripts/render.sh <project_dir> <out.mp4>
# Run the gate once and preserve its actual exit status (never grep away failures).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJ="$(cd "$1" && pwd)"
OUT="$(realpath -m "$2")"
source "$HERE/env.sh" >/dev/null
cd "$HF_WORKDIR"
echo "▶ check"
npx hyperframes check "$PROJ"
echo "▶ render (1 worker, 1080×1920, 30 fps; never run two renders at once)"
mkdir -p "$(dirname "$OUT")"
npx hyperframes render "$PROJ" --output "$OUT" --workers 1 --fps 30 --crf 20
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of default=nw=1 "$OUT"
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate -of default=nw=1 "$OUT"
