#!/usr/bin/env python3
"""Search the original Buffett Brain evidence atlas offline. No remote requests."""
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

ATLAS = Path(__file__).resolve().parents[1] / "knowledge" / "atlas.json"
WORD = re.compile(r"[a-z0-9]+", re.I)

def tokenize(value):
    return [w.lower() for w in WORD.findall(str(value)) if len(w) >= 2]

def score_matches(entries, query, kind=None):
    selected = [e for e in entries if not kind or e["kind"] == kind]
    tokens = tokenize(query)
    if not tokens:
        return [(0.0,e) for e in selected]
    def text(e):
        return " ".join([e["title"],e["summary"],e["evidence"],e["interpretation"],
                         e["limitations"]," ".join(e.get("topics",[]))," ".join(e.get("companies",[])),str(e["year"])])
    documents = [Counter(tokenize(text(e))) for e in selected]
    n=len(documents)
    df=Counter(w for d in documents for w in d)
    avg_length=sum(sum(d.values()) for d in documents)/max(1,n)
    scored=[]
    for e,d in zip(selected,documents):
        length=sum(d.values())
        s=0.0
        for token in set(tokens):
            freq=d.get(token,0)
            if not freq: continue
            idf=math.log(1+(n-df[token]+0.5)/(df[token]+0.5))
            s+=idf*freq*(1.2+1)/(freq+1.2*(0.25+0.75*length/max(1,avg_length)))
        title_tokens=tokenize(e["title"])
        s+=sum(0.5 for token in tokens if token in title_tokens)
        if s>0: scored.append((s,e))
    return sorted(scored,key=lambda pair:(-pair[0],-pair[1]["year"],pair[1]["id"]))

def search(atlas,query,kind=None,limit=8):
    sources={s["id"]:s for s in atlas["sources"]}
    result=[]
    for score,entry in score_matches(atlas["entries"],query,kind)[:limit]:
        result.append({**entry,"score":round(score,4),
            "sources":[{"id":sid,"title":sources[sid]["title"],"url":sources[sid]["url"]}
                       for sid in entry["sourceIds"]]})
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query",help="search question, company, theme, or transaction")
    parser.add_argument("--kind",choices=["decision","mistake","principle","book","interview","statement"])
    parser.add_argument("--limit",type=int,default=8)
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args()
    with ATLAS.open(encoding="utf-8") as f:atlas=json.load(f)
    results=search(atlas,args.query,args.kind,max(1,min(args.limit,50)))
    if args.json: print(json.dumps({"query":args.query,"results":results},ensure_ascii=False,indent=2));return
    if not results: print("No grounded entries found. Check the original source archive; do not guess.");return
    for n,row in enumerate(results,1):
        print(f"{n}. [{row['kind']} · {row['year']}] {row['title']}")
        print(f"   {row['summary']}")
        print(f"   Source evidence: {row['evidence']}")
        print(f"   What remains uncertain: {row['limitations']}")
        for s in row["sources"]: print(f"   Source: {s['title']} — {s['url']}")
if __name__=="__main__":main()
