#!/usr/bin/env python3
"""No-server, no-dependencies stdio MCP for local desktop clients.

This optional local MCP adapter runs entirely on the user's machine.
It does not transmit queries, request live prices, or call ValuEdge.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = json.loads((ROOT / "knowledge" / "atlas.json").read_text(encoding="utf-8"))
INDEX = {e["id"]: e for e in ATLAS["entries"]}
SOURCES = {s["id"]: s for s in ATLAS["sources"]}
NOTE = "Source links reference original publishers; they are not full-text copies or proof that every source was independently read."
TOOL_SPECS = [
    {"name": "search", "description": "Search the bundled Warren Buffett and Berkshire historical research notes by company, acquisition, mistake, year, person or investment principle. No live market data or private accounts.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string", "minLength": 1, "maxLength": 160}, "limit": {"type": "integer", "minimum": 1, "maximum": 10}}, "required": ["query"], "additionalProperties": False}},
    {"name": "fetch", "description": "Retrieve a historical note by its exact ID including evidence, interpretations, limitations and original publisher source links.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string", "minLength": 1, "maxLength": 120}}, "required": ["id"], "additionalProperties": False}},
    {"name": "research_overview", "description": "Describe the breadth and limits of the independent open-source Buffett Brain historical evidence registry.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
]
for tool in TOOL_SPECS:
    tool["annotations"] = {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False}

def source_link(source_id):
    s = SOURCES.get(source_id)
    if not s:
        return None
    return {"id": s["id"], "title": s.get("title"), "url": s.get("url"), "year": s.get("year"), "locator": s.get("locator")}

def tokenize(s):
    return re.findall(r"[a-z0-9]+", str(s or "").lower())[:18]

def search(args):
    term = args.get("query")
    if not isinstance(term, str) or not term.strip() or len(term) > 160:
        raise ValueError("query must be 1–160 characters")
    limit = args.get("limit", 5)
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 10:
        raise ValueError("limit must be an integer from 1 to 10")
    words = tokenize(term)
    rows = []
    for e in ATLAS["entries"]:
        title = str(e.get("title", "")).lower()
        companies = " ".join(e.get("companies", [])).lower()
        topics = " ".join(e.get("topics", [])).lower()
        body = " ".join(str(e.get(f, "")) for f in ("summary", "evidence", "interpretation", "limitations")).lower()
        year = str(e.get("year", ""))
        score = sum(5 * (w in title) + 4 * (w in companies) +
                    3 * (w in topics) + (w in body) + 3 * (w in year) for w in words)
        if score:
            rows.append((score, e))
    rows.sort(key=lambda r: (-r[0], -int(r[1].get("year", 0)), r[1]["id"]))
    return {"query": term, "total": len(rows),
            "results": [
                {"id": e["id"], "title": e["title"], "year": e.get("year"), "kind": e.get("kind"),
                 "snippet": e.get("summary", "")[:240],
                 "sourceLinks": [s for sid in e.get("sourceIds", []) if (s := source_link(sid))]}
                for _, e in rows[:limit]
            ], "limitations": NOTE}

def fetch(args):
    rid = args.get("id")
    if not isinstance(rid, str) or not rid or len(rid) > 120:
        raise ValueError("id must be 1–120 characters")
    entry = INDEX.get(rid)
    if entry:
        return {"id": entry["id"], "title": entry.get("title"),
                "year": entry.get("year"), "kind": entry.get("kind"),
                "summary": entry.get("summary"), "evidence": entry.get("evidence"),
                "interpretation": entry.get("interpretation"),
                "limitations": entry.get("limitations"),
                "verification": entry.get("verification"),
                "locator": entry.get("locator"),
                "sourceLinks": [s for sid in entry.get("sourceIds", []) if (s := source_link(sid))],
                "note": NOTE}
    source = source_link(rid)
    if source:
        return {"recordType": "external-source-link", **source, "note": NOTE}
    raise ValueError("ID not found in the bundled research corpus")

def overview(_):
    groups = {}
    for e in ATLAS["entries"]:
        k = e.get("kind", "other")
        groups[k] = groups.get(k, 0) + 1
    return {"project": "Warren Buffett Brain", "researchNotes": len(INDEX),
            "externalSourceLinks": len(SOURCES), "categories": groups,
            "independent": True, "liveMarketData": False, "privatePortfolioAccess": False,
            "sourceCode": "https://github.com/kkfir13/warren-buffett-brain",
            "note": NOTE}

HANDLERS = {"search": search, "fetch": fetch, "research_overview": overview}

def reply(id_, result=None, error=None):
    data = {"jsonrpc": "2.0", "id": id_}
    if error:
        data["error"] = error
    else:
        data["result"] = result
    sys.stdout.write(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()

def dispatch(msg):
    if not isinstance(msg, dict):
        reply(None, error={"code": -32600, "message": "Invalid request"})
        return
    method = msg.get("method")
    if "id" not in msg:
        return  # MCP notifications must not receive a response.
    id_ = msg["id"]
    if method == "initialize":
        reply(id_, {"protocolVersion": "2025-06-18", "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "warren-buffett-brain-offline", "version": "1.2.0"},
                    "instructions": "Source-linked historical research only. Do not impersonate Warren Buffett; distinguish original evidence from interpretation and cite publisher URLs."})
    elif method == "ping":
        reply(id_, {})
    elif method == "tools/list":
        reply(id_, {"tools": TOOL_SPECS})
    elif method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        if name not in HANDLERS:
            reply(id_, error={"code": -32602, "message": "Unknown tool"})
            return
        try:
            output = HANDLERS[name](params.get("arguments") or {})
            reply(id_, {"content": [{"type": "text", "text": json.dumps(output, ensure_ascii=False)}]})
        except (ValueError, TypeError) as exc:
            reply(id_, {"content": [{"type": "text", "text": str(exc)}], "isError": True})
    else:
        reply(id_, error={"code": -32601, "message": "Unknown method"})

def main():
    for raw in sys.stdin.buffer:
        if len(raw) > 32768:
            reply(None, error={"code": -32600, "message": "Request exceeds 32KB"})
            continue
        try:
            dispatch(json.loads(raw))
        except json.JSONDecodeError:
            reply(None, error={"code": -32700, "message": "Malformed JSON"})
        except Exception:
            reply(None, error={"code": -32603, "message": "Internal error"})

if __name__ == "__main__":
    main()
