#!/usr/bin/env bash
# source this before any hyperframes command:   source scripts/env.sh [workdir-with-node_modules]
# It exports the env HyperFrames needs in this sandbox and checks the toolchain. Safe to re-run.
export TMPDIR="${TMPDIR:-$HOME/.cache/tmp}"
export HYPERFRAMES_SKIP_SKILLS=1
export HYPERFRAMES_EXTRACT_CACHE_DIR="${HYPERFRAMES_EXTRACT_CACHE_DIR:-$HOME/.cache/hfx}"
mkdir -p "$TMPDIR" "$HYPERFRAMES_EXTRACT_CACHE_DIR"
[ -x /opt/node22/bin/node ] && export PATH="/opt/node22/bin:$PATH"
export HF_WORKDIR="${1:-${HF_WORKDIR:-$HOME/reel-sadiqeen}}"   # a dir that has node_modules/hyperframes

ok=1
command -v ffmpeg >/dev/null || { echo "✗ ffmpeg missing → sudo apt-get install -y ffmpeg"; ok=0; }
NODE_V=$(node -v 2>/dev/null || echo none)
case "$NODE_V" in v2[2-9]*|v[3-9]*) ;; *) echo "✗ node >=22 missing (have $NODE_V) → curl -fsSL https://nodejs.org/dist/v22.23.3/node-v22.23.3-linux-x64.tar.xz -o /tmp/node.tar.xz && sudo mkdir -p /opt/node22 && sudo tar -xJf /tmp/node.tar.xz -C /opt/node22 --strip-components=1"; ok=0;; esac
if [ ! -d "$HF_WORKDIR/node_modules/hyperframes" ]; then
  echo "✗ hyperframes not installed in $HF_WORKDIR → mkdir -p $HF_WORKDIR && cd $HF_WORKDIR && npm init -y >/dev/null && npm install --no-audit --no-fund hyperframes@0.8.157 playwright@1.64.1"; ok=0
fi
python3 -c "from PIL import features; import sys; sys.exit(0 if features.check('raqm') else 1)" 2>/dev/null || echo "⚠ Pillow+libraqm missing → font fitting falls back to estimates (pip install pillow)"
[ $ok = 1 ] && echo "✓ toolchain ok (node $NODE_V, ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}'), hyperframes in $HF_WORKDIR)"
hf() { (cd "$HF_WORKDIR" && npx hyperframes "$@"); }
export -f hf 2>/dev/null
