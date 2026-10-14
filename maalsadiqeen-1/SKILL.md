---
name: maalsadiqeen-1
description: Turn a scholarly Shia carousel post (hadith + rijal/sanad verification + explanation + sources, 3–6 cards in any layout) into a dignified, formal-Arabic, faceless 30–60 s Instagram Reel (text + music, no voice) in the maalsadiqeen house style — kinetic typography, animated sanad chain with ثقة stamps and a verdict seal, share-oriented CTA. Use when the user uploads hadith cards/images or asks for a Reel, ريلز, فيديو, or انيميشن for a hadith post. Covers intake (vision → content.json), hook writing/scoring in Arabic, timing/pagination planning, brand extraction, royalty-free audio, Remotion rendering, QA, and the caption/pinned-comment kit.
license: MIT
metadata:
  author: maalsadiqeen / Arena.ai agent
  version: 1.0.0
  upstream: ig-reel (hooks, scoring) · short-editing (safe zones, loudness, post copy) · video-editing (ffmpeg QA, "edit, don't generate") · remotion-best-practices (composition rules)
---

# maalsadiqeen-1 — carousel / Remotion

Produce a Reel that is **با وقار** (dignified), beautiful, viral and faithful to the source: every on-screen
word is formal Arabic (فصحى) copied from the user's cards, nothing is invented, the sanad is shown as
the proof, and the viewer is asked to *send* it to someone — the strongest 2026 reach signal.

The pipeline is **data-driven**: you never edit React. You write `content.json` (what), run `plan.py`
to get `plan.json` (when / how big), and render the fixed Remotion template. Iterate only through JSON.

```
cards (images)  ──vision──▶  content.json  ──validate──▶  hooks (3, scored ≥ 65)
      ──plan.py──▶  plan.json  ──extract_brand / make_audio──▶  render.py  ──QA──▶  post_kit.py
```

## 0. Preflight (once per machine)

```bash
SKILL=/home/user/skills/maalsadiqeen-1
python3 $SKILL/scripts/setup_studio.py --dest ~/reel-studio            # template + npm install + Chrome + audio + tsc
# existing Remotion project on this box?  add: --link-node-modules /home/user/reel-maalsadiqeen/node_modules
pip install -q imageio-ffmpeg                                             # loudness/duration probe (optional, not persisted)
```

Memory on this sandbox is ≈1 GB: render with `--concurrency 1`, never run Studio and a render together.
A 45 s render takes ≈3 min — start it with `start_process`, keep working, then `get_process_output … wait_for exit`.

## 1. Intake — read the cards with vision

Look at **every** card image (`read_file`) and classify each one; the number and background of the
cards vary (3, 4, 5…), so detect roles by content, not by position:

| Card looks like | Role | content.json |
|---|---|---|
| Vocalized hadith under an arc ornament, «قال الإمام …», a one-line thesis below | **hadith** (+ `hook` material, `hadith.bridge`) | `hadith.intro`, `hadith.lines[]`, `hadith.bridge` |
| Numbered traits / conditions / meanings, each with 1–2 sentences | **points** (2–5) | `points[]` |
| A single supporting narration, tafsir or scholar's explanation | **bayan** | `bayan` |
| Narrator names with ثقة/ضعيف/إمامي… or «السند صحيح/معتبر» | **sanad** | `sanad.chain[]`, `sanad.verdict` |
| «المصادر»: book, volume, page | **sources** | `sources[]` (keep ≤ 4, Arabic digits) |
| Logo / handle / ornament corners | **brand** | `brand.handle`, `extract_brand.py` |

Rules of transcription (read `references/content-extraction.md` before the first job):
- Copy the hadith **letter-for-letter with its tashkeel**; split at the natural pauses into lines of ≤ 6 words
  (≤ 42 letters). Mark the first clause `style:"lead"`, the consequence («فليس منّا», «فمِيتتُهُ…») `style:"warning"`.
- Points: `title` = the exact words of the hadith for that trait; `desc` ≤ 2 short lines **in the card's own wording**
  — never add doctrine the card does not contain. If the card quotes another narration, put it in `quote`.
- Sanad: one node per narrator, in the order printed on the card (author → Imam); copy grades verbatim;
  `imam:true` on the Infallible. `verdict` is mandatory when a chain is shown.
- Anything you cannot read with certainty → ask the user; never guess a name, a grade or a page number.
- Scenes you have no card for are simply omitted (`points`, `bayan`, `sanad` are optional).

Write `~/reel-studio/jobs/<slug>/content.json` using `references/schema.md`; the two files in
`assets/examples/` are complete, working references (4-card and 3-card variants).

## 2. Validate, then write and score three hooks

```bash
python3 $SKILL/scripts/validate_content.py jobs/<slug>/content.json --public ~/reel-studio/public
python3 $SKILL/scripts/hook_score_ar.py "hook A" "hook B" "hook C" --out jobs/<slug>/hooks.json
```

Fix every ERROR (emoji, colloquial, Persian letters, missing verdict, >10 hadith lines). Warnings are
layout advice — honour them unless the card forces otherwise.
Hooks: 3–8 words, a question or a number, second person, stakes, no clickbait. Use the formulas in
`references/hooks-ar.md`; the best one (score ≥ 65, ideally ≥ 80) becomes `hook.line1/line2`, with the
key word in `hook.highlight` and the Imam's name in `hook.sub`. Show the three candidates to the user
in the final message — hooks are the most common thing they want to change.

## 3. Plan timing, pagination and type sizes

```bash
python3 $SKILL/scripts/plan.py jobs/<slug>/content.json --target 46     # 30–60 s hard limits
```

`plan.py` reads Arabic on-screen reading speed (≈2.3 words/s), paginates long hadiths (balanced pages,
«تتمّةُ الحديث» label), shrinks sanad rows for long chains (row = min(112, 800/N)), sizes type to the
longest line, inserts 5-frame crossfades and schedules every SFX cue. Read its summary:
- `pace` < 0.6 → content is too heavy: drop a point into the caption or split into two Reels.
- `pace` = 1.12 with total < 40 s → content is light: add `bayan` (one supporting narration) rather than
  stretching holds.
- Target 42–48 s for hadith + points + sanad; 36–42 s for hadith + bayan + sanad.
Never hand-edit frame numbers unless the user asks for a specific beat; re-run `plan.py` instead.

## 4. Brand and audio

```bash
python3 $SKILL/scripts/extract_brand.py "cards/1.jpg" --out ~/reel-studio/public      # logo.png, branch.png, brand.json
python3 $SKILL/scripts/make_audio.py --out ~/reel-studio/public/audio --plan jobs/<slug>/plan.json --maqam bayati
```

Look at the extracted PNGs (`read_file`) — if the logo crop is wrong, pass `--logo-box br|tl|tr` or
`--no-logo` (the frame falls back to the `@handle` text). Keep `DEFAULT_PALETTE` (paper, green
rgb(10,79,6), maroon for warnings) unless the page's cards clearly use other colours; then paste
`brand.json → palette` into `content.brand.palette`.
The bed is a synthesized, non-rhythmic maqam drone at −20 dB RMS (religious audiences avoid percussive
music). If the user supplies a licensed nasheed/ambient track, save it as `public/audio/pad.wav`
(normalize to ≈ −20 dB RMS) — never download copyrighted audio.

## 5. Render and QA

```bash
python3 $SKILL/scripts/render.py --studio ~/reel-studio --content jobs/<slug>/content.json --stills-only   # 20 s layout check
python3 $SKILL/scripts/render.py --studio ~/reel-studio --content jobs/<slug>/content.json --out ~/reel-output/<slug>
```

Always look at the stills / `contact-sheet.jpg` before declaring done and run through
`references/qa-checklist.md`: no clipped or wrapped-mid-word lines, tashkeel not colliding (large vocalized
text uses Noto Naskh; Amiri only ≤ 90 px), nothing in the top 250 px / bottom 300 px safe zones, seal
readable, −22…−12 LUFS, 30–60 s, cover frame = hook. Fix by editing `content.json` (split a line,
shorten a desc) and re-planning — not by touching the template.

## 6. Post kit and hand-off

```bash
python3 $SKILL/scripts/post_kit.py jobs/<slug>/content.json --hooks jobs/<slug>/hooks.json -o ~/reel-output/<slug>/post.md
```

Deliver: `<slug>.mp4`, `cover.jpg`, `post.md` (caption with keyword-rich first line, pinned rijal
comment, alt hooks, publish checklist). Present the MP4 with `present_file`; summarize in the user's
language (Persian for this user) the structure, the three hooks, and the two or three decisions they
may want to flip (hook, trait wording, colour of the warning line).

## Dignity rules (non-negotiable)

- Formal Arabic only; no emoji, no Latin, no slang, no exclamation stacks, no "لن تصدق".
- Never depict the Prophet or the Imams; no faces, no AI "cinematic" people. Ornament, paper, type only.
- Honorifics stay attached: «عليه السلام», «صلى الله عليه وآله» — never abbreviated on screen.
- Warnings («فليس منّا») are maroon and underlined, not red flashes; stakes are shown, not shouted.
- Sources and the verdict are always on screen; the pinned comment carries the full chain.
- The CTA asks to *send* and *save*; it never begs for follows.

## Why it is viral (built-in, do not strip)

Hook ≤ 1.5 s reading time with an open loop → the hadith reveals word-group by word-group (watch time) →
progress chips make the viewer wait for «٣/٣» → the sanad verification is the share-trigger for a
scholarly audience (credibility = DM shares) → the seal is the emotional peak with a visual "hit" →
the CTA names the recipient («لمن يُحبُّهم») → a fade to the paper lets the loop restart cleanly.
See `references/virality.md` for the ranking-signal mapping and what to measure after posting.

## What each upstream skill contributes (upgraded here)

| Upstream | Taken | Upgraded |
|---|---|---|
| ig-reel | 26 hook formulas, hookscore heuristics, 3-second rule | 12 Arabic scholarly formulas, `hook_score_ar.py` (dignity penalties, tashkeel tip) |
| short-editing | 9:16 safe zones, −14/−16 LUFS targets, caption structure | safe zones baked into the template; −20 dB bed + per-cue SFX gains; Arabic caption + pinned-comment kit |
| video-editing | ffmpeg probe/loudness, "edit don't generate" | `render.py` QA (ebur128, duration gate, contact sheet); brand assets are *extracted* from the real cards, not generated |
| remotion-best-practices | `calculateMetadata`, `staticFile`, `@remotion/media` Audio, Sequence timing, local fonts | data-driven composition (JSON in, duration out), zero-range `interpolate` guards, font loading before render |

## Files

- `assets/template/` — Remotion project (src/scenes/{Hook,Hadith,Points,Bayan,Sanad,CTA}.tsx, ui.tsx, theme.tsx, fonts, SFX)
- `assets/examples/shiatuna/` (4 cards → 5 scenes, 46 s) · `assets/examples/variant-bayan/` (3 cards → bayan, 42 s)
- `scripts/` — setup_studio · validate_content · hook_score_ar · plan · extract_brand · make_audio · render · post_kit
- `references/` — content-extraction · schema · hooks-ar · design-system · virality · qa-checklist
