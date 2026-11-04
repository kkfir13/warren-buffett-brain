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

The [Buffett Brain plugin package](dist/warren-buffett-brain-chatgpt-plugin.zip) is a **Skills-only** archive with its historical research corpus bundled. It does **not** connect to a remote MCP endpoint or consume ValuEdge infrastructure. It currently exists as a **private plugin**, not a publicly installable listing.

**After directory review and publication**, users with eligible access can open ChatGPT's **Plugins** directory, search for **Warren Buffett Brain**, review it, and install it. A public install link will be added here only after it is confirmed.

The skill adds a disciplined framework and bundled historical notes. It does **not** provide live securities prices, trade execution or access to personal accounts.

## Option 2b — Import as a Personal Skill on eligible ChatGPT accounts

Eligible ChatGPT Business, Enterprise, Healthcare and Edu accounts with Personal Skills enabled can use the research bundle **without waiting for universal Plugins Directory publication**. This is a manual import per person or workspace, not a one-click public plugin installation.

1. Download the [Warren Buffett Brain Personal Skill ZIP](dist/warren-buffett-brain-personal-skill.zip).
2. Open ChatGPT → **Plugins** → **Skills** → **Create** → **Upload from your computer**.
3. Select that ZIP and follow the safety review/installation prompts. If your account does not show Skills or Upload, this route is not available to your account.
4. In ChatGPT, ask: **"Use Warren Buffett Brain to explain Berkshire's GEICO investment and cite the historical evidence."**

**Do not upload the plugin ZIP in this Skills uploader**; it is a separate format with `plugin.json`. The Personal Skill ZIP contains one `warren-buffett-brain/` folder with `SKILL.md` and its bundled `references/`. Neither path connects to ValuEdge, Supabase or a remote MCP server.

See the [OpenAI Help Center — Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/) for plan/role requirements.

## Option 3 — Use offline MCP on a compatible desktop client

Users who want an MCP server rather than the ChatGPT plugin can use the [local no-hosting MCP adapter](local-mcp/README.md). This is an **advanced desktop setup**, not an automatically available ChatGPT web connection. It runs from the open-source repository with Python and the user's own machine, at no ongoing hosting cost.

**Important:** The former experimental public endpoint on a ValuEdge Supabase project was decommissioned; do not try to connect to it.

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
