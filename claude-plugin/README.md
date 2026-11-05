# Warren Buffett Brain

**Source-linked Buffett and Berkshire research, with optional ValuEdge stock tools in Claude.**

Warren Buffett Brain is an independent open-source research assistant for documented Berkshire Hathaway investment decisions, business quality, competitive moats, owner-like cash flow, stewardship, and the difference between a good business and an attractively priced share.

The plugin bundles **55 independently written historical research notes**, **60 links to original source materials** and **eight original detailed case studies**. Historical links are not complete copies of copyrighted shareholder letters, books or meeting recordings. Facts, interpretation and uncertainty must remain distinct.

## What this plugin provides

- A reproducible Buffett-inspired research process and source-linked historical research on Berkshire's decisions and mistakes.
- Research on a company's economic moat, cash generation, management, valuation uncertainty, and strongest counterarguments.
- An **optional ValuEdge remote MCP connector** for public stock fundamentals, model-based fair values, comparisons and bounded screening. Its data may be dated, incomplete, or subject to coverage limitations.
- When the user deliberately connects their own authorized ValuEdge account and has an eligible subscription, tools to read their own portfolio, watchlist and alerts. The connector is read-only and cannot place trades.

## Connect ValuEdge (optional)

This plugin declares the HTTPS MCP endpoint at https://valuedge.app/mcp. On claude.ai and in Cowork, add or connect the server from the plugin's Connectors tab; Claude Code can connect to the declared endpoint when the plugin is enabled. Public stock research tools can work without a ValuEdge account. Private account tools require explicit authorization. No private token or credential is included in this repository.

Historical research works without a live MCP connection. When a ValuEdge tool is called, the server receives relevant ticker symbols, comparison inputs or screening terms; with your authorization and explicit request it may also return personal account research. See the project's [privacy](https://kkfir13.github.io/warren-buffett-brain/privacy/) and [terms](https://kkfir13.github.io/warren-buffett-brain/terms/).

## Try these prompts

- "What did Buffett learn from See's Candies? Use original sources."
- "Analyze Alphabet's moat, then retrieve ValuEdge's dated valuation assumptions."
- "Find five potentially undervalued quality stocks using ValuEdge; disclose screening limitations."
- "Compare KO versus PEP's cash flow, financial risk and fair-value models."

## Independence and support

This project is **not affiliated with or endorsed by Warren Buffett or Berkshire Hathaway**, does not impersonate Buffett and does not give personalized buy/sell recommendations. ValuEdge is a separate commercial service operated by the same maintainer, Kfir Aharon. Its model values are not Buffett's personal estimates.

Source and support: https://github.com/kkfir13/warren-buffett-brain · License: MIT for original project content, excluding linked third-party materials.
