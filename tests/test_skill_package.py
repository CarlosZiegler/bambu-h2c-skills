import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_and_names(self):
        skills = list((ROOT / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills), 4)
        for path in skills:
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding='utf-8')
                match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
                self.assertIsNotNone(match)
                meta = yaml.safe_load(match.group(1))
                self.assertEqual(meta['name'], path.parent.name)
                self.assertRegex(meta['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
                self.assertLessEqual(len(meta['name']), 64)
                self.assertIsInstance(meta['description'], str)
                self.assertTrue(0 < len(meta['description']) <= 1024)
                self.assertNotIn('[TODO:', text)

    def test_all_relative_markdown_references_resolve(self):
        for path in [ROOT / 'README.md', *ROOT.glob('skills/**/*.md'), *ROOT.glob('docs/*.md')]:
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):
                    continue
                destination = (path.parent / unquote(target.split('#')[0])).resolve()
                with self.subTest(source=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.is_file(), f'Missing reference: {target}')

    def test_plugin_contains_all_skill_directories(self):
        plugin = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertTrue((ROOT / plugin['skills']).is_dir())
        self.assertEqual(marketplace['plugins'][0]['name'], plugin['name'])
        self.assertTrue((ROOT / marketplace['plugins'][0]['source']).is_dir())

    def test_codex_metadata_matches_skill(self):
        for path in ROOT.glob('skills/*/agents/openai.yaml'):
            meta = yaml.safe_load(path.read_text())
            skill = path.parents[1].name
            self.assertIn('$' + skill, meta['interface']['default_prompt'])
            self.assertTrue(25 <= len(meta['interface']['short_description']) <= 64)
            self.assertTrue(meta.get('policy', {}).get('allow_implicit_invocation', True))


if __name__ == '__main__':
    unittest.main()
