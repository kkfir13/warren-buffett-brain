#!/usr/bin/env python3
"""Build a reproducible, skills-only ChatGPT plugin archive from canonical research files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
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

def build(output: Path):
    validate()
    output.parent.mkdir(parents=True, exist_ok=True)
    paths = [ROOT / "plugin.json", ROOT / "LICENSE"] + sorted(p for p in SKILL.rglob("*") if p.is_file())
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for f in paths:
            z.write(f, f.relative_to(ROOT).as_posix())
    with ZipFile(output) as z:
        assert set(z.namelist()) == {p.relative_to(ROOT).as_posix() for p in paths}
        assert z.testzip() is None
    print(f"Validated {len(paths)} files: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="refresh bundled original references")
    parser.add_argument("--output", type=Path, default=ARCHIVE)
    args = parser.parse_args()
    if args.sync:
        sync()
    build(args.output)
