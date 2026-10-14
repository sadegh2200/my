#!/usr/bin/env python3
"""Project-specific editorial + timing gate, complementary to the skill's QC.

Verifies the selected excerpts against the ingested content, the scope of the
negative verdict and the absence of a misleading affirmative seal. It does not
purport to authenticate religious sources independently.
"""
import argparse
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def plain(text):
    text = re.sub(r"<[^>]*>", "", text)
    return " ".join("".join(c for c in unicodedata.normalize("NFD", text)
                           if unicodedata.category(c) != "Mn").split())


def words_in(value):
    if isinstance(value, str):
        return len(re.findall(r"[\u0621-\u064a\u0660-\u0669]+", plain(value)))
    if isinstance(value, list):
        return sum(words_in(v) for v in value)
    return 0


def validate(spec, content):
    errors = []
    scenes = spec.get("scenes", [])
    duration = spec.get("duration", 0)
    if not 30 <= duration <= 60:
        errors.append("Duration must be 30–60 seconds")
    if not scenes or scenes[0].get("type") != "hook" or scenes[0].get("start") != 0:
        errors.append("Start with a hook at t=0")
    if not scenes:
        return errors
    if scenes[0]["end"] > 4.5:
        errors.append("First cut must be no later than 4.5s")
    if len({s["id"] for s in scenes}) != len(scenes):
        errors.append("Scene IDs must be unique")
    if scenes[-1]["type"] != "cta" or scenes[-1]["end"] != duration:
        errors.append("CTA must end at duration")
    if scenes[-1]["end"] - scenes[-1]["start"] < 6.4:
        errors.append("CTA must last at least 6.4s")
    for prev, sc in zip(scenes, scenes[1:]):
        if prev["end"] != sc["start"]:
            errors.append(f"Non-contiguous scene {sc['id']}")
    for sc in scenes:
        if sc["end"] <= sc["start"]:
            errors.append(f"Invalid duration in {sc['id']}")
        if not sc.get("source_cards") or not set(sc["source_cards"]) <= {1, 2, 3, 4}:
            errors.append(f"Missing source-card provenance in {sc['id']}")
        if sc.get("seal"):
            errors.append("No affirmative seal: the supplied verdict is not صحيح السند")
        if sc["type"] == "quote" and sc.get("reveal") == "words":
            text = " ".join(sc["text"]) if isinstance(sc["text"], list) else sc["text"]
            cues = sc.get("cues", {}).get("words", [])
            if len(cues) != len(text.split()):
                errors.append(f"Quote word/cue mismatch in {sc['id']}")
            if cues != sorted(cues) or any(t < sc["start"] or t > sc["end"] - 1.8 for t in cues):
                errors.append(f"Unsafe word cues in {sc['id']}")
    audio = spec.get("audio", {})
    if audio.get("mode") != "silent" or audio.get("stems") or audio.get("recitation"):
        errors.append("No narrator/recitation was requested or supplied")
    verdict_scene = next((s for s in scenes if s["type"] == "answer"), {})
    verdict = plain(verdict_scene.get("hero", "") + " " + verdict_scene.get("after", ""))
    if verdict != plain(content["sanad"]["verdict"]):
        errors.append("On-screen verdict does not match card 3")
    if plain("الأولى") not in plain(verdict_scene.get("q1", "")):
        errors.append("Verdict must be scoped to the FIRST narration")
    if "بحسب الدراسة المرفقة" != verdict_scene.get("q2"):
        errors.append("Verdict must be explicitly attributed to the supplied study")
    hadith = plain(" ".join(x["t"] for x in content["hadith"]["lines"]))
    quotes = [s for s in scenes if s["type"] == "quote"]
    if len(quotes) != 2:
        errors.append("Expected distinct excerpts from cards 1 and 2")
    else:
        if plain(" ".join(quotes[0]["text"])) not in hadith:
            errors.append("First excerpt differs from ingested narration")
        bayan = plain(" ".join(content["bayan"]["lines"]))
        if plain(" ".join(quotes[1]["text"])) not in bayan:
            errors.append("Second excerpt differs from card 2")
        if "أخرى" not in quotes[1].get("label", "") and plain("أخرى") not in plain(quotes[1].get("label", "")):
            errors.append("Second excerpt must be labelled as another narration")
    concerns = next((s for s in scenes if s["type"] == "proof"), {})
    cards = concerns.get("cards", [])
    if not cards or plain("عند آخرين") not in plain(cards[0].get("grade", "")):
        errors.append("Preserve the disagreement qualifier عند آخرين")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=Path, default=ROOT / "projects/ashab-51")
    a = ap.parse_args()
    spec = json.loads((a.project / "spec.json").read_text())
    content = json.loads((a.project / "content.json").read_text())
    errors = validate(spec, content)
    fields = {"lead", "line1", "line2", "text", "q1", "hero", "after", "share", "final"}
    main_words = sum(words_in(v) for sc in spec["scenes"] for k, v in sc.items() if k in fields)
    print(f"Primary copy: {main_words} words (labels, names and references separate)")
    if main_words > 70:
        errors.append("Primary copy exceeds 70 words")
    for error in errors:
        print("FAIL:", error)
    print(f"Editorial/timing gate: {len(errors)} failures")
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
