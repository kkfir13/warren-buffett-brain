# Local Warren Buffett Brain MCP (Python / stdio)

This is a **local, read-only MCP server** for AI desktop clients that support the `stdio` transport. It reads the repository's `knowledge/atlas.json` on your computer. It needs **Python 3.10+**, but no hosted server, database, API key, ValuEdge login or broker connection.

**It is not a public remote MCP URL, a ChatGPT web/mobile connector, or an installed ChatGPT Skill.** If you simply want to try the research method in ChatGPT, use [the prompt guide](../CHATGPT.md).

## Run it

```bash
git clone https://github.com/kkfir13/warren-buffett-brain.git
cd warren-buffett-brain
python3 local-mcp/server.py
```

The process listens for JSON-RPC messages on **standard input** and writes responses to **standard output**. It normally waits without printing a prompt; this is expected. A compatible MCP client manages the process and requests.

## Configure a compatible desktop MCP client

Use a **real absolute filesystem path** on your computer. The example below is a generic stdio MCP configuration; each desktop client's settings location may differ.

```json
{
  "mcpServers": {
    "warren-buffett-brain": {
      "command": "python3",
      "args": ["/ABSOLUTE/PATH/TO/warren-buffett-brain/local-mcp/server.py"]
    }
  }
}
```

If `python3` is not available under that name on your platform, use the full path to a working Python 3.10+ executable. Restart the client if it doesn't discover the server.

The available tools are:

- `search({query, limit?})` — search the locally bundled, source-linked historical notes.
- `fetch({id})` — read a specific note or source record using its exact ID.
- `research_overview({})` — understand the current corpus and limitations.

For example, ask your connected client to **search for GEICO**, then **fetch one of the returned record IDs** and report both historical evidence and uncertainties. These are public historical research records, not market-data or trading tools.

## Verify and troubleshoot

From the repository root:

```bash
python3 -m unittest tests.test_offline_mcp -v
```

If the desktop client sees no tools, verify Python, the absolute path, the client's **stdio MCP** support and its logs. Do not paste this configuration into ChatGPT as a way of installing a plugin.

This adapter does not upload searches to a Buffett Brain backend. Your chosen AI client may separately process your conversation under its own privacy settings. Linked source sites are third parties and are not downloaded by the adapter.

For research-agent instructions and source limitations, read [AGENTS.md](../AGENTS.md). For an optional self-hosted remote MCP implementation, see [mcp/](../mcp/README.md).
