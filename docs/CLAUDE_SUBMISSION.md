# Claude and ChatGPT: separate submission formats

## Claude directory: use the dedicated plugin folder

Repository: `https://github.com/kkfir13/warren-buffett-brain`
Plugin path: `claude-plugin`
Branch: `main`

The direct folder link is https://github.com/kkfir13/warren-buffett-brain/tree/main/claude-plugin . Paste it in the Source repository field to have Claude prefill the path, or expand "Plugin in a subfolder or on another branch?" and set `claude-plugin` manually. Click **Re-validate** after changes. Submitting the repository root is not the correct Claude layout; its `plugin.json` is for the portable OpenAI package, not the Claude manifest.

The Claude folder contains `.claude-plugin/plugin.json`, `.mcp.json`, a self-contained skills directory with its references, `README.md`, `LICENSE` and one SVG icon. It intentionally excludes binary ZIP artifacts and build tools that cause unnecessary directory holds.

For a local precheck run `claude plugin validate ./claude-plugin` with a recent Claude Code version, then validate in Claude's [directory portal](https://claude.ai/directory/manage). Check that the public tools can be called after connecting, test historical questions with no connection, and accurately answer the portal's data-handling questions. Anthropic separately asks you to submit your remote ValuEdge server as an **MCP connector**, from the same organization, in addition to the plugin bundle.

## ChatGPT directory: use portable ZIP

The root portable `plugin.json` and existing source skill remain unchanged. Build a separate remote-MCP package via `python3 scripts/build_chatgpt_plugin.py` and `python3 scripts/build_valuedge_mcp_plugin.py`, then upload `dist/warren-buffett-brain-valuedge-mcp.zip` through **With MCP** as a new plugin. Do not upload a ZIP from the entire repository or attempt to add MCP to the earlier skills-only draft.

Official documentation: https://claude.com/docs/plugins/submit and https://developers.openai.com/plugins/deploy/submission .
