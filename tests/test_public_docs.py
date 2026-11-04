"""Guardrails for user-facing and AI-agent documentation, without network access."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        info = dict(attrs)
        if tag == "a" and info.get("href"):
            self.hrefs.append(info["href"])
        if tag == "h1":
            self.headings += 1


class PublicDocumentationTests(unittest.TestCase):
    def test_documented_entrypoints_exist(self):
        paths = (
            "README.md", "CHATGPT.md", "AGENTS.md", "SKILL.md",
            "skills/warren-buffett-brain/SKILL.md",
            "knowledge/atlas.json", "local-mcp/server.py",
            "mcp/worker.ts", "install/index.html",
            "dist/warren-buffett-brain-chatgpt-plugin.zip",
            "dist/warren-buffett-brain-personal-skill.zip",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())

    def test_prompt_does_not_pretend_to_load_corpus(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        chatgpt = (ROOT / "CHATGPT.md").read_text(encoding="utf-8")
        html = (ROOT / "install/index.html").read_text(encoding="utf-8")
        self.assertIn("not** an installed skill", readme)
        self.assertIn("automatically read", chatgpt)
        self.assertIn("does not automatically load", html)
        self.assertIn("not yet publicly listed", html)
        self.assertIn("Personal Skill ZIP", chatgpt)
        self.assertIn("not publicly listed", readme)

    def test_agent_has_canonical_paths_and_source_caveats(self):
        agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        knowledge = (ROOT / "knowledge/README.md").read_text(encoding="utf-8")
        atlas = json.loads((ROOT / "knowledge/atlas.json").read_text(encoding="utf-8"))
        for p in ("knowledge/atlas.json", "deep-dives/", "sourceIds",
                  "verbatimExcerpt", "AGENTS.md"):
            combined = agent + knowledge + (ROOT / "README.md").read_text(encoding="utf-8")
            self.assertIn(p, combined)
        self.assertNotIn("public/buffett/atlas.json", knowledge)
        self.assertIn("skills/warren-buffett-brain/references/atlas.json", knowledge)
        self.assertEqual(len(atlas["entries"]), 55)
        self.assertEqual(len(atlas["sources"]), 60)

    def test_web_install_help_is_realistically_labeled(self):
        html = (ROOT / "install/index.html").read_text(encoding="utf-8")
        parser = Links()
        parser.feed(html)
        self.assertEqual(parser.headings, 1)
        self.assertIn("https://github.com/kkfir13/warren-buffett-brain/blob/main/AGENTS.md", parser.hrefs)
        self.assertIn("https://help.openai.com/en/articles/20001066-skills-in-chatgpt/", parser.hrefs)
        self.assertIn("Personal Skill ZIP", html)
        self.assertIn("not a one-click ChatGPT web/mobile connector", html)


if __name__ == "__main__":
    unittest.main()
