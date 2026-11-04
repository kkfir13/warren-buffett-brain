#!/usr/bin/env python3
"""Refresh the deployed-source mirror from canonical public research files."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/"supabase/functions/buffett-brain-mcp"
(target/"atlas.json").write_bytes((ROOT/"knowledge/atlas.json").read_bytes())
(target/"evidence.mjs").write_bytes((ROOT/"mcp/evidence.mjs").read_bytes())
print("Synced public MCP corpus and deterministic retrieval helper to",target)
