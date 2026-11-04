import assert from "node:assert/strict";
const endpoint = "https://axmttnzfvzsfhcruhmce.supabase.co/functions/v1/buffett-brain-mcp/mcp";
const wait = (ms) => AbortSignal.timeout(ms);
const health = await fetch(endpoint.slice(0,-4)+"health",{signal:wait(20000)});
assert.equal(health.status,200,"Health HTTP status "+health.status);
const json = await health.json();
assert.equal(json.status,"ok");
assert.equal(json.notes,55);
assert.equal(json.sources,60);
console.log("PASS live Supabase MCP health:",json.status);
async function rpc(id,method,params){
  const res=await fetch(endpoint,{
    method:"POST",headers:{"accept":"application/json, text/event-stream","content-type":"application/json"},
    body:JSON.stringify({jsonrpc:"2.0",id,method,params}),
    signal:wait(20000)
  });
  const raw=await res.text();
  assert.ok(res.ok,"HTTP "+res.status+" "+raw.slice(0,500));
  const lines=raw.split(/\r?\n/).filter(x=>x.startsWith("data:")).map(x=>x.slice(5).trim());
  const data=JSON.parse(lines.at(-1)??raw);
  assert.ok(!data.error,"JSON-RPC error "+JSON.stringify(data.error));
  return data.result;
}
const init=await rpc(1,"initialize",{
  protocolVersion:"2025-06-18",capabilities:{},clientInfo:{name:"buffett-ci-smoke",version:"1.0.0"}
});
assert.equal(init.serverInfo.name,"warren-buffett-brain");
console.log("PASS MCP initialize");
const tools=(await rpc(2,"tools/list",{})).tools;
assert.deepEqual(tools.map(t=>t.name).sort(),["fetch","research_overview","search"]);
for(const t of tools){
 assert.equal(t.annotations?.readOnlyHint,true);
 assert.equal(t.annotations?.destructiveHint,false);
 assert.equal(t.annotations?.openWorldHint,false);
}
console.log("PASS MCP tools/list with correct read-only annotations");
const search=JSON.parse((await rpc(3,"tools/call",{name:"search",arguments:{query:"GEICO",limit:3}})).content[0].text);
assert.ok(search.results.length>0 && search.results.some(x=>JSON.stringify(x).includes("GEICO")));
assert.ok(search.results.some(x=>x.sources.length>0));
console.log("PASS source-linked GEICO research search");
const detail=JSON.parse((await rpc(4,"tools/call",{name:"fetch",arguments:{id:search.results[0].id}})).content[0].text);
assert.equal(detail.recordType,"research-note");
assert.ok(detail.sourceLinks.length>0);
console.log("PASS note fetch with citations");
const overview=JSON.parse((await rpc(5,"tools/call",{name:"research_overview",arguments:{}})).content[0].text);
assert.equal(overview.originalResearchNotes,55);
console.log("PASS research overview");
