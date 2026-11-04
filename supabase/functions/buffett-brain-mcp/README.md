# Deployed Supabase MCP function

This directory preserves the exact source of the public, read-only `buffett-brain-mcp` Edge Function first deployed on November 4, 2026 to the existing ValuEdge Supabase project. It has **no database access in application code**, no customer-specific tools, no trading functionality, and accepts unauthenticated public requests by design.

Production endpoint: `https://axmttnzfvzsfhcruhmce.supabase.co/functions/v1/buffett-brain-mcp/mcp`

The project also includes a Cloudflare Worker alternative at `mcp/worker.ts`. Both backends use the same canonical `mcp/evidence.mjs` retrieval logic.

For a reproducible future deployment, from the repository root:

```sh
python3 scripts/sync_supabase_mcp.py
supabase link --project-ref axmttnzfvzsfhcruhmce
supabase functions deploy --no-verify-jwt buffett-brain-mcp
```

Only run the deploy if you intentionally intend to update the public endpoint. Review network costs and request volumes, as this public function consumes resources on the existing ValuEdge Supabase project. A dedicated hosting account or a custom-domain Cloudflare Worker is preferable for a larger launch.

The project hostname `*.supabase.co` is not a domain the project owner controls at its root. OpenAI public **With MCP** review additionally requires a root-level `/.well-known/openai-apps-challenge` file on the MCP hostname or an eligible parent. To complete directory publication, migrate the MCP public hostname to one you control and can verify. This does not prevent direct MCP connections.
