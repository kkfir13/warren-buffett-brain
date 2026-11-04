# Self-host Warren Buffett Brain as an MCP server (optional)

This directory contains a **read-only, open-source Streamable HTTP MCP server** for Cloudflare Workers. It lets compatible MCP clients search the public Warren Buffett Brain research notes. It is **source code**, not a live connection that you can install directly in ChatGPT.

**Most people do not need to run this server.** To try the research methodology in ChatGPT, use [the ChatGPT guide](../CHATGPT.md). To read the historical sources, browse [the archive](../knowledge/atlas.json). For a local, no-hosting MCP setup, use the [Python stdio adapter](../local-mcp/README.md).

## What the server can do

It provides exactly three read-only tools:

| Tool | Input | Result |
| --- | --- | --- |
| `search` | `{"query":"GEICO","limit":5}` | Matches from the 55-note historical evidence index |
| `fetch` | `{"id":"<id returned by search>"}` | One source-linked note or source record |
| `research_overview` | `{}` | Research coverage and limitations |

The project bundles **55 independently authored notes** and **60 source links** from `../knowledge/atlas.json` at build time. Links are not copies of copyrighted letters/books or proof that every original was read.

The server **does not** provide live prices, financial accounts, private holdings, a valuation API, trading, user-specific tools or Buffett's personal current-stock opinions. It does not call ValuEdge or a Supabase database.

## Where is the public MCP URL?

**This repository does not publish or verify an official hosted Buffett Brain MCP URL.** The discontinued experiment on ValuEdge Supabase is not a usable public endpoint. GitHub Pages hosts a static website and cannot accept MCP POST requests.

If you choose to self-host the Worker, Cloudflare assigns a hostname; your own endpoint will be the exact hostname plus `/mcp`. Do not put a placeholder URL into an MCP client or assume another deployment is maintained by this project.

## Run or deploy your own instance

Requires a Cloudflare account, Node.js (the project's CI uses Node 22), and npm.

```bash
git clone https://github.com/kkfir13/warren-buffett-brain.git
cd warren-buffett-brain/mcp
npm install
npm test
npx wrangler dev
```

This starts a **local development server**, not an internet-facing endpoint. To deploy your own Worker, log in to Cloudflare and run:

```bash
npx wrangler login
npx wrangler deploy
```

The Worker settings live in `wrangler.jsonc`; the implementation is `worker.ts`. When using Cloudflare's GitHub integration, point the project root to `mcp` and ensure the checkout also contains `../knowledge/atlas.json` at build time.

**After deployment, verify the actual returned hostname:**

1. GET `https://YOUR-REAL-HOST/health`; a healthy build returns JSON with `status: "ok"` and the number of notes.
2. Connect an [MCP Inspector](https://github.com/modelcontextprotocol/inspector) client using **Streamable HTTP** to `https://YOUR-REAL-HOST/mcp`.
3. Verify `initialize`, `tools/list`, then call `search` for `GEICO`, and `fetch` using an actual returned result ID. Try `research_overview` too.
4. Connect to your intended MCP client **only if** that client supports custom remote MCP connections. ChatGPT support varies by account, workspace, permissions and interface; deploying a Worker does not make a public ChatGPT plugin.

The server creates a fresh stateless transport for each request. It includes request-size and input-complexity limits, but this does **not** make an unauthenticated public service immune to abuse.

## Costs, privacy and limitations

- A public self-hosted server allows anonymous research requests. You are responsible for **rate limiting, hosting limits, operating costs and logs**.
- Cloudflare or another hosting provider may process client IP addresses and requests. Avoid sending passwords, private account details or sensitive portfolio data; the tools do not need them.
- The code uses bundled public records and does not write a user-profile database, but you must check your **own** deployment's logging and privacy configuration before advertising it.
- A new commit to `knowledge/atlas.json` is **not automatically live** on an already deployed Worker; rebuild/redeploy it.
- If you receive an HTTP 200 but `tools/list` or `tools/call` fails, the MCP connection is **not verified**.

For tool behavior, read `worker.ts` and `evidence.mjs`. For deployment workflows, app-directory submissions, and host-verification procedures, see **[maintainer operations](../docs/MAINTAINER.md)** rather than using those procedures as end-user installation steps.

Independent project; not affiliated with Warren Buffett or Berkshire Hathaway. See [privacy](../PRIVACY.md) and [terms](../TERMS.md).
