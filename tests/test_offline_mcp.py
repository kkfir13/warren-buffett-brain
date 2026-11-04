"""End-to-end, subprocess-only tests for the local no-server MCP adapter."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "local-mcp" / "server.py"

class OfflineMCPTests(unittest.TestCase):
    def messages(self, steps):
        raw = "".join(json.dumps(s) + "\n" for s in steps)
        process = subprocess.run([sys.executable, str(SCRIPT)], input=raw,
                                 capture_output=True, text=True, timeout=10, check=True)
        self.assertEqual(process.stderr, "")
        return [json.loads(line) for line in process.stdout.strip().splitlines()]

    def test_handshake_and_source_linked_research(self):
        calls = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "search", "arguments": {"query": "GEICO", "limit": 3}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "research_overview", "arguments": {}}}
        ]
        r = self.messages(calls)
        self.assertEqual(len(r), 4)
        self.assertEqual(r[0]["result"]["serverInfo"]["name"], "warren-buffett-brain-offline")
        tools = r[1]["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, {"search", "fetch", "research_overview"})
        self.assertTrue(all(t["annotations"]["readOnlyHint"] for t in tools))
        self.assertFalse(any(t["annotations"]["destructiveHint"] for t in tools))
        search = json.loads(r[2]["result"]["content"][0]["text"])
        self.assertGreater(search["total"], 0)
        self.assertTrue(any(e["sourceLinks"] for e in search["results"]))
        overview = json.loads(r[3]["result"]["content"][0]["text"])
        self.assertEqual((overview["researchNotes"], overview["externalSourceLinks"]), (55, 60))

    def test_fetch_and_negative_cases(self):
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
             "params": {"name": "fetch", "arguments": {"id": "berkshire-textile-1965"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
             "params": {"name": "fetch", "arguments": {"id": "../../not-a-note"}}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "search", "arguments": {"query": "GEICO", "limit": 100}}},
        ]
        r = self.messages(requests)
        note = json.loads(r[0]["result"]["content"][0]["text"])
        self.assertEqual(note["id"], "berkshire-textile-1965")
        self.assertTrue(note["sourceLinks"][0]["url"].startswith("https://"))
        self.assertTrue(r[1]["result"]["isError"])
        self.assertTrue(r[2]["result"]["isError"])

if __name__ == "__main__":
    unittest.main()
