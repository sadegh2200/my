# my — مجموعهٔ اسکیل‌ها (Agent Skills)

مخزنِ اسکیل‌های ایجنت (قالب استاندارد `SKILL.md` — قابل استفاده در Claude Code، Codex، Cursor و هر ایجنتی که از
[Agent Skills](https://agentskills.io) پشتیبانی می‌کند). هر پوشهٔ سطح‌بالا یک اسکیل کامل و مستقل است.

## اسکیل‌های اختصاصی (ساخت خودمان)

| پوشه | کار |
|---|---|
| `maalsadiqeen-reel/` | **اسکیل نهایی (v2.0)** — خط تولید کامل ریل برای صفحهٔ «مع الصادقین»: ورق‌های برند → بریف → هوک امتیازدهی‌شده → spec → ساخت (HyperFrames، موتور پیش‌فرض) → تلاوت/طراحی صدا/مسترینگ → گیت QC → رندر → کاور، بیت‌شیت فارسی، پست‌کیت. موتور Remotion به‌عنوان جایگزین داخل همین اسکیل است (`references/remotion-studio.md`). |

> دو اسکیل قبلی (`maalsadiqeen-1` = Remotion و `maalsadiqeen-reel` = HyperFrames) بر اساس ۷ اسکیل مرجع زیر بازبینی و در
> **یک** اسکیل ادغام شدند. گزارش کامل بازبینی، ایرادهای پیداشده و تصمیم‌ها: [`REVIEW-maalsadiqeen-fa.md`](REVIEW-maalsadiqeen-fa.md).

## اسکیل‌های دانلودشده از اینترنت (برترین‌های هر دسته — ۱۴ اکتبر ۲۰۲۶)

معیار انتخاب: تعداد ستارهٔ گیت‌هاب مخزن، تعداد نصب در [skills.sh](https://www.skills.sh) (دایرکتوری رسمی اسکیل‌ها)،
رسمی‌بودن (Anthropic / Remotion / HyperFrames)، عبور از ممیزی امنیتی skills.sh و کیفیت خودِ `SKILL.md`.
هر اسکیل **بدون تغییر** از مخزن اصلی کپی شده؛ فقط فایل `LICENSE` بالادستی کنارش گذاشته شده است.

### ۱) اسکیل‌ساز (۳ اسکیل)

| # | پوشه | منبع | ⭐ مخزن | نصب skills.sh | چه می‌کند |
|---|---|---|---|---|---|
| 1 | `skill-creator/` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — رسمی Anthropic | 181K | 406K | ساخت، ویرایش و **سنجش** اسکیل: نوشتن پیش‌نویس، ساخت تست‌کیس، اجرای eval با/بدون اسکیل، benchmark، بهینه‌سازی خودکار `description` برای trigger بهتر؛ با اسکریپت‌های پایتون و ایجنت‌های grader/comparator/analyzer |
| 2 | `writing-skills/` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/writing-skills) | 299K | 210K | روش TDD برای نوشتن اسکیل: اول سناریوی فشار بدون اسکیل (RED)، بعد نوشتن اسکیل (GREEN)، بعد بستن راه‌های فرار؛ شامل `anthropic-best-practices.md` و راهنمای تست با subagent |
| 3 | `writing-for-agents/` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) | 291K | 417K | اصول نوشتن هر سندی که ایجنت می‌خواند (SKILL.md، AGENTS.md، CLAUDE.md): context pointer، progressive disclosure، سلسله‌مراتب اطلاعات؛ `SKILL-MECHANICS.md` برای frontmatter و router skills |

### ۲) ساخت ویدیو موشن / وایرال اینستاگرام (۲ اسکیل)

| # | پوشه | منبع | ⭐ مخزن | نصب skills.sh | چه می‌کند |
|---|---|---|---|---|---|
| 4 | `motion-graphics/` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes/tree/main/skills/motion-graphics) — رسمی HyperFrames | 64K | 450K | موشن‌گرافیک کوتاهِ طراحی‌محور: کینتیک تایپوگرافی، شمارندهٔ عدد، چارت، لوگو استینگ، لوئر-ثرد و اورلی شبکه‌های اجتماعی، نقشهٔ متحرک، توییت/تیتر متحرک؛ خروجی MP4 یا اورلی شفاف |
| 5 | `remotion-best-practices/` | [remotion-dev/skills](https://github.com/remotion-dev/skills/tree/main/skills/remotion-best-practices) — رسمی Remotion (v4.0.535) | 5K (خود Remotion ده‌ها هزار) | **618K** (پرنصب‌ترین اسکیل ویدیویی) | روتر همهٔ اسکیل‌های Remotion: ساخت پروژه، مارک‌آپ React، انیمیشن، صدا، کپشن، ترنزیشن، نقشه، رندر، Studio؛ ۳۰+ فایل قاعده |

### ۳) ساخت ریلز (۲ اسکیل)

| # | پوشه | منبع | ⭐ مخزن | چه می‌کند |
|---|---|---|---|---|
| 6 | `ig-reel/` | [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill/tree/main/skills/ig-reel) — پرستاره‌ترین پک اسکیل اینستاگرام | 1.3K | از یک ایدهٔ خام تا ریل: ۳ هوک از ۲۶ فرمول (`hooks.json`)، امتیازدهی با `hookscore.py`، اسکریپت گفتاری + متن روی صفحه (safe zone)، بیت‌شیت زمان‌بندی‌شده با `beats.py`؛ الگوی `templates/voice.md` هم ضمیمه است |
| 7 | `viral-instagram-reels/` | [vyralcontent/content-skills](https://github.com/vyralcontent/content-skills/tree/main/skills/viral-instagram-reels) (از تحلیل ۲۰۰هزار ویدیوی وایرال) | 140 | قواعد مخصوص الگوریتم ریلز: sends-per-reach، Trial Reels، Original Content Guidelines، اپ Edits، Reels Insights، تشخیص علت فلاپ‌شدن، کپشن به‌عنوان سیگنال سرچ؛ با چک‌لیست هوک، قالب اسکریپت و فلوی تصمیم Trial Reels |

> نکته: `motion-graphics` یک «نقطهٔ ورود» از خانوادهٔ HyperFrames است و در عمل به اسکیل‌های پایهٔ همان خانواده
> (`hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-cli`, `media-use`) تکیه می‌کند.
> اولین بار که استفاده می‌کنید `npx hyperframes skills update motion-graphics` (یا `npx skills add heygen-com/hyperframes`)
> را بزنید تا وابستگی‌هایش هم نصب شود.

## نحوهٔ استفاده

```bash
# Claude Code (پروژه‌ای)
mkdir -p .claude/skills && cp -r skill-creator writing-skills writing-for-agents motion-graphics remotion-best-practices ig-reel viral-instagram-reels .claude/skills/

# Codex / Copilot / Gemini CLI و بقیه (مسیر مشترک)
mkdir -p ~/.agents/skills && cp -r <skill-folder> ~/.agents/skills/

# یا نصب مستقیم آخرین نسخه از منبع اصلی
npx skills add anthropics/skills --skill skill-creator
npx skills add obra/superpowers --skill writing-skills
npx skills add mattpocock/skills --skill writing-for-agents
npx skills add heygen-com/hyperframes --skill motion-graphics
npx skills add remotion-dev/skills --skill remotion-best-practices
npx skills add jakeschincariol/instagram-agent-skill --skill ig-reel
npx skills add vyralcontent/content-skills --skill viral-instagram-reels
```

## منبع و نسخهٔ دقیق هر اسکیل (provenance)

| پوشه | مخزن بالادستی | commit | تاریخ commit | مجوز |
|---|---|---|---|---|
| `skill-creator/` | anthropics/skills · `skills/skill-creator` | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | 2026-10-09 | Apache-2.0 (`LICENSE.txt` داخل پوشه) |
| `writing-skills/` | obra/superpowers · `skills/writing-skills` | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | 2026-10-09 | MIT |
| `writing-for-agents/` | mattpocock/skills · `skills/productivity/writing-for-agents` | `49dd158d1076134a641b33efb035946536778336` | 2026-10-09 | MIT |
| `motion-graphics/` | heygen-com/hyperframes · `skills/motion-graphics` | `d65eefad5ed351e9d36d2caeb6049878be0aba85` | 2026-10-14 | Apache-2.0 |
| `remotion-best-practices/` | remotion-dev/skills · `skills/remotion-best-practices` (آینهٔ `packages/skills` در مونوریپوی Remotion) | `7ba4dcf8ebe1626b00baa41e1f2478113719b60b` | 2026-10-12 | [Remotion License](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) — رایگان برای افراد و شرکت‌های تا ۳ نفر |
| `ig-reel/` | Jakeschincariol/instagram-agent-skill · `skills/ig-reel` (+ `templates/voice.md`) | `d03c56bb598be770c60b201f94237e5d1a4268a6` | 2026-09-13 | MIT |
| `viral-instagram-reels/` | vyralcontent/content-skills · `skills/viral-instagram-reels` | `349e495d97029a3e6303a7510e3f39c73f36d8fe` | 2026-06-22 | MIT |

ستاره‌ها و تعداد نصب‌ها در تاریخ ۲۰۲۶-۱۰-۱۴ از GitHub API و skills.sh خوانده شده‌اند. اعتبارسنجی: هر ۷ اسکیل با
`skill-creator/scripts/quick_validate.py` چک شده‌اند (همه معتبر؛ `remotion-best-practices` فقط یک کلید اضافهٔ `version`
در frontmatter دارد که انتخاب خود Remotion است و مشکلی ایجاد نمی‌کند).

---

## English summary

Collection of Agent Skills (`SKILL.md` standard). One in-house skill (`maalsadiqeen-reel` v2.0 — the merged, reviewed
final of the former `maalsadiqeen-1` + `maalsadiqeen-reel`; review report in `REVIEW-maalsadiqeen-fa.md`) plus seven
top-ranked skills vendored verbatim from their upstream repos on 2026-10-14 (ranked by GitHub stars, skills.sh installs,
official status and security audits):

- **Skill creators:** `skill-creator` (Anthropic, 181K★ / 406K installs), `writing-skills` (obra/superpowers, 299K★ / 210K),
  `writing-for-agents` (mattpocock/skills, 291K★ / 417K).
- **Motion video / viral Instagram:** `motion-graphics` (HyperFrames, 64K★ / 450K), `remotion-best-practices`
  (Remotion official, 618K installs — the most-installed video skill).
- **Reels:** `ig-reel` (instagram-agent-skill, 1.3K★ — 26 scored hook formulas + beat sheet tools),
  `viral-instagram-reels` (Vyral — Reels-algorithm playbook: sends per reach, Trial Reels, originality rules).

See the provenance table above for exact upstream commits and licenses.
