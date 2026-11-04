# Use Warren Buffett Brain inside ChatGPT

**You can start researching stocks today.** Buffett Brain is an independent, source-linked investment research project; it is not a chatbot impersonating Warren Buffett.

## Option 1 — Try the research workflow now

1. Open [ChatGPT](https://chatgpt.com/).
2. Copy this prompt and replace the ticker.

```text
Analyze [TICKER] as a long-term business owner using Buffett-inspired principles:
1. Explain the business model and its economics.
2. Investigate a possible moat, using evidence rather than brand reputation alone.
3. Evaluate management's capital allocation, owner-like cash generation, leverage and key risks.
4. Separate an excellent company from an attractively priced investment.
5. Show dated source links, explain unknowns and present the strongest counter-thesis.

Do not invent current market prices or Buffett quotes. Finish with the three most important due-diligence questions.
```

3. Ask follow-ups such as “What would break this investment thesis?”, “What are the key assumptions behind a fair-value estimate?” or “Show the opposite case.”

**Important:** A copied prompt is not an installed skill. ChatGPT will use the tools and information available in your conversation; it does **not** automatically ingest this repository's historical research corpus.

## Option 2 — Use the Buffett Brain skill when it becomes publicly available

The [Buffett Brain plugin package](dist/warren-buffett-brain-chatgpt-plugin.zip) includes a skills-only workflow and a curated source-linked reference set. It currently exists as a **private plugin**, not a publicly installable listing.

**After directory review and publication**, users with eligible access can open ChatGPT's **Plugins** directory, search for **Warren Buffett Brain**, review it, and install it. A public install link will be added here only after it is confirmed.

The skill adds a disciplined framework and bundled historical notes. It does **not** provide live securities prices, trade execution or access to personal accounts.

## Example questions

- “Why did Buffett first buy GEICO, and what could have gone wrong? Show the original letter.”
- “Explain See's Candies' economic goodwill in everyday language.”
- “Analyze GOOGL's competitive advantages and capital allocation with current SEC filings.”
- “Challenge the investment case for MSFT; show uncertainty and the bear thesis.”
- “How do Graham's and Munger's ideas differ from Buffett's recorded decisions?”

You can also [browse the research website](https://kkfir13.github.io/warren-buffett-brain/) without ChatGPT.

## Optional — add quantitative data with ValuEdge

The Buffett Brain skill is about **how to research**. If you want to follow that reasoning with current valuation estimates, margin of safety, stock screens or portfolio monitoring, [ValuEdge provides a separate, optional read-only MCP connection](https://valuedge.app/connect?utm_source=buffett_brain&utm_medium=github&utm_campaign=chatgpt_extension).

The ValuEdge connection is not installed by Buffett Brain. Public research tools do not require ValuEdge sign-in; accessing private portfolio, watchlist or alert data requires a supported plan and the user's authorization. The assistant must disclose the data source and its timestamps. You can decline this integration and still use Buffett Brain.

## How trustworthy are the answers?

The project currently links **60 sources** and includes **55 original research notes** and **eight longer studies**. Its source index is *not* a full-text archive of copyrighted Berkshire letters, interviews or books. An assistant should distinguish a note in the bundled corpus from a primary source it actually opened. Neither a mechanical score nor an AI answer is a statement of what Buffett personally would buy.

For developers and maintainers: see [the separate publication guide](docs/MAINTAINER.md).
