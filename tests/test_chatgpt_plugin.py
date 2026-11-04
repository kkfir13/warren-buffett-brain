"""No-network verification of the ChatGPT skills-only plugin package."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "warren-buffett-brain"

class ChatGPTPluginTests(unittest.TestCase):
    def test_manifest(self):
        p = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(p["name"], "warren-buffett-brain")
        self.assertEqual(p["extensions"]["com.openai"]["interface"]["category"], "Finance")
        self.assertLessEqual(len(p["extensions"]["com.openai"]["interface"]["displayName"]), 30)
        self.assertLessEqual(len(p["extensions"]["com.openai"]["interface"]["shortDescription"]), 30)
        self.assertTrue((SKILL / "SKILL.md").read_text().startswith("---\n"))

    def test_packaged_corpus_matches_canonical(self):
        bundled = SKILL / "references"
        self.assertEqual((ROOT / "knowledge/atlas.json").read_bytes(), (bundled / "atlas.json").read_bytes())
        self.assertEqual((ROOT / "references/methodology.md").read_bytes(), (bundled / "methodology.md").read_bytes())
        for case in (ROOT / "deep-dives").glob("*.md"):
            self.assertEqual(case.read_bytes(), (bundled / "deep-dives" / case.name).read_bytes())

    def test_clean_plugin_zip(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.zip"
            subprocess.run([sys.executable, str(ROOT / "scripts/build_chatgpt_plugin.py"), "--output", str(path)], check=True, capture_output=True, text=True)
            with ZipFile(path) as z:
                names = z.namelist()
                self.assertIn("plugin.json", names)
                self.assertIn("skills/warren-buffett-brain/SKILL.md", names)
                self.assertIn("skills/warren-buffett-brain/references/atlas.json", names)
                self.assertNotIn("index.html", names)
                self.assertIsNone(z.testzip())
                self.assertEqual(len(json.loads(z.read("skills/warren-buffett-brain/references/atlas.json"))["entries"]), 55)
        released = ROOT / "dist" / "warren-buffett-brain-chatgpt-plugin.zip"
        if released.is_file():
            with ZipFile(released) as z:
                self.assertIsNone(z.testzip())
                for name in names:
                    self.assertEqual(z.read(name), (ROOT / name).read_bytes(), f"Stale released ZIP member: {name}")

if __name__ == "__main__":
    unittest.main()
