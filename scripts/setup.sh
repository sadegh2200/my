#!/usr/bin/env bash
# One-time / resumed-sandbox setup. Network: npm and PyPI only.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
node -e 'if (Number(process.versions.node.split(".")[0]) < 22) throw Error("Node 22+ required")'
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
HYPERFRAMES_SKIP_SKILLS=1 PUPPETEER_SKIP_DOWNLOAD=1 npm ci --no-audit --no-fund
node scripts/setup-browser.mjs
.venv/bin/python - <<'PY'
from pathlib import Path
import imageio_ffmpeg, os
root = Path.cwd()
bin_dir = root / '.cache/bin'
bin_dir.mkdir(parents=True, exist_ok=True)
for name, target in [('ffmpeg', imageio_ffmpeg.get_ffmpeg_exe()),
                     ('ffprobe', root / 'node_modules/@ffprobe-installer/linux-x64/ffprobe')]:
    link = bin_dir / name
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        raise SystemExit(f'Refusing to replace non-symlink: {link}')
    link.symlink_to(os.path.relpath(target, bin_dir))
PY
python3 scripts/install_skills.py
source scripts/env.sh
"$HYPERFRAMES_BROWSER_PATH" --version
ffmpeg -version | head -n 1
ffprobe -version | head -n 1
printf '\nReady. Build: npm run reel:build\n'
