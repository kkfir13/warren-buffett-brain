"use strict";
const byId=id=>document.getElementById(id);
const mk=(tag,css="",content="")=>{const node=document.createElement(tag);if(css)node.className=css;node.textContent=String(content);return node};
const groupLabels={decision:"Transaction",mistake:"Mistake",principle:"Principle",book:"Book",interview:"Interview",statement:"Verbatim excerpt"};
let atlas=null,kind="all",term="",take=12,allResults=[];
function terms(text){return String(text||"").toLowerCase().match(/[a-z0-9]+/g)||[]}
function results(){
 const words=terms(term);
 return atlas.entries.filter(e=>kind==="all"||e.kind===kind).map(e=>{
  const title=e.title.toLowerCase(),company=e.companies.join(" ").toLowerCase(),topic=e.topics.join(" ").toLowerCase();
  const body=[e.summary,e.evidence,e.interpretation,e.limitations].join(" ").toLowerCase();
  const score=words.length?words.reduce((s,w)=>s+(title.includes(w)?5:0)+(company.includes(w)?4:0)+(topic.includes(w)?3:0)+(body.includes(w)?1:0)+(String(e.year).includes(w)?3:0),0):1;
  return {e,score};
 }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||b.e.year-a.e.year).map(x=>x.e);
}
function detail(node,label,desc){const d=mk("div","detail");d.append(mk("strong","",label),mk("p","",desc));node.append(d)}
function card(e){
 const root=mk("article","card"),head=mk("div","card-head");head.append(mk("span","tag",groupLabels[e.kind]),mk("span","year",e.year));
 root.append(head,mk("h3","",e.title));
 if(e.verbatimExcerpt && e.speaker){const block=mk("blockquote","quote",e.verbatimExcerpt);const speaker=mk("cite","",e.speaker);block.append(speaker);root.append(block)}
 root.append(mk("p","",e.summary));
 const expanded=mk("details");expanded.append(mk("summary","","Evidence, interpretation & original sources"));
 detail(expanded,"WHAT THE DOCUMENT ESTABLISHES",e.evidence);
 detail(expanded,"OUR INTERPRETATION — NOT A BUFFETT QUOTE",e.interpretation);
 detail(expanded,"UNCERTAINTY & LIMITATIONS",e.limitations);
 if(e.locator)expanded.append(mk("p","", "Locator: "+e.locator));
 const list=mk("ul","sources-list"),sources=new Map(atlas.sources.map(x=>[x.id,x]));
 e.sourceIds.forEach(id=>{const src=sources.get(id);if(!src)return;
  const li=mk("li"),link=mk("a","",src.title+" ↗");link.href=src.url;link.target="_blank";link.rel="noopener noreferrer";li.append(link);list.append(li)});
 expanded.append(list);
 if(e.deepDivePath && /^deep-dives\/[a-z0-9-]+\.md$/.test(e.deepDivePath)){
   const deep=mk('a','longform','Read the complete source-linked case study ↗');
   deep.href='./cases/'+e.deepDivePath.slice('deep-dives/'.length).replace(/\.md$/,'')+'/';
   expanded.append(deep);
 }
 root.append(expanded);return root;
}
function render(){
 if(!atlas)return;
 allResults=results();const container=byId("cards");container.replaceChildren();
 byId("status").textContent=allResults.length?(allResults.length+" sourced research notes. Open each card for evidence and limitations."):
  "No documented note matches this query. Try a different term or browse the primary archive below.";
 allResults.slice(0,take).forEach(x=>container.append(card(x)));
 const more=byId("more");more.hidden=allResults.length<=take;more.textContent="Show more ("+(allResults.length-take)+" remaining)";
}
function apply(q){
 term=q.trim();take=12;const params=new URLSearchParams(location.search);
 if(term)params.set("q",term);else params.delete("q");
 const qs=params.toString();history.replaceState(null,"",location.pathname+(qs?"?"+qs:"")+location.hash);render();
}
async function start(){
 byId("search-form").addEventListener("submit",ev=>{ev.preventDefault();apply(byId("query").value)});
 byId("more").addEventListener("click",()=>{take+=12;render()});
 document.querySelectorAll("[data-example]").forEach(b=>b.addEventListener("click",()=>{byId("query").value=b.dataset.example;apply(b.dataset.example)}));
 document.querySelectorAll("[data-kind]").forEach(b=>b.addEventListener("click",()=>{
  kind=b.dataset.kind;take=12;document.querySelectorAll("[data-kind]").forEach(item=>{item.classList.toggle("active",item===b);item.setAttribute("aria-pressed",item===b?"true":"false")});render();
 }));
 term=new URLSearchParams(location.search).get("q")||"";byId("query").value=term;
 try{
  const response=await fetch("./knowledge/atlas.json");if(!response.ok)throw Error("Atlas HTTP "+response.status);
  const candidate=await response.json();
  if(candidate.schemaVersion!=="buffett-brain-atlas-v1"||!Array.isArray(candidate.sources)||!Array.isArray(candidate.entries))throw Error("Invalid atlas");
  atlas=candidate;byId("count-entries").textContent=atlas.entries.length+" original research notes";byId("count-sources").textContent=atlas.sources.length+" linked sources";
  atlas.sources.filter(s=>s.type==="shareholder_letter").sort((a,b)=>b.year-a.year).forEach(s=>{
   const a=mk("a","",s.year);a.href=s.url;a.target="_blank";a.rel="noopener noreferrer";a.title=s.title;byId("years").append(a)});
  render();
 }catch(error){byId("status").textContent="Unable to read the local research atlas. Run a local HTTP server from the buffett-brain folder and reload.";console.error(error)}
}
start();