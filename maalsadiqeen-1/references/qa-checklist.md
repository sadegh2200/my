# QA checklist — run before delivering

Use `render.py --stills-only` first (≈20 s), then the full render and `contact-sheet.jpg`. Look at every
image with `read_file`; do not trust the numbers alone.

## Text

- [ ] Every hadith word matches the card (compare side by side; tashkeel included).
- [ ] No line wraps mid-phrase; no clipped glyph at the 940 px column edge; no orphan single word.
- [ ] Tashkeel sits on the letters (Noto Naskh for large text); no marks colliding with the line above.
- [ ] Highlight word in the hook is the intended one and the underline reaches it.
- [ ] Honorifics complete; Arabic-Indic digits in sources; no Latin, emoji, dialect.
- [ ] Warning line maroon + underline; bridge visible and not overlapping the hadith block.
- [ ] Continuation pages show «تتمّةُ الحديث», not the intro again.

## Layout and brand

- [ ] Nothing important inside the top 250 px or bottom 300 px (IG UI zones); logo bottom-left, branch top-right, or @handle fallback.
- [ ] Hook frame works as the cover in the 4:5 centre crop (cover.jpg).
- [ ] Points: numeral ring, chips count = points count, last card lights all chips.
- [ ] Sanad: names readable at the chosen row size, Imam node is the star, seal text ≤ 2 lines, note not overlapping the seal.
- [ ] CTA: sources ≤ 2 lines, send/save icons, fade to paper at the end.

## Timing and sound (qa.json)

- [ ] 30 ≤ duration ≤ 60 s (target 42–48); `pace` between 0.6 and 1.12.
- [ ] Each hadith line holds ≥ 1.3 s; each point card 3.6–7.5 s; seal hold ≥ 3 s.
- [ ] Integrated loudness −22…−12 LUFS, true peak ≤ −1 dBFS; bed audible but under the SFX.
- [ ] SFX land on the reveals (boom at frame 0 and at the seal; stamps with the ثقة chips).

## Files

- [ ] `<slug>.mp4` (H.264, yuv420p, AAC, 1080×1920), `cover.jpg`, `post.md`, `contact-sheet.jpg`, `qa.json`.
- [ ] `content.json` + `plan.json` kept in `jobs/<slug>/` for re-cuts.

## Fixing rules

Edit `content.json` (split lines, shorten desc, drop a point) → `plan.py` → re-render. Change frame
numbers in `plan.json` only for a user-requested beat. Touch the template only for a genuine bug, and
then re-run both examples in `assets/examples/`.
