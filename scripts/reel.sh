#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source scripts/env.sh
S="$ROOT/maalsadiqeen-reel/scripts"
SOURCE="$ROOT/projects/ashab-51"
PROJECT="$ROOT/work/ashab-51/project"
DELIVER="$ROOT/deliver/ashab-51"
MASTER="$DELIVER/maalsadiqeen-51.mp4"
SNAPS="1.2,10.4,18.9,29.9,41.3,49.7"

build() {
  python3 scripts/validate_reel.py
  python3 maalsadiqeen-1/scripts/validate_content.py "$SOURCE/content.json" --strict
  python3 "$S/build_reel.py" "$SOURCE/spec.json" --out "$PROJECT"
  python3 "$S/mix.py" "$PROJECT"
}
check() {
  python3 scripts/validate_reel.py
  python3 "$S/verify.py" "$PROJECT" --snaps "$SNAPS"
}
finalize() {
  python3 "$S/verify.py" "$PROJECT" --render "$MASTER" --no-check
  python3 "$S/export_variants.py" "$MASTER" --out "$DELIVER" --name maalsadiqeen-51 --cover 2.6
  python3 "$S/beat_sheet.py" "$PROJECT" --spec "$SOURCE/spec.json" --lang fa --out "$DELIVER/beat-sheet-fa.md"
}
case "${1:-build}" in
  build) build ;;
  check) check ;;
  render)
    check
    printf '\nInspect work/ashab-51/project/qc/sheet.jpg before publishing.\n'
    bash "$S/render.sh" "$PROJECT" "$MASTER"
    finalize ;;
  finalize) finalize ;;
  all) build; check; bash "$S/render.sh" "$PROJECT" "$MASTER"; finalize ;;
  *) echo 'Usage: bash scripts/reel.sh {build|check|render|finalize|all}' >&2; exit 2 ;;
esac
