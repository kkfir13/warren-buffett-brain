# Public Warren Buffett Brain MCP server

This directory contains an **optional, independently deployable** read-only MCP Streamable HTTP reference server for Cloudflare Workers. It is not deployed and is not part of the default plugin. The source of truth is the GitHub repository's `knowledge/atlas.json`; the 55 original research notes and 60 source links are bundled into the Worker at build time. No account, brokerage connection, ValuEdge API, server secret, paid AI inference, or user data are required for end users.

## Important status

**Optional reference implementation only. There is no active public Buffett Brain MCP endpoint hosted by this repository.** The earlier experimental deployment using ValuEdge resources was disabled. The default product is a [zero-backend Skills-only ChatGPT plugin](../CHATGPT.md), and users can run the [local MCP adapter](../local-mcp/README.md) without a server subscription.

The static GitHub Pages website cannot serve MCP POST requests. A personal skills-only ChatGPT plugin is also **not** a public MCP server.

## Deploy directly from the existing GitHub repository (recommended)

Cloudflare Workers Builds can deploy this **subdirectory of the existing monorepo**. You do not need a separate repository, a GitHub Actions deploy token, a ValuEdge account, or an MCP Plugin ZIP.

1. Open [Cloudflare Workers & Pages](https://dash.cloudflare.com/) → **Create application** → **GitHub**.
2. Authorize Cloudflare access to `kkfir13/warren-buffett-brain` (restrict GitHub repository access to this repository where possible).
3. Select `kkfir13/warren-buffett-brain`, production branch `main`.
4. Enter the build settings exactly:

   - **Worker name:** `warren-buffett-brain-mcp` (must match `mcp/wrangler.jsonc`)
   - **Root directory:** `mcp` (not `/` and not the GitHub Pages website)
   - **Build command:** `npm install --no-audit --no-fund` (if Cloudflare auto-installs dependencies, this may be left empty)
   - **Deploy command:** `npx wrangler deploy`

5. Select **Save and Deploy**. Cloudflare will assign a real public hostname on `workers.dev`, with the endpoint **`https://ACTUAL-ASSIGNED-HOST/mcp`**. Never present the placeholder as a deployed URL.
6. Test **`https://ACTUAL-ASSIGNED-HOST/health`** in the browser. Expect JSON with `status: ok` and `notes: 55`; a browser GET to `/mcp` is *not* a valid connection test.
7. Test with [MCP Inspector](https://github.com/modelcontextprotocol/inspector) using **Streamable HTTP**, no authentication: Connect → List Tools (expect `search`, `fetch`, `research_overview`) → call `search` with `{"query":"GEICO"}` → call `fetch` with an actual returned ID.
8. On an eligible ChatGPT account or workspace, go to [Plugins](https://chatgpt.com/plugins) → **+ → Add custom MCP server**; give it the name Warren Buffett Brain and the **actual** `/mcp` URL, set no authentication, acknowledge the server risk warning and confirm the discovered read-only tools. Install the plugin and in a new conversation type `@Warren Buffett Brain` and ask for a source-linked GEICO analysis.

**Availability warning:** OpenAI's current Help Center says creation of custom MCP connections is available on ChatGPT Business and Enterprise/Edu web, subject to admin/owner permissions and Enterprise/Edu RBAC. Some user accounts may not show this option; deploying the server does not unlock the ChatGPT feature for those accounts.

**Security and cost:** This public MCP has read-only research tools, does not touch ValuEdge or any broker, and authenticates no visitors. Configure [Build watch paths](https://developers.cloudflare.com/workers/ci-cd/builds/build-watch-paths/) to include `mcp/*` and `knowledge/atlas.json` so irrelevant website/README commits do not trigger Worker rebuilds. Cloudflare Free has daily request and per-request CPU limits; monitor Workers analytics and consider rate limiting if traffic grows.

## Troubleshooting

- **Cannot find repository:** In the GitHub app permission page, select the repository for Cloudflare Workers and Pages; then refresh the Cloudflare import screen.
- **No `wrangler.jsonc` found:** Root directory must be `mcp`.
- **Worker name mismatch:** Name in Cloudflare and in `mcp/wrangler.jsonc` must be exactly `warren-buffett-brain-mcp`.
- **Build fails resolving imports:** Confirm Cloudflare checked out the **whole repository**, including `knowledge/atlas.json`. Run the [MCP build validation workflow](../.github/workflows/mcp-validate-worker.yml) and inspect its logs.
- **`/health` is 404:** Check the exact assigned `workers.dev` hostname and whether the deployment succeeded.
- **Tools can be listed but not called:** Re-test via MCP Inspector. The transport must run statelessly so requests do not require a lost session.
- **ChatGPT has no Add custom MCP server:** This is an account/workspace eligibility or permission question, not a Cloudflare deployment problem.

## Deploy on Cloudflare Workers

The owner must use a Cloudflare account with permission to deploy Workers:

```bash
cd mcp
npm install
npm test
npx wrangler login
npx wrangler deploy
```

The deploy command displays the actual HTTPS hostname assigned to your Worker, typically on your own `workers.dev` subdomain. Set the MCP URL to **that verified hostname followed by `/mcp`**. Never use `localhost` or the GitHub Pages URL as an MCP endpoint. Run `npm run dev` for a *local test only*.

Changes to `knowledge/atlas.json` must be redeployed to update the MCP corpus. The Worker only retrieves bundled public historical research and does not access private databases or live prices. To limit unexpected usage and cost, turn on Cloudflare rate limits and monitor request volume before promoting it.

## Generate the correct With MCP ZIP for OpenAI submission

The original `dist/warren-buffett-brain-chatgpt-plugin.zip` is **Skills only** and does not contain a server reference. After your public MCP deployment is live, build a **separate** plugin ZIP with the actual MCP URL:

```bash
python3 scripts/build_chatgpt_plugin.py --mcp-url "https://YOUR-REAL-DEPLOYED-HOST/mcp"
```

This validates the address and creates `dist/warren-buffett-brain-with-mcp.zip`, including `mcp.json` and the original skill research bundle. The placeholder shown above must be replaced with your actual verified hostname.

**No local Python?** In the GitHub repository open **Actions → Build Buffett Brain With MCP submission ZIP (manual) → Run workflow** and enter the *real deployed* MCP URL. Download the generated ZIP artifact from that workflow run. This manually triggered packaging job does not run on every commit.

See [the five positive and three negative MCP review scenarios](REVIEW_CASES.md), and the [privacy statement](../PRIVACY.md) and [use terms](../TERMS.md).

## Test the *actual deployed* endpoint

Replace `MCP_URL` with the URL printed by Wrangler:

```bash
MCP_URL='https://YOUR-CLOUDFLARE-HOSTNAME/mcp'
curl -i -X POST "$MCP_URL" \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"manual-test","version":"1.0"}}}'
```

Then use [MCP Inspector](https://github.com/modelcontextprotocol/inspector), transport **Streamable HTTP**, to test `tools/list`, `search`, `fetch` and `research_overview`. An HTTP 200 alone is insufficient: initialize and representative tool calls must succeed.

## Connect in ChatGPT before public listing

On supported ChatGPT surfaces, go to **Plugins → Add custom MCP server**, enter the deployed `/mcp` URL, and follow the connection prompts. You may keep the custom connection private while testing. Users must independently add the server if no public listing exists.

## Submit publicly to the Plugins Directory

Open the [OpenAI Plugins submission portal](https://platform.openai.com/plugins) under the correct verified organization with **Apps Management: Write**. Choose **With MCP**, not **Skills only**. The public submission can include the open-source skill in `skills/warren-buffett-brain/`. A future public remote MCP plugin would be a *separate item*: do not assume it is a public listing, and do not try to add an MCP server to a previous skills-only public submission.

The public review requires control of the host. When the portal gives a challenge token, set a Worker secret or variable named `OPENAI_APPS_CHALLENGE` to the exact token and confirm:
`https://YOUR-CLOUDFLARE-HOSTNAME/.well-known/openai-apps-challenge` returns only that value. Example command:

```bash
cd mcp
npx wrangler secret put OPENAI_APPS_CHALLENGE
```

Use the *same hostname* as your real MCP URL. Submit five positive and three negative MCP review cases, truthful listing details, a verified identity, and appropriate privacy/terms URLs. The public reviewer also checks tool metadata and actual MCP connectivity.

If the portal responds `Invalid URL (POST /v1/dashapi/uploads/plugins)` before parsing the ZIP, this is **not** proof of an invalid archive. Check the selected OpenAI organization, Apps Management write permission, retry the **With MCP** draft workflow and capture browser network status/request IDs for OpenAI support. The direct Plugin Creator tool can create a **private ChatGPT plugin** but does not publish it into the developer portal.

## Tool contracts

- `search({query,limit?})` — bounded textual search of documented research notes; includes original publisher URLs.
- `fetch({id})` — return one exact note (or listed source) and its limitations, interpretations and original source links.
- `research_overview({})` — coverage counts and scope limitations.

All tools are public, read-only and free of brokerage data. No tool can write files, run jobs, retrieve private portfolios, trade securities, provide live market quotes, or speak as Warren Buffett.

© Original project material under MIT; third-party works remain with their respective publishers. Independent project, not affiliated with Warren Buffett or Berkshire Hathaway.
