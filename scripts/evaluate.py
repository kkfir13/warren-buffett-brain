#!/usr/bin/env python3
"""Offline educational six-signal screen; zero network calls or external libraries."""
import argparse, json, math
from datetime import datetime, timezone, timedelta
from pathlib import Path

def num(v):
    if v is None or isinstance(v, bool) or v == "": return None
    try: f = float(v)
    except (ValueError, TypeError): return None
    return f if math.isfinite(f) else None

def date(s):
    if not isinstance(s, str): return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except ValueError: return None

def old(s, days, now):
    d = date(s)
    return d is None or d > now + timedelta(days=1) or now-d > timedelta(days=days)

def screen(snapshot, now=None):
    now = now or datetime.now(timezone.utc)
    m = snapshot.get("metrics") or {}
    out = []
    stale = old(snapshot.get("fundamentalsAsOf"), 180, now)
    def add(key, field, comparator, unit="%"):
        v = num(m.get(field))
        out.append({"metric": key, "value": "unavailable" if v is None or stale else
                    (("%.2f" if unit == "x" else "%.1f") % v + unit),
                    "state": "unavailable" if v is None or stale else comparator(v)})
    add("roic", "roicPct", lambda v: "supporting" if v >= 15 else "review" if v >= 10 else "challenging")
    add("operating-margin", "operatingMarginPct", lambda v: "supporting" if v >= 15 else "review" if v >= 5 else "challenging")
    add("free-cash-flow", "fcfYieldPct", lambda v: "supporting" if v > 0 else "challenging")
    add("revenue-growth", "revenueCagr3yPct", lambda v: "supporting" if v >= 5 else "review" if v >= 0 else "challenging")
    if snapshot.get("sector") == "Financial Services":
        out.append({"metric":"leverage", "value":"unavailable", "state":"unavailable"})
    else:
        add("leverage", "netDebtToEbitda", lambda v: "supporting" if v <= 1.5 else "review" if v <= 3 else "challenging", "x")
    p,v = num(snapshot.get("price")),num(snapshot.get("fairValue"))
    if not snapshot.get("hasValidFairValue") or p is None or v is None or p <= 0 or v <= 0 or old(snapshot.get("priceAsOf"),10,now) or old(snapshot.get("fairValueAsOf"),45,now):
        out.append({"metric":"margin-of-safety", "value":"unavailable", "state":"unavailable"})
    else:
        mos = (v-p)/v*100
        out.append({"metric":"margin-of-safety", "value":"%.1f%%" % mos, "state":"supporting" if mos>=20 else "review" if mos>=0 else "challenging"})
    return {"symbol":snapshot.get("symbol"),"signals":out,"not_affiliated":True,
            "unassessed":["moat", "management", "circle of competence"], "investment_advice":False}

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("snapshot", type=Path)
    ap.add_argument("--now", default=None)
    args=ap.parse_args()
    now=date(args.now) if args.now else None
    if args.now and now is None: ap.error("--now must be ISO-8601")
    with args.snapshot.open(encoding="utf-8") as f: data=json.load(f)
    if not isinstance(data,dict) or not isinstance(data.get("metrics"),dict): ap.error("Expected an object with metrics")
    print(json.dumps(screen(data,now),indent=2))
