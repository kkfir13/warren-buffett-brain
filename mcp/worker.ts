/**
 * Public, read-only MCP endpoint for Warren Buffett Brain.
 * Deploy via Cloudflare Workers; no database, API keys or user sign-in needed.
 * Production URL is issued by your own Cloudflare account only after deployment.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
import { z } from "zod";
import atlas from "../knowledge/atlas.json";
import { coverage, recordById, searchEvidence } from "./evidence.mjs";

interface Env { OPENAI_APPS_CHALLENGE?: string; }
const allowedOrigins = new Set(["https://chatgpt.com", "https://platform.openai.com"]);

function responseForTool(value: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(value) }] };
}

function mcpServer() {
  const server = new McpServer(
    { name: "warren-buffett-brain", version: "1.0.0" },
    { instructions: "Public, read-only, independent Buffett and Berkshire research. Search evidence first, then fetch specific records and cite the original source URLs. Links alone do not mean full source texts were read. Do not impersonate Buffett, invent quotes or provide live market data." },
  );
  const readonly = { readOnlyHint: true, destructiveHint: false, openWorldHint: false };
  server.registerTool("search", {
    title: "Search Warren Buffett research",
    description: "Use this when the user asks about Warren Buffett, Berkshire Hathaway investment decisions, financial history, mistakes, books, moats, capital allocation or value investing. Search the open-source evidence atlas; get source-linked records, not fabricated quotes. Then call fetch with an exact returned id.",
    annotations: readonly,
    inputSchema: {
      query: z.string().min(1).max(160).describe("Investment, company, principle, person, or year to research"),
      limit: z.number().int().min(1).max(10).optional().describe("Maximum research notes (default five)")
    }
  }, async ({ query, limit }) => responseForTool(searchEvidence(atlas, query, limit ?? 5)));
  server.registerTool("fetch", {
    title: "Fetch Buffett evidence and source links",
    description: "Use this when a search result has an id, or a source id is known, to retrieve the original evidence note, interpretation, limitations, and publisher URLs. An indexed source URL does not prove its full document has been read.",
    annotations: readonly,
    inputSchema: { id: z.string().min(1).max(120).describe("Exact research-note or source id from search") }
  }, async ({ id }) => {
    const entry = recordById(atlas, id);
    return entry ? responseForTool(entry) : { ...responseForTool({ id, message: "No matching evidence note or source id." }), isError: true };
  });
  server.registerTool("research_overview", {
    title: "Buffett Brain research coverage",
    description: "Use this to see which types of Warren Buffett historical research the open-source project contains, its evidence counts, and its limitations.",
    annotations: readonly,
    inputSchema: {}
  }, async () => responseForTool(coverage(atlas)));
  return server;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === "/.well-known/openai-apps-challenge") {
      // OpenAI issues a unique token during submission; leave absent until issued.
      return env.OPENAI_APPS_CHALLENGE
        ? new Response(env.OPENAI_APPS_CHALLENGE, { headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" } })
        : new Response("Not configured", { status: 404 });
    }
    if (url.pathname === "/health" && request.method === "GET") {
      return Response.json({ status: "ok", server: "warren-buffett-brain", notes: atlas.entries.length });
    }
    if (url.pathname !== "/mcp") return new Response("Not found", { status: 404 });
    if (request.method === "OPTIONS") {
      const origin = request.headers.get("origin") ?? "";
      return new Response(null, {
        status: 204,
        headers: allowedOrigins.has(origin) ? {
          "access-control-allow-origin": origin,
          "access-control-allow-methods": "POST, GET, DELETE, OPTIONS",
          "access-control-allow-headers": "content-type, accept, mcp-session-id, mcp-protocol-version",
          "vary": "Origin"
        } : {}
      });
    }
    if (!["POST", "GET", "DELETE"].includes(request.method)) return new Response("Method not allowed", { status: 405 });
    // Reject hostile browser origins. Server-to-server MCP clients may send no Origin.
    const origin = request.headers.get("origin");
    if (origin && !allowedOrigins.has(origin)) {
      return new Response("Origin not allowed", { status: 403 });
    }
    const contentLength = Number(request.headers.get("content-length") ?? "0");
    if (Number.isFinite(contentLength) && contentLength > 32768) {
      return new Response("Request too large", { status: 413 });
    }
    // A new McpServer AND stateless transport for each HTTP request.
    // ChatGPT calls initialize, tools/list and tools/call as separate HTTP requests.
    const server = mcpServer();
    const transport = new WebStandardStreamableHTTPServerTransport({
      sessionIdGenerator: undefined
    });
    await server.connect(transport);
    try {
      const response = await transport.handleRequest(request);
      const origin = request.headers.get("origin") ?? "";
      if (!allowedOrigins.has(origin)) return response;
      const headers = new Headers(response.headers);
      headers.set("access-control-allow-origin", origin);
      headers.set("vary", "Origin");
      return new Response(response.body, { status: response.status, headers });
    } catch (error) {
      console.error("MCP transport error", error instanceof Error ? error.message : "Unknown error");
      return Response.json({ error: "MCP request failed" }, { status: 500 });
    }
  },
};
