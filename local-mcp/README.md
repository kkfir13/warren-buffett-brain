# Offline MCP (advanced users, no hosting bill)

For users who prefer an MCP connection rather than an installed ChatGPT skill, Buffett Brain includes an **optional local stdio MCP server** written in Python standard library. It runs on the user's own computer and reads `knowledge/atlas.json` directly. **It does not use Supabase, ValuEdge, Cloudflare, API keys or any hosted inference.**

## Requirements

Python 3.10+ and a compatible **desktop** MCP client with support for stdio. This is not a one-click ChatGPT web/mobile connector and should not be advertised as such.

```bash
git clone https://github.com/kkfir13/warren-buffett-brain.git
cd warren-buffett-brain
python3 local-mcp/server.py
```

The server waits for JSON-RPC requests on stdin and emits responses to stdout. To configure it in a desktop client, use the **absolute path** to `local-mcp/server.py` in the MCP client settings:

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

It exposes `search`, `fetch` and `research_overview` as read-only tools. Searches are deterministic; source documents are linked, not bundled as copyrighted full texts.

For the broadest ChatGPT distribution, **the main product is the bundled Skills-only plugin** in `dist/warren-buffett-brain-chatgpt-plugin.zip`. That plugin does not require this local MCP server. Public directory installation still requires the developer to complete OpenAI review and publish.

## Testing

```bash
python3 -m unittest tests.test_offline_mcp -v
```

A public remote MCP server is optional, not deployed by this project. The independent Cloudflare Worker reference implementation remains in `mcp/` for maintainers who choose to run their own infrastructure; it is not connected to ValuEdge.
