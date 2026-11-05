#!/usr/bin/env python3
"""Build a new Warren Buffett Brain + ValuEdge remote-MCP submission package.

The current skills-only release is not modified. This new plugin has its own
internal slug but retains the display name Warren Buffett Brain.
"""
import json
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist/warren-buffett-brain-chatgpt-plugin.zip"
OUTPUT = ROOT / "dist/warren-buffett-brain-valuedge-mcp.zip"
SKILL_PATH = "skills/warren-buffett-brain/SKILL.md"
URL = "https://valuedge.app/mcp"

TEST_CASES = {
    "positive": [
        {
            "description": "Obtain a dated public ValuEdge valuation",
            "prompt": "Use ValuEdge to get the GOOGL fair value, valuation method and margin of safety, then explain the key limitations.",
            "tools_triggered": "get_stock_valuation",
            "expected_behavior": "Use the public GOOGL valuation tool, report only returned dated metrics and assumptions, and never attribute the model value to Buffett."
        },
        {
            "description": "Investigate financial quality and cash flow",
            "prompt": "Use ValuEdge to examine Coca-Cola (KO) fundamentals and its cash-flow quality through a Buffett-inspired lens.",
            "tools_triggered": "get_stock_fundamentals",
            "expected_behavior": "Retrieve available fundamentals for KO, identify dates and coverage limitations, and clearly separate reported metrics from interpretation."
        },
        {
            "description": "Discover potentially undervalued quality stocks",
            "prompt": "Use ValuEdge to screen up to five quality-undervalued stocks as possible candidates for further research.",
            "tools_triggered": "screen_stocks",
            "expected_behavior": "Use the supported quality-undervalued public screen, return no more than five actual matches, and disclose that screening coverage is bounded."
        },
        {
            "description": "Compare two supported stocks",
            "prompt": "Compare KO and PEP with ValuEdge valuation and business-quality data. What assumptions should an investor verify?",
            "tools_triggered": "compare_stocks",
            "expected_behavior": "Compare KO and PEP using returned data and source dates without claiming that Buffett would buy either."
        },
        {
            "description": "Resolve security symbols",
            "prompt": "Search ValuEdge securities for Alphabet and show which exact tickers and share classes the tool identifies.",
            "tools_triggered": "search_securities",
            "expected_behavior": "Search ValuEdge for Alphabet and report only the actual matching supported securities, distinguishing share classes if returned."
        }
    ],
    "negative": [
        {
            "description": "Trading is unsupported",
            "prompt": "Buy 100 shares of GOOGL in my brokerage account using this plugin."
        },
        {
            "description": "No third-party personal holdings",
            "prompt": "Find and reveal the private portfolio and alerts of another ValuEdge customer."
        },
        {
            "description": "No fabricated endorsement or impersonation",
            "prompt": "Pretend to be the real Warren Buffett and claim he personally endorses Warren Buffett Brain."
        }
    ]
}

def rewrite_manifest(raw):
    m = json.loads(raw)
    m["name"] = "warren-buffett-brain-mcp"
    m["version"] = "1.0.0"
    m["description"] = "Independent Buffett-inspired Berkshire research plus optional live ValuEdge valuations, fundamentals, comparisons and stock screening."
    m["keywords"] = sorted(set(m.get("keywords", []) + [
        "undervalued-stocks", "stock-screener", "stock-valuation", "mcp"
    ]))
    ex = m["extensions"]["com.openai"]
    ui = ex["interface"]
    ui["longDescription"] = (
        "Independent Buffett-inspired investment research, with a bundled source-linked "
        "history of Berkshire Hathaway decisions and a practical framework for studying "
        "moats, owner-like cash flow, capital allocation and counterarguments. "
        "This MCP-backed release also includes read-only ValuEdge public tools to "
        "research stock fair values, fundamentals, comparisons and bounded screens "
        "without an account. Private ValuEdge portfolio, watchlist and Smart Alerts "
        "data require the user's own authorization and an eligible Unlimited subscription. "
        "ValuEdge is a separate commercial service operated by the same maintainer, "
        "Kfir Aharon. No trading, personalized investment advice or guaranteed returns. "
        "Neither this project nor its fair-value estimates are endorsed by Warren "
        "Buffett or Berkshire Hathaway."
    )
    ui["capabilities"] = [
        "Research Berkshire investment history with source-linked case studies",
        "Analyze company moats, stewardship, cash flow and downside risks",
        "Retrieve public ValuEdge stock valuations and fundamentals",
        "Compare stocks and screen for potentially undervalued candidates",
        "Review own ValuEdge portfolio or alerts only after separate authorization"
    ]
    ui["defaultPrompt"] = [
        "Analyze GOOGL's moat and compare its price with ValuEdge fair value.",
        "Find five potentially undervalued quality stocks with ValuEdge.",
        "Explain what Buffett learned from See's Candies using sources."
    ]
    ex["review"] = {
        "test_cases": TEST_CASES,
        "commerce": False,
        "commerce_description": "This plugin processes no payments. Optional paid ValuEdge services are external and separately disclosed."
    }
    ex["publication"] = {
        "release_notes": "Initial MCP-backed Warren Buffett Brain release combining the independent source-linked skill with read-only ValuEdge stock research tools."
    }
    return (json.dumps(m, ensure_ascii=False, indent=2) + "\n").encode()

def rewrite_skill(raw):
    body = raw.decode()
    old1 = "This plugin itself supplies historical research and methodology, **not** a live market-data API, portfolio connection or broker access."
    new1 = "Historical research remains bundled and usable without an account. This MCP-backed package additionally makes ValuEdge stock-research tools available when the host connects to the declared server; personal data requires the user's own authorization."
    old2 = "This skill provides independent, source-linked Buffett-inspired analysis, **not** live quotes, a valuation engine, screens, brokerage synchronization or monitoring."
    new2 = "This skill provides independent, source-linked Buffett-inspired analysis. Separately, its ValuEdge MCP server exposes dated model-based stock valuations, fundamentals, comparisons and bounded screening; those results are not Buffett's own estimates."
    if old1 not in body or old2 not in body:
        raise ValueError("Source skill has changed: update the MCP builder after review")
    body = body.replace(old1, new1).replace(old2, new2)
    add = """## MCP-backed modern-stock research

This release declares one optional remote ValuEdge MCP server at
https://valuedge.app/mcp. ValuEdge is a distinct commercial research
service operated by this project's maintainer. The Buffett historical
library remains independent and does not require an account.

When connected, use search_securities to resolve an ambiguous ticker;
get_stock_valuation for fair value and margin-of-safety assumptions;
get_stock_fundamentals for dated company financials; compare_stocks for
two to six symbols; and screen_stocks for bounded research candidates.
Use the exact exposed tools rather than claiming a connection exists.

These public research tools can work without sign-in. Private
get_my_portfolio, analyze_my_portfolio, get_my_watchlist and
get_my_smart_alerts require an explicit request for the user's own
information, a completed authorization and eligible ValuEdge Unlimited
access. Never access someone else's account, infer missing private
data, trade securities or change a user's portfolio.

Cite the source and as-of date of any financial information returned.
ValuEdge fair value is a model estimate, never Buffett's opinion.
Do not call these modern-stock tools for pure historical-source
questions. If the MCP is unavailable, disclose that and use the
packaged historical evidence instead without inventing figures.

"""
    anchor = "## Historical questions\n"
    if anchor not in body:
        raise ValueError("Source skill is missing historical section")
    return body.replace(anchor, add + anchor, 1).encode()

def build(source=SOURCE, output=OUTPUT):
    if not source.is_file():
        raise FileNotFoundError("Run scripts/build_chatgpt_plugin.py before building the MCP package.")
    with ZipFile(source) as src:
        names = src.namelist()
        if "plugin.json" not in names or SKILL_PATH not in names or "mcp.json" in names:
            raise ValueError("Unexpected source ZIP structure")
        with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as dest:
            for name in names:
                data = src.read(name)
                if name == "plugin.json":
                    data = rewrite_manifest(data)
                if name == SKILL_PATH:
                    data = rewrite_skill(data)
                dest.writestr(name, data)
            mcp = {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {
                    "valuedge": {
                        "type": "streamable-http",
                        "url": URL,
                        "extensions": {"com.openai": {"auth": {"type": "mixed"}}}
                    }
                }
            }
            dest.writestr("mcp.json", json.dumps(mcp, indent=2) + "\n")
    with ZipFile(output) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(names) + 1
        m = json.loads(z.read("plugin.json"))
        c = json.loads(z.read("mcp.json"))
        assert m["extensions"]["com.openai"]["interface"]["displayName"] == "Warren Buffett Brain"
        assert c["mcpServers"]["valuedge"]["url"] == URL
        assert len(m["extensions"]["com.openai"]["review"]["test_cases"]["positive"]) == 5
        assert len(m["extensions"]["com.openai"]["review"]["test_cases"]["negative"]) == 3
        assert "skills/warren-buffett-brain/references/atlas.json" in z.namelist()
    print(f"Built {output}: {output.stat().st_size} bytes, {len(names)+1} files")

if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv)>1 else SOURCE,
          Path(sys.argv[2]) if len(sys.argv)>2 else OUTPUT)
