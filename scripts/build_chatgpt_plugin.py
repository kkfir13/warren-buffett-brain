#!/usr/bin/env python3
"""Build a reproducible, skills-only ChatGPT plugin archive from canonical research files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "warren-buffett-brain"
REFERENCES = SKILL / "references"
ARCHIVE = ROOT / "dist" / "warren-buffett-brain-chatgpt-plugin.zip"

def sync():
    REFERENCES.mkdir(parents=True, exist_ok=True)
    (REFERENCES / "deep-dives").mkdir(parents=True, exist_ok=True)
    (REFERENCES / "atlas.json").write_bytes((ROOT / "knowledge" / "atlas.json").read_bytes())
    (REFERENCES / "methodology.md").write_bytes((ROOT / "references" / "methodology.md").read_bytes())
    for f in sorted((ROOT / "deep-dives").glob("*.md")):
        (REFERENCES / "deep-dives" / f.name).write_bytes(f.read_bytes())

def validate():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "warren-buffett-brain", "Unexpected plugin identity"
    assert len(manifest["extensions"]["com.openai"]["interface"]["shortDescription"]) <= 30
    source = json.loads((ROOT / "knowledge" / "atlas.json").read_text(encoding="utf-8"))
    bundle = json.loads((REFERENCES / "atlas.json").read_text(encoding="utf-8"))
    assert source == bundle, "Bundled atlas is stale: rerun with --sync"
    assert len(source["sources"]) == 60 and len(source["entries"]) == 55
    for f in (ROOT / "deep-dives").glob("*.md"):
        assert (REFERENCES / "deep-dives" / f.name).read_bytes() == f.read_bytes(), f"Stale case study: {f.name}"
    assert (REFERENCES / "methodology.md").read_bytes() == (ROOT / "references" / "methodology.md").read_bytes()
    assert (SKILL / "SKILL.md").is_file()
    assert (REFERENCES / "RIGHTS.md").is_file()

def validate_mcp_url(value: str) -> str:
    """Accept only a real-looking HTTPS MCP endpoint, not a local or placeholder URL."""
    url = urlsplit(value.strip())
    host = (url.hostname or "").lower()
    if (url.scheme != "https" or not host or url.username or url.password
            or url.query or url.fragment or not url.path.endswith("/mcp")
            or host in {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
            or host.endswith(".local") or host.endswith(".example")
            or "your-" in host or "example" in host or "<" in value or ">" in value):
        raise ValueError("Use the live deployed public HTTPS endpoint ending in /mcp (no placeholders, credentials or localhost).")
    if not "." in host:
        raise ValueError("MCP hostname must be a public fully-qualified domain.")
    return value.strip()


def build(output: Path, mcp_url: str | None = None):
    validate()
    output.parent.mkdir(parents=True, exist_ok=True)
    paths = [ROOT / "plugin.json", ROOT / "LICENSE"] + sorted(p for p in SKILL.rglob("*") if p.is_file())
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for f in paths:
            z.write(f, f.relative_to(ROOT).as_posix())
        if mcp_url:
            url = validate_mcp_url(mcp_url)
            server = {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {
                    "warren-buffett-brain": {
                        "type": "streamable-http",
                        "url": url,
                        "extensions": {"com.openai": {"auth": {"type": "none"}}},
                    }
                },
            }
            z.writestr("mcp.json", json.dumps(server, ensure_ascii=False, indent=2) + "\\n")
    with ZipFile(output) as z:
        expected = {p.relative_to(ROOT).as_posix() for p in paths}
        if mcp_url:
            expected.add("mcp.json")
        assert set(z.namelist()) == expected
        assert z.testzip() is None
    print(f"Validated {len(paths)} files: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="refresh bundled original references")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--mcp-url", help="Verified deployed HTTPS URL ending /mcp, for a new With MCP submission")
    args = parser.parse_args()
    if args.sync:
        sync()
    target = args.output or (ROOT / "dist" / "warren-buffett-brain-with-mcp.zip" if args.mcp_url else ARCHIVE)
    build(target, args.mcp_url)
