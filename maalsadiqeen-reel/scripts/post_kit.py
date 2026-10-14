#!/usr/bin/env python3
"""
post_kit.py — generate post.md (caption, hashtags, pinned rijal comment, alt hooks, publish checklist).

    python3 post_kit.py content.json [--hooks hooks.json] [-o post.md]

Caption strategy (2026 ranking signals): keyword-rich first line (search), the full hadith text
(saves), the sanad verdict (trust → shares), a soft share prompt, ≤ 8 niche hashtags.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import load_json, strip_tashkeel

BASE_TAGS = ["#أهل_البيت", "#حديث_شريف", "#الإمام_الرضا", "#الإمام_الصادق", "#الإمام_الباقر", "#شيعة", "#تحقيق_السند", "#رجال_الحديث", "#معارف_أهل_البيت", "#علم_الحديث"]


def pick_tags(c):
    # detect the Imam from the hadith/hook/bayan only (not from narrators' names in the chain)
    parts = [c.get("title", ""), json.dumps(c.get("hook", {}), ensure_ascii=False), json.dumps(c.get("hadith", {}), ensure_ascii=False),
             json.dumps(c.get("bayan", {}), ensure_ascii=False), " ".join(p.get("title", "") for p in c.get("points") or [])]
    text = " ".join(parts)
    tags = ["#أهل_البيت", "#حديث_شريف", "#تحقيق_السند"]
    for imam, tag in (("الرضا", "#الإمام_الرضا"), ("الصادق", "#الإمام_الصادق"), ("الباقر", "#الإمام_الباقر"), ("الكاظم", "#الإمام_الكاظم"), ("أمير المؤمنين", "#أمير_المؤمنين"), ("الحسين", "#الإمام_الحسين"), ("فاطمة", "#فاطمة_الزهراء")):
        if imam in text and tag not in tags:
            tags.append(tag)
    for kw, tag in (("شيعت", "#شيعة"), ("ولاي", "#الولاية"), ("سند", "#رجال_الحديث")):
        if kw in text and tag not in tags:
            tags.append(tag)
    tags += [t for t in ("#معارف_أهل_البيت", "#علم_الحديث") if t not in tags]
    return tags[:8]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("content")
    ap.add_argument("--hooks", help="ranked hooks JSON from hook_score_ar.py --out")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    c = load_json(a.content)
    hook = c["hook"]
    hook_line = (hook.get("line1", "") + " " + (hook.get("line2") or "")).strip()
    hadith = c["hadith"]
    hadith_text = " ".join(l["t"] for l in hadith["lines"])
    intro = hadith.get("intro", "")
    sanad = c.get("sanad") or {}
    chain = sanad.get("chain") or []
    sources = c.get("sources") or []
    title = c.get("title") or strip_tashkeel(hadith["lines"][0]["t"])
    tags = pick_tags(c)

    chain_md = " ← ".join(f"{n['name']}" + (f" ({n['grade']})" if n.get("grade") else "") for n in chain)
    pinned = []
    if chain:
        pinned.append(f"سلسلة السند: {chain_md}.")
        if sanad.get("verdict"):
            pinned.append(f"النتيجة: {sanad['verdict']}" + (f" — {sanad['verdict_sub']}" if sanad.get("verdict_sub") else "") + ".")
        if sanad.get("note"):
            pinned.append(sanad["note"] + ".")
    if sources:
        pinned.append("المصادر: " + "؛ ".join(sources) + ".")

    caption = [hook_line, "", (intro + " " if intro else "") + hadith_text, ""]
    for p in c.get("points") or []:
        caption.append(f"• {p['title']}" + (f": {' '.join(p.get('desc') or [])}" if p.get("desc") else ""))
    if c.get("points"):
        caption.append("")
    if c.get("bayan"):
        caption += [" ".join(c["bayan"]["lines"]), ""]
    if sanad.get("verdict"):
        caption += [f"✦ {sanad['verdict']}" + (f" — {sanad['verdict_sub']}" if sanad.get("verdict_sub") else ""), ""]
    if sources:
        caption += ["المصادر: " + "؛ ".join(sources), ""]
    cta = c.get("cta") or {}
    if cta.get("line1"):
        caption += [cta["line1"] + (" " + cta["line2"] if cta.get("line2") else ""), ""]
    caption.append(" ".join(tags))

    alt_hooks = ""
    if a.hooks and Path(a.hooks).exists():
        ranked = load_json(a.hooks)
        alt_hooks = "\n".join(f"{i+1}. [{r['score']}] {r['hook']}" for i, r in enumerate(ranked[:5]))

    md = f"""# {title} — Post kit

## Caption (copy as-is)

```
{chr(10).join(caption)}
```

## Pinned comment (rijal detail — pin it immediately after posting)

```
{chr(10).join(pinned) if pinned else "—"}
```

## Alternative hooks (A/B for the cover text or a re-cut)

{alt_hooks or "run: python3 scripts/hook_score_ar.py \"...\" \"...\" --out hooks.json"}

## Publish checklist

- [ ] Cover = hook frame (cover.jpg); the title text is inside the 4:5 centre crop
- [ ] Caption first line = the hook (keywords: Imam's name + topic) — Instagram search indexes it
- [ ] Add on-screen topics (الموضوعات) in the Reel settings: أهل البيت / حديث / سند
- [ ] Pin the rijal comment within the first minute; reply to the first 10 comments (replies count as engagement)
- [ ] Share to Story with the «أرسِل» sticker prompt; sends-per-reach is the strongest non-follower signal (2026)
- [ ] No reposted footage / watermarks; the video is original (originality boosts distribution since 2026-04-30)
- [ ] Post when the Arabic-speaking audience is awake: 19:00–22:00 Baghdad/Riyadh time; Thursday–Friday nights perform best for religious content
- [ ] Watch retention after 24 h: if the drop is at the hadith scene → shorten pace (plan.py --target 40); if at points → merge points into bayan

## Hashtags

{" ".join(tags)}
"""
    out = a.out or str(Path(a.content).with_name("post.md"))
    Path(out).write_text(md, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
