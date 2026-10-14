#!/usr/bin/env bash
# Source before invoking the bundled skill scripts.
REEL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$REEL_ROOT/.venv/bin:$REEL_ROOT/.cache/bin:$PATH"
export HF_WORKDIR="$REEL_ROOT"
export HYPERFRAMES_SKIP_SKILLS=1
export HYPERFRAMES_TELEMETRY_DISABLED=1
export DO_NOT_TRACK=1
export HYPERFRAMES_BROWSER_PATH="$REEL_ROOT/.cache/browser/chromium"
export HYPERFRAMES_EXTRACT_CACHE_DIR="$REEL_ROOT/.cache/hfx"
export TMPDIR="$REEL_ROOT/.cache/tmp"
export FONTCONFIG_PATH="$REEL_ROOT/.cache/browser/fonts"
export LD_LIBRARY_PATH="$REEL_ROOT/.cache/browser/lib:$REEL_ROOT/.cache/browser${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
mkdir -p "$TMPDIR" "$HYPERFRAMES_EXTRACT_CACHE_DIR"
