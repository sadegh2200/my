---
name: maalsadiqeen-reel
description: Use when the user asks for a reel/video/ریل/ویدیو for the Instagram page «مع الصادقين» (maalsadiqeen, @maalsadiqeen), or shares branded Arabic "sheets"/ورق/پست/پوستر (cream paper, green arc, tree logo) with a verse, ḥadīth, scholar quote, question or occasion and wants them turned into a 30–60 s vertical video — including re-cuts, A/B hooks, 4:5 feed variants, covers, beat sheets, captions or "same style as the Ṣādiqīn reel". Also use when any Arabic religious short-form video is requested in this page's style, even without an āyah on the sheets.
license: Proprietary — made for the maalsadiqeen page; third-party assets per assets/sfx/CREDITS.md and font licences (OFL).
metadata:
  version: 1.0.0
  brand: maalsadiqeen
  output: 1080x1920 MP4 (30 fps, ≤60 s) + cover + beat sheet
  requires: node>=22, hyperframes 0.8.x, ffmpeg, python3 (numpy, pillow)
---

# maalsadiqeen-reel — from the page's sheets to a finished reel

Turn one or more branded sheets of «مع الصادقين» into a dignified, text-led, viral-ready vertical
video: you read the sheets, decide the story, write فصيح Arabic copy, compile a HyperFrames project
from a JSON spec, build the soundtrack (recitation + sound design, no narrator), verify with
snapshots, render, and hand over master + cover + beat sheet with a Persian summary. Everything the
five generic skills (video, motion-design, hyperframes, remotion-best-practices, instagram-viral) did
for this page is encoded here as scripts and references — do not re-derive it.

## Non-negotiables

1. **No human or synthetic narrator** unless the user asks for one in this conversation. Qurʾan
   recitation is welcome when the reel contains an āyah. The reel must make full sense muted.
2. **≤ 60 s, 9:16 1080×1920, 30 fps**; default length 45 s (36–50 s window).
3. **Brand = paper, green, gold** (`references/brand.md`). No new colours, fonts, or effects.
4. **Copy is فصيح, متين, fully vocalised** where sacred/quoted (`references/arabic-copy.md`). Never
   alter or "repair" a verse/ḥadīth from memory; quote the sheet, flag unreadable spots to the user.
5. **No invented references or gradings.** No source on the sheet → no proof block (say so).
6. **verify.py must pass before `render`.** Look at `qc/sheet.jpg` with your own eyes every time.
7. Reply to the user in Persian; on-screen copy in Arabic (Persian only if explicitly requested).

## Workflow

### 0 · Toolchain (every session — the sandbox forgets)

```bash
SK=/home/user/skills/maalsadiqeen-reel      # wherever this skill is installed
source $SK/scripts/env.sh                   # prints missing pieces + exact install commands
```
Fix whatever it reports (`references/troubleshooting.md`). Never run two renders or checks at once.

### 1 · Read the sheets → brief (`references/content-analysis.md`)

Open every attached image (`read_file`). Transcribe sacred text, references, scholar comments, the
page's framing. Classify (A verse+ḥadīth+grading · B ḥadīth only · C scholar/concept · D FAQ ·
E occasion · F objection) and write the one-sentence idea, hinge word, surprise, authority,
take-away. Save it as `work/<slug>/brief.md`. If the sheets hold two ideas, propose two reels.

When research adds value (hook benchmarks, verifying a reference, a recitation choice), do it now,
briefly; cite sources in the brief. Do not scrape Instagram.

### 2 · Scenario = spec (`references/narrative.md`, `references/blocks.md`)

```bash
S=$SK/scripts; W=/home/user/work/<slug>; mkdir -p $W
python3 $S/new_spec.py --archetype A --duration 45 --out $W/spec.json [--recitation 9:119]
```
Replace every «…» with the final copy. Rules of thumb: hook word on screen by 1.2 s; one `<em>`
hinge word per line at most; ≤ 70 words on screen in total; one hero line; CTA ≥ 6.4 s with
«أَرْسِلْهَا لِمَنْ تُحِبّ» and the brand card. Keep explicit `cues` only where the audio dictates
them (verse words); otherwise let the builder pace by reading speed.

With a verse: fetch the recitation first and size the verse scene from it.
```bash
python3 $S/recite.py 9:119 --out $W/recite.wav            # prints duration → verse scene ≥ duration + 1.6 s
python3 $S/cues.py $W/recite.wav --words 8 --offset <verse scene start> --json   # → scenes[verse].cues.words
```

### 3 · Build

```bash
python3 $S/build_reel.py $W/spec.json --out $W/project    # → index.html + spec.resolved.json; read every WARN
```
Fix WARNs by editing the spec (never the generated HTML, except as a last resort for one-offs).

### 4 · Soundtrack (`references/audio.md`)

```bash
cp $W/recite.wav $W/project/assets/audio/recite.wav 2>/dev/null; python3 $S/mix.py $W/project --dry-run   # review events
python3 $S/mix.py $W/project                               # bed + recitation + auto SFX → assets/audio/mix.wav, prints LUFS
```
Narration only on explicit request: produce stems, `tighten.py`, add to `audio.stems`, `mode: narrated`.

### 5 · Verify (pre-render gate, `references/qc.md`)

```bash
python3 $S/verify.py $W/project                            # pacing · html · hyperframes check · snapshots → qc/sheet.jpg
```
`read_file $W/project/qc/sheet.jpg`. Check typography, clipping, gold emphasis, seal, watermark,
brand card. Iterate spec → build → mix → verify until 0 failures and the frames look right. If the
cover frame (hero + 0.9 s) would not stop a scroll, rewrite the hero/hook — now, not after rendering.

### 6 · Render (3.5–6 min)

```bash
bash $S/render.sh $W/project /home/user/deliver/<slug>.mp4          # use start_process; one render at a time
python3 $S/verify.py $W/project --render /home/user/deliver/<slug>.mp4 --no-check
```
Grab 4–6 frames from the MP4 with ffmpeg and compare to the snapshots (a blank render = `dir=rtl` on
`<html>` or missing fonts).

### 7 · Deliverables (`references/publish.md`)

```bash
python3 $S/export_variants.py /home/user/deliver/<slug>.mp4 --out /home/user/deliver --name <slug> --spec $W/project/spec.resolved.json [--feed] [--audio]
python3 $S/beat_sheet.py $W/project --spec $W/spec.json --out /home/user/deliver/<slug>-beat-sheet.md --lang fa
```
Write the caption (3–5 lines + ≤ 5 hashtags, reference in line 1–2) into the beat sheet or
`<slug>-caption.txt`. `present_file` the MP4. In the Persian summary give: idea + archetype, the
scene table (time, copy, source), audio plan, what was verified (check/snapshots/LUFS/duration),
posting advice (cover, caption, A/B or Trial Reels, metrics to watch), and any flagged uncertainty
(unreadable word, missing reference).

## Decision points

| situation | do |
|---|---|
| sheets contain an āyah | archetype A (or E); recitation `ar.mahermuaiqly`; verse words cued from `cues.py` |
| no āyah, a ḥadīth with reference | B; `quote` with `reveal: words`; proof cards without seal unless a grading is stated |
| only a scholar's point / concept | C; contrast block carries the turn; hero = the text that settles it |
| question-type sheet | D; answer as `list` (≤ 3) or `quote`; keep the answer scene ≥ 8 s |
| date / person / occasion | E; `title` card first; no contrast; final = greeting line |
| objection / شبهة | F; calm tone, quote the objection neutrally, never name opponents |
| user asks for narration | narrated mode: stems + `tighten.py` + `cues.py --lines`; target −14 LUFS; Persian runs 20 % longer |
| user asks for a variant | A/B: change scene 1 only; feed: `export_variants.py --feed`; Persian version: translate copy, shrink sizes/`nowrap` |
| user wants > 60 s | refuse politely; propose a two-part series with the same opening signature |
| toolchain missing / render impossible | still deliver spec + beat sheet + snapshots if check runs; otherwise brief + spec and the exact commands |

## Files

| path | purpose |
|---|---|
| `scripts/env.sh` | env vars + toolchain check (source it first) |
| `scripts/new_spec.py` | archetype scaffolds A–F |
| `scripts/build_reel.py` | spec → HyperFrames project; block library (hook, verse, contrast, answer, proof, cta, quote, list, title); exact Arabic font fitting; reading-speed cues |
| `scripts/recite.py`, `scripts/cues.py` | recitation download/trim; word/line onset detection |
| `scripts/mix.py`, `scripts/gen_bed.py`, `scripts/tighten.py` | soundtrack: bed, recitation, auto sound design, ducking, mastering; narration tightening |
| `scripts/verify.py`, `scripts/render.sh` | QC gates (pre/post render); check+render wrapper |
| `scripts/export_variants.py`, `scripts/beat_sheet.py` | cover, 4:5, 1:1, audio stem; Persian/Arabic/English beat sheet |
| `references/brand.md` | tokens, typography, grid, motion personality, tone |
| `references/content-analysis.md` | reading the sheets, classification, brief template |
| `references/narrative.md` | archetypes A–F with timings; hook formulas allowed/rejected |
| `references/arabic-copy.md` | register, quoting, tashkeel checklist, line budgets, caption skeleton |
| `references/blocks.md` | spec format, every block's fields and cues, timing recipes, extending |
| `references/audio.md`, `references/motion.md` | pipeline details; HyperFrames/GSAP rules and choreography |
| `references/qc.md`, `references/publish.md`, `references/troubleshooting.md` | gates & defects; posting playbook; sandbox fixes |
| `assets/examples/sadiqeen-9-119.silent.json` | the delivered 45 s reel (archetype A) — the gold standard |
| `assets/examples/hadith-only.json` | archetype B/C example without a verse (40 s) |
| `assets/{fonts,brand,sfx,gsap.min.js,hyperframes.json}` | everything the builder copies into a project |
| `evals/evals.json`, `evals/rubric.md`, `evals/files/sheet-*.jpg` | test prompts with the real sheets |
| `README-fa.md` | Persian guide for the page owner |

## Done means

- `deliver/<slug>.mp4` passes `verify.py --render` (1080×1920, ≤ 60 s, AAC, LUFS within ±1.2 of target).
- `deliver/<slug>-cover.jpg`, `deliver/<slug>-beat-sheet.md` (+ caption) exist.
- Snapshots were inspected; every quoted text matches the sheets; every reference comes from the sheets.
- The Persian summary states what was built, what was verified, and what the user should check.
