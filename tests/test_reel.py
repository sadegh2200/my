import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install_skills import install
from validate_reel import validate, plain


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ReelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = ROOT / 'projects/ashab-51'
        cls.spec = json.loads((cls.project / 'spec.json').read_text())
        cls.content = json.loads((cls.project / 'content.json').read_text())
        cls.builder = load_module('reel_builder', ROOT / 'maalsadiqeen-reel/scripts/build_reel.py')

    def test_both_skills_installed_idempotently(self):
        links = install(ROOT)
        self.assertEqual(len(links), 2)
        for link in links:
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), ROOT / link.name)
            self.assertIn(f'name: {link.name}\n', (link / 'SKILL.md').read_text())
        self.assertEqual(links, install(ROOT))

    def test_scripts_compile_on_python_311(self):
        for skill in ('maalsadiqeen-1', 'maalsadiqeen-reel'):
            for script in (ROOT / skill / 'scripts').glob('*.py'):
                with self.subTest(script=script):
                    compile(script.read_text(), str(script), 'exec')

    def test_spec_passes_editorial_gate(self):
        self.assertEqual(validate(self.spec, self.content), [])

    def test_positive_verdict_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec['scenes'][3]['hero'] = 'السند صحيح'
        self.assertTrue(any('verdict' in e for e in validate(spec, self.content)))

    def test_affirmative_seal_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec['scenes'][4]['seal'] = ['صحيح', 'السند']
        self.assertTrue(any('seal' in e for e in validate(spec, self.content)))

    def test_unscoped_verdict_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec['scenes'][3]['q1'] = 'والسند؟'
        self.assertTrue(any('FIRST' in e for e in validate(spec, self.content)))

    def test_changed_quotation_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec['scenes'][1]['text'][0] = 'أصحاب مئة'
        self.assertTrue(any('differs' in e for e in validate(spec, self.content)))

    def test_missing_word_cue_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec['scenes'][1]['cues']['words'].pop()
        self.assertTrue(any('word/cue' in e for e in validate(spec, self.content)))

    def test_disagreement_qualifier_is_required(self):
        spec = copy.deepcopy(self.spec)
        spec['scenes'][4]['cards'][0]['grade'] = 'ضُعّف بشدّة'
        self.assertTrue(any('qualifier' in e for e in validate(spec, self.content)))

    def test_no_unrequested_narration(self):
        spec = copy.deepcopy(self.spec)
        spec['audio']['stems'] = [{'file': 'voice.wav'}]
        self.assertTrue(any('narrator' in e for e in validate(spec, self.content)))

    def test_four_original_sources_preserved(self):
        manifest = json.loads((self.project / 'source/manifest.json').read_text())
        self.assertEqual({m['card'] for m in manifest}, {1, 2, 3, 4})
        for entry in manifest:
            self.assertEqual(hashlib.sha256((self.project / entry['file']).read_bytes()).hexdigest(), entry['sha256'])
        self.assertEqual({n for sc in self.spec['scenes'] for n in sc['source_cards']}, {1, 2, 3, 4})

    def test_quote_references_match_supplied_cards(self):
        self.assertEqual(self.spec['scenes'][1]['attribution'], 'وسائل الشيعة · ج٤ ص٥٧')
        self.assertEqual(self.spec['scenes'][2]['attribution'], 'تأويل الآيات · ج١ ص٧١٦')
        self.assertIn(plain('السند لا ينهض على شرط الصحة'), plain((self.project / 'source/transcription.md').read_text()))

    def test_hooks_are_scored_not_virality_claims(self):
        hooks = json.loads((self.project / 'hooks.json').read_text())
        self.assertEqual(len(hooks), 3)
        self.assertTrue(all(h['score'] >= 65 for h in hooks))

    def test_primary_copy_is_short(self):
        from validate_reel import words_in
        fields = {'lead', 'line1', 'line2', 'text', 'q1', 'hero', 'after', 'share', 'final'}
        count = sum(words_in(v) for sc in self.spec['scenes'] for k, v in sc.items() if k in fields)
        self.assertLessEqual(count, 70)

    def test_stacked_cards_have_no_approval_icon(self):
        ctx = self.builder.Ctx()
        self.builder.blk_proof(self.spec['scenes'][4], ctx)
        markup = ''.join(ctx.html)
        self.assertIn('card stacked', markup)
        self.assertNotIn('class="seal"', markup)
        self.assertNotIn('class="ok"', markup)
        self.assertIn('عند آخرين', markup)

    def test_arabic_widths_and_markup_escaping(self):
        for font in ('naskh', 'kufi', 'amiri-b'):
            width = self.builder.width_em('السَّنَدُ لَا يَنْهَضُ', font)
            self.assertGreater(width, 2)
            self.assertLess(width, 20)
        self.assertNotIn('<script>', self.builder.em('<script>bad</script>'))
        self.assertIn('class="em"', self.builder.em('<em>السند</em>'))

    def test_publish_text_fits_platform_fields(self):
        for name in ('caption-ar.txt', 'pinned-comment-ar.txt'):
            text = (ROOT / 'deliver/ashab-51' / name).read_text()
            self.assertLess(len(text), 2200)
        caption = (ROOT / 'deliver/ashab-51/caption-ar.txt').read_text()
        self.assertLessEqual(caption.count('#'), 5)


if __name__ == '__main__':
    unittest.main()
