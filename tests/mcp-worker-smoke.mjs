import assert from "node:assert/strict";

const base = "http://127.0.0.1:8788";
const health = await fetch(base + "/health", { signal: AbortSignal.timeout(20000) });
assert.equal(health.status, 200);
const about = await health.json();
assert.equal(about.status, "ok");
assert.equal(about.notes, 55);

async function rpc(id, method, params) {
  const result = await fetch(base + "/mcp", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "accept": "application/json, text/event-stream"
    },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
    signal: AbortSignal.timeout(20000)
  });
  const body = await result.text();
  assert.equal(result.status, 200, body.slice(0, 1500));
  const eventLines = body.split(/\r?\n/).filter(x => x.startsWith("data:")).map(x => x.slice(5).trim());
  const packet = JSON.parse(eventLines.at(-1) || body);
  assert.ok(!packet.error, JSON.stringify(packet.error));
  return packet.result;
}
const init = await rpc(1, "initialize", {
  protocolVersion: "2025-06-18",
  capabilities: {},
  clientInfo: { name: "github-ci", version: "1.0" }
});
assert.equal(init.serverInfo.name, "warren-buffett-brain");
const list = await rpc(2, "tools/list", {});
assert.deepEqual(list.tools.map(x => x.name).sort(), ["fetch", "research_overview", "search"]);
const matching = await rpc(3, "tools/call", { name: "search", arguments: { query: "GEICO", limit: 3 } });
assert.ok(matching.content?.[0]?.text);
const records = JSON.parse(matching.content[0].text);
assert.ok(records.results.length > 0);
const one = await rpc(4, "tools/call", { name: "fetch", arguments: { id: records.results[0].id } });
assert.ok(JSON.parse(one.content[0].text).sourceLinks.length > 0);
const overview = await rpc(5, "tools/call", { name: "research_overview", arguments: {} });
assert.equal(JSON.parse(overview.content[0].text).originalResearchNotes, 55);
const disallowed = await fetch(base + "/mcp", { method: "POST", headers: { origin: "https://invalid.example", "content-type":"application/json" }, body: "{}" });
assert.equal(disallowed.status, 403);
console.log("PASS: Worker health, stateless initialize, tool discovery, GEICO search/fetch, research overview, origin check");
