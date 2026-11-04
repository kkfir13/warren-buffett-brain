import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { McpServer } from "npm:@modelcontextprotocol/sdk@1.25.3/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "npm:@modelcontextprotocol/sdk@1.25.3/server/webStandardStreamableHttp.js";
import { z } from "npm:zod@4.1.13";
import atlas from "./atlas.json" with { type: "json" };
import { coverage, recordById, searchEvidence } from "./evidence.mjs";

// Public, static-source research only. This function deliberately has no database
// client, permissions to trade, private data access, or outbound API calls.
const slug = "buffett-brain-mcp";
const corsOrigins = new Set(["https://chatgpt.com", "https://platform.openai.com", "https://claude.ai", "https://claude.com"]);
const maxBody = 32768;
const wrap = (obj: unknown) => ({ content: [{ type: "text" as const, text: JSON.stringify(obj) }] });
function createServer() {
  const server = new McpServer({name:"warren-buffett-brain",version:"1.0.0"},{
    instructions:"Independent, educational research on Warren Buffett's documented investments and Berkshire Hathaway. Original evidence notes, source links and limitations are available; primary documents are not reproduced. Do not impersonate Buffett or invent quotes, brokerage access, live market prices or Buffett-endorsed valuations."
  });
  const readOnly = { readOnlyHint: true, destructiveHint: false, openWorldHint: false };
  server.registerTool("search",{
    title:"Search Warren Buffett research",
    description:"Search a finite, public catalog of original historical research notes about Warren Buffett, Berkshire Hathaway, investment decisions, mistakes, Graham, Munger and value investing. Returns source-linked snippets but does not search current market news or live prices.",
    annotations:readOnly,
    inputSchema:{
      query:z.string().min(1).max(160).describe("Company, deal, historical event, person or investing principle to find"),
      limit:z.number().int().min(1).max(10).optional().describe("Maximum number of records (default 5)")
    }
  },async ({query,limit})=>wrap(searchEvidence(atlas,query,limit??5)));
  server.registerTool("fetch",{
    title:"Read a Buffett Brain research record",
    description:"Retrieve one research note or original source-link record by its ID from the public Buffett Brain catalog, including evidence, interpretations, limitations, and citation URLs. The existence of a linked source does not mean its complete text was ingested.",
    annotations:readOnly,
    inputSchema:{id:z.string().min(1).max(120).describe("Exact ID from a research-search result")}
  },async ({id})=>{
    const found=recordById(atlas,id);
    return found?wrap(found):{...wrap({id,error:"Research note or source link not found."}),isError:true};
  });
  server.registerTool("research_overview",{
    title:"See Buffett Brain research coverage",
    description:"Describe the public historical research dataset, source-link counts, available note categories, and the limits of what this MCP server can do.",
    annotations:readOnly,inputSchema:{}
  },async()=>wrap(coverage(atlas)));
  return server;
}
Deno.serve(async(req:Request)=>{
  const path=new URL(req.url).pathname;
  const allowedPrefixes=["/functions/v1/"+slug,"/"+slug,""];
  const isPath=(suffix:string)=>allowedPrefixes.some(p=>path===p+suffix);
  if(req.method==="GET" && isPath("/health"))
    return Response.json({status:"ok",server:"warren-buffett-brain",notes:atlas.entries.length,sources:atlas.sources.length},{headers:{"cache-control":"no-store","x-content-type-options":"nosniff"}});
  if(!isPath("/mcp"))return new Response("Not found",{status:404});
  const origin=req.headers.get("origin");
  if(origin && !corsOrigins.has(origin))return new Response("Origin not allowed",{status:403});
  const cors:Record<string,string>=origin?{"access-control-allow-origin":origin,"vary":"Origin"}:{};
  if(req.method==="OPTIONS")return new Response(null,{status:204,headers:{...cors,"access-control-allow-methods":"POST, GET, DELETE, OPTIONS","access-control-allow-headers":"content-type, accept, mcp-session-id, mcp-protocol-version","access-control-max-age":"600"}});
  if(!["POST","GET","DELETE"].includes(req.method))return new Response("Method not allowed",{status:405});
  if(req.method==="POST"){
    const advertised=Number(req.headers.get("content-length")??"0");
    if(advertised>maxBody)return new Response("Payload too large",{status:413});
  }
  const server=createServer();
  const transport=new WebStandardStreamableHTTPServerTransport();
  try{
    await server.connect(transport);
    const response=await transport.handleRequest(req);
    const headers=new Headers(response.headers);
    Object.entries(cors).forEach(([k,v])=>headers.set(k,v));
    headers.set("x-content-type-options","nosniff");
    headers.set("cache-control","no-store");
    return new Response(response.body,{status:response.status,headers});
  }catch(err){
    console.error("Public MCP transport error",err instanceof Error?err.message:"Unknown error");
    return Response.json({error:"Research MCP request failed"},{status:500,headers:cors});
  }
});