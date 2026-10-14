# Examples

| folder | cards | scenes | length | notes |
|---|---|---|---|---|
| `shiatuna/` | 4 (hadith · traits · sanad · sources) | hook · hadith · points(3) · sanad(7) · cta | 46 s | reproduces the delivered Reel «شيعتنا المسلمون لأمرنا» |
| `variant-bayan/` | 3 (hadith · explanation · sanad) | hook · hadith · bayan · sanad(4) · cta | 42 s | **layout fixture** — verify the narration text, chain and pages against the sources before publishing |

Regenerate a plan: `python3 ../../scripts/plan.py shiatuna/content.json`.
Render: `python3 ../../scripts/render.py --studio ~/reel-studio --content shiatuna/content.json`.
