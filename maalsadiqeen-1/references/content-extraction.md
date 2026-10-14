# Content extraction — from carousel cards to content.json

## 1. Look before you type

Open every card with `read_file`. For each card note: (a) its role (hadith / points / bayan / sanad /
sources / cover-only), (b) the exact text, (c) colours and ornaments (arc, star, divider, leaf, logo corner).
Cards from this page usually follow one of these layouts:

| Layout | Typical cards | Scenes produced |
|---|---|---|
| A — 4 cards | hadith · traits (numbered) · sanad table · sources/closing | hook · hadith · points · sanad · cta |
| B — 3 cards | hadith · explanation (one narration / tafsir) · sanad+sources | hook · hadith · bayan · sanad · cta |
| C — 2 cards | hadith with thesis · sanad+sources | hook · hadith · sanad · cta (add `bayan` from the thesis if < 36 s) |
| D — 5–6 cards | hadith · 3–4 traits · supporting narration · sanad · sources | hook · hadith · points(≤4) · bayan · sanad · cta — expect `pace` warnings; move 1 point to the caption |

The **sanad card** is sometimes merged with the hadith card as a footnote («السند يعتبر صحيحاً ومعتبراً»)
and the chain itself is in the caption of the post — ask the user for the chain if it is not on any card.

## 2. Transcription rules

1. **Hadith** — exact wording with full tashkeel. Read it twice. Break into lines at the natural
   syntactic pauses (after «،» «؛» or at clause boundaries), ≤ 6 words / ≤ 42 letters per line. Up to 10
   lines; longer hadiths become two Reels (part ١/٢).
   - First clause → `style:"lead"` (large green).
   - Consequence / threat / exclusion → `style:"warning"` (maroon with an underline).
   - `intro` = the isnād-free attribution as printed («قالَ الإمامُ الرضا عليه السلام:»). If the card says
     «روى عن أبي الحسن الرضا عليه السلام قال», normalize to «عن أبي الحسنِ الرضا عليه السلام قال:» — keep the kunya the card uses.
2. **Bridge** — the card's thesis line («ثلاثُ صفاتٍ لِصدقِ الولاء») shortened to ≤ 5 words. If the card
   has none, omit it.
3. **Points** — only when the card enumerates. `title` = the hadith's own phrase for the trait;
   `chip` = its one-word root (التسليم / الأخذ / المخالفة). `desc` = the card's gloss, ≤ 2 lines of ≤ 48
   letters; if the card has a longer paragraph, keep its first sentence and the operative clause.
   Supporting narrations on the card go to `quote.lines` (split at the «،») with `quote.src`.
4. **Bayan** — one narration/tafsir block: ≤ 6 lines, the decisive line in `emphasis`.
5. **Sanad** — exactly as printed, top to bottom. Common grades: ثقة · ثقة جليل · إمامي ثقة · ممدوح ·
   حسن · مجهول · ضعيف · من مشايخ الإجازة. If a narrator is weak, keep the card's grade and the card's
   verdict (e.g. «السند معتبر بالقرائن») — the Reel must not be more confident than the scholar.
   The Imam is the last node with `imam:true` and no grade.
6. **Sources** — «الكتاب ج• ص•» with Arabic-Indic digits (`٠١٢٣٤٥٦٧٨٩`). Convert «جلد: 27, صفحه: 116» → «ج٢٧ ص١١٦».
7. **Honorifics** — «عليه السلام», «عليها السلام», «عليهم السلام», «صلى الله عليه وآله» spelled out.
8. **Never** add explanation, numbers, dates, or doctrine that is not on the cards. If a hook needs a
   claim («ثلاث صفات»), it must be countable on the card.

## 3. Hook material

The hook is the only text you *write*. It must be answerable by the hadith on screen:
- Question that the hadith answers («هل يكفي الحُبُّ لتكونَ من شيعتِهم؟»).
- Number the card provides («ثلاثُ صفاتٍ… إن فقدتَ واحدةً فلستَ منهم»).
- Stakes the hadith states («ميتةٌ جاهليّة… مَن يموتُها اليوم؟»).
Write three, score them with `hook_score_ar.py`, keep the best in `hook`, the others in `post.md`.

## 4. Slug and title

`slug` = ASCII transliteration of the first 3–4 words (`shiatuna-almuslimun-liamrina`); `title` = the
first clause of the hadith without tashkeel.

## 5. When to ask the user

- Any illegible word, grade, or page number.
- The chain is not on the cards.
- The card's verdict is nuanced (معتبر vs صحيح, موثق, حسن) and you are unsure which the user wants displayed.
- More than 10 hadith lines or more than 5 points (propose a split).
