# Design system — maalsadiqeen Reel

1080 × 1920, 30 fps. Paper background with radial vignette and 2 % noise; everything is type and
line-work; no photos, no faces, no AI imagery.

## Palette (`DEFAULT_PALETTE` in src/theme.tsx)

| Token | Value | Use |
|---|---|---|
| bgCenter → bgEdge | rgb(252,247,241) → rgb(217,212,206) | paper radial |
| green | rgb(10,79,6) | lead hadith line, titles, seal, chips, icons |
| ink / inkSoft | rgb(41,34,25) / rgb(77,70,60) | body text / secondary |
| olive / oliveSoft | rgb(128,142,116) / rgba(…,0.45) | labels, sources, hairlines |
| maroon | rgb(122,36,33) | warning clause, emphasis in bayan |
| gold / goldSoft | rgb(192,181,160) / rgba(…,0.45) | ornaments, quote rule, imam star |
| chip | rgba(10,79,6,0.08) | chip background |

Overrides come from `content.brand.palette` (any subset of keys).

## Type

| Role | Font | Size (plan key) | Notes |
|---|---|---|---|
| Hook | Amiri Bold | `hook.size` 72–112 | highlight word green + underline draw-on |
| Hadith lead | Noto Naskh Arabic 700 | `hadith.lead` ≤ 128 | Noto keeps tashkeel attached at large sizes (Amiri floats it) |
| Hadith body | Noto Naskh 500 | `hadith.body` 56–78 | line-height 1.75 |
| Warning | Noto Naskh 700 maroon | `hadith.warning` ≤ 66 | 3 px underline draws over 24 frames |
| Point title | Amiri Bold green | `points.title` 72–104 | |
| Point desc | Vazirmatn 400 | `points.desc` 34–44 | |
| Quote box | Noto Naskh 44 | fixed | right border gold 4 px |
| Sanad names | Vazirmatn 500 / Naskh 700 (Imam) | `sanad.name` 30–40 | |
| Chips / stamps | Vazirmatn 600 | 24–30 | |
| CTA line1 | Amiri Bold green | 84–104 | |
| Sources, labels | Vazirmatn 28–34 olive | | |

Rules: ≤ 6 words per hadith line, ≤ 3 lines of desc, never wrap a title mid-phrase (shorten instead),
Arabic-Indic digits everywhere, honorifics spelled out.

## Layout grid (y in px)

- 0–250 safe (IG top UI) · 1620–1920 safe (caption/buttons). Brand frame: logo bottom-left at y≈1760, branch top-right.
- Hook: vertically centred block, 70 px side padding.
- Hadith: arc ornament top 350; text block `page.top` (632 default, lower for short pages); bridge + divider at 1420.
- Points: numeral ring 500–520; title block 660–690; tracker chips 1430.
- Bayan: title at `top − 220`; quote block at `top` (vertically centred by plan).
- Sanad: question 330; chain from 500, row `sanad.row` (112 → 72 for 11 nodes), line at x 790; note 1340.
- CTA: sources 380; headline 700; icons +34 below divider; footer 1400.

## Motion vocabulary

- Reveal: fade + rise 14–30 px + optional scale 1.04–1.07, 16–22 frames, `Easing.bezier(0.16,1,0.3,1)`.
- Scene crossfade: 5-frame overlap, 10–12 frame fade-out, CTA 34 frame fade to paper (clean loop).
- Hook underline draw-on 22→44 f; warning underline 24 f; sanad line grows linearly with the nodes.
- Seal: scale 1.6→1 with overshoot, −7°→−4° rotation, paper flash 0.35→0 over 16 f, chain recedes (blur 3 px, 0.18 opacity).
- Progress chips pop 0.9→1 over 16 f; the last card lights all chips 50 f before the end.
- Nothing moves continuously except the soft icon pulse in the CTA; stillness reads as dignity.

## Sound

- Bed: maqam drone (`make_audio.py`, bayati/hijaz/nahawand/rast), −20 dB RMS, fades 1.5 s / 2.5 s, non-rhythmic.
- Cues (plan.sfx): boom on hook and seal, page-turn on scene changes, tick on reveals (0.55–0.7), stamp on grades/warning (0.5), whoosh on titles (0.3), ding with the seal (0.4).
- Target −16 ± 4 LUFS integrated, true peak ≤ −1 dBFS (render.py reports).
