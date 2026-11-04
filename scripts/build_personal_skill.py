#!/usr/bin/env python3
"""Package the bundled research skill for eligible ChatGPT Personal Skills uploads."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "warren-buffett-brain"
TARGET = ROOT / "dist" / "warren-buffett-brain-personal-skill.zip"
PREFIX = "warren-buffett-brain/"

def main():
    assert (SKILL / "SKILL.md").is_file()
    evidence = json.loads((SKILL / "references" / "atlas.json").read_text(encoding="utf-8"))
    assert len(evidence["entries"]) == 55 and len(evidence["sources"]) == 60
    paths = sorted(p for p in SKILL.rglob("*") if p.is_file())
    assert len(paths) >= 12
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(TARGET, "w", ZIP_DEFLATED, compresslevel=9) as out:
        for p in paths:
            out.write(p, PREFIX + p.relative_to(SKILL).as_posix())
    with ZipFile(TARGET) as z:
        assert z.testzip() is None
        assert PREFIX + "SKILL.md" in z.namelist()
        assert sum(path.lower().endswith("/skill.md") for path in z.namelist()) == 1
        assert not any(path.lower().endswith("/plugin.json") or path.lower().endswith("/mcp.json") for path in z.namelist())
    print("Verified Personal Skill archive:", TARGET, "files:", len(paths))

if __name__ == "__main__":
    main()
