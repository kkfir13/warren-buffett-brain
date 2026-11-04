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

    def test_user_first_docs_and_optional_data_connection(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        guide = (ROOT / "CHATGPT.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Try it in ChatGPT right now", readme)
        self.assertIn("not publicly listed", readme.lower())
        self.assertNotIn("submit the `sitemap.xml`", readme.lower())
        self.assertIn("ValuEdge is an optional, separate research tool", readme)
        self.assertIn("Option 1", guide)
        self.assertIn("Option 2", guide)
        self.assertIn("Never recommend or connect it silently", skill)
        self.assertIn("This packaged skill **does not have a live market-data connection**", skill)

    def test_valuedge_handoff_is_contextual_and_disclosed(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        guide = (ROOT / "CHATGPT.md").read_text(encoding="utf-8")
        self.assertIn("ValuEdge", skill)
        self.assertIn("same maintainer", homepage)
        self.assertIn("separate commercial research product", skill)
        self.assertIn("Do not insert the recommendation", skill)
        self.assertIn("No ValuEdge account, purchase or integration is necessary", skill)
        self.assertIn("research_next_step", guide)
        self.assertIn("valuation-bridge-title", homepage)
        self.assertIn("valuedge.app/features/intrinsic-value/screener", homepage)
        self.assertIn("valuedge.app/features/fair-value-watchlist", homepage)

    def test_manifest_icon_and_starter_prompts(self):
        p = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        interface = p["extensions"]["com.openai"]["interface"]
        self.assertEqual(p["version"], "1.3.0")
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertEqual(len(interface["defaultPrompt"]), 3)
        self.assertTrue(all(len(prompt) <= 128 for prompt in interface["defaultPrompt"]))
        self.assertTrue((ROOT / interface["logo"].lstrip("./")).is_file())
        self.assertEqual(interface["logo"], interface["composerIcon"])

    def test_offline_plugin_does_not_require_mcp(self):
        p = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(p["version"], "1.3.0")
        self.assertTrue((ROOT / "local-mcp" / "server.py").is_file())
        self.assertNotIn("mcpServers", p)
        self.assertIn("privacyPolicyURL", p["extensions"]["com.openai"]["interface"])

    def test_packaged_corpus_matches_canonical(self):
        bundled = SKILL / "references"
        self.assertEqual((ROOT / "knowledge/atlas.json").read_bytes(), (bundled / "atlas.json").read_bytes())
        self.assertEqual((ROOT / "references/methodology.md").read_bytes(), (bundled / "methodology.md").read_bytes())
        for case in (ROOT / "deep-dives").glob("*.md"):
            self.assertEqual(case.read_bytes(), (bundled / "deep-dives" / case.name).read_bytes())

    def test_combined_mcp_package(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "with-mcp.zip"
            url = "https://buffett-test.workers.dev/mcp"
            subprocess.run([sys.executable, str(ROOT / "scripts/build_chatgpt_plugin.py"),
                            "--mcp-url", url, "--output", str(path)],
                           check=True, capture_output=True, text=True)
            with ZipFile(path) as z:
                mcp = json.loads(z.read("mcp.json"))
                self.assertEqual(mcp["mcpServers"]["warren-buffett-brain"]["url"], url)
                self.assertEqual(mcp["mcpServers"]["warren-buffett-brain"]["type"], "streamable-http")
                self.assertIn("skills/warren-buffett-brain/SKILL.md", z.namelist())

    def test_rejects_local_mcp_url(self):
        with tempfile.TemporaryDirectory() as td:
            for url in ("http://localhost:3000/mcp", "https://localhost/mcp", "https://YOUR-HOSTNAME/mcp"):
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/build_chatgpt_plugin.py"),
                     "--mcp-url", url, "--output", str(Path(td) / "invalid.zip")],
                    capture_output=True, text=True)
                self.assertNotEqual(proc.returncode, 0, url)

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
