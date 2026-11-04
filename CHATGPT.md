# Use Warren Buffett Brain with ChatGPT

Warren Buffett Brain is a **free, independent source-linked investment research project**. There are several ways to use it, depending on whether you only want the research approach or want an AI assistant to read the actual historical notes.

## Option 1: Try the method in ChatGPT now

This is the easiest option and works **without installing this project**.

1. Open [ChatGPT](https://chatgpt.com/).
2. Copy the prompt below and replace the company or ticker.
3. If you need recent figures, ask ChatGPT to verify them using current filings and dated sources.

```text
Research [COMPANY / TICKER] as a long-term business owner using Buffett-inspired investing principles.

First, explain the business and the evidence for or against a durable competitive moat. Then examine management's capital allocation, free cash flow after necessary reinvestment, debt and downside resilience. Separate business quality from valuation; if you use a fair-value model, show its dated inputs, assumptions and uncertainty.

Use current primary filings for financial claims. Distinguish facts, inferences and unknowns. Show the strongest counter-thesis and three questions to verify next. Do not invent current quotes, exact Buffett statements or a claim that Buffett endorses the security.
```

Useful follow-ups: **"What evidence would disprove the moat?"**, **"What capital expenditures are required just to maintain this business?"**, or **"Show the bear case using the most recent annual filing."**

**What this does not do:** the prompt is not a plugin installation. It **does not** automatically read `knowledge/atlas.json`, the eight case studies or any other GitHub file. ChatGPT answers using only the material and tools actually available in that conversation. To use the project's evidence, provide files or give an assistant with repository access the instructions in [AGENTS.md](AGENTS.md).

## Option 2: Import the research Skill if your account supports it

ChatGPT Personal Skills are generally available to eligible **Business, Enterprise, Healthcare and Edu** accounts, depending on workspace permissions and supported surface. Availability differs by account; do not assume this menu appears for everyone. See the official [Skills in ChatGPT help article](https://help.openai.com/en/articles/20001066-skills-in-chatgpt/).

1. Download the [Warren Buffett Brain Personal Skill ZIP](dist/warren-buffett-brain-personal-skill.zip).
2. In a supported ChatGPT workspace, open **Plugins → Skills → Create → Upload from your computer**.
3. Upload that **Personal Skill ZIP**, review the safety prompts and install it.
4. Ask: **"Use Warren Buffett Brain to explain the See's Candies acquisition and distinguish historical evidence from interpretation."**

This is a real bundled Skill containing historical research notes, source links and case studies. The assistant can use the bundle **after successful installation** in a supported environment; its ability to independently open external sources depends on the tools available there.

**Do not upload the plugin ZIP** (`dist/warren-buffett-brain-chatgpt-plugin.zip`) into the Personal Skills uploader. That ZIP has `plugin.json` and is a different distribution format. Neither ZIP connects to a brokerage account, ValuEdge, a remote MCP or a live market-price feed.

## Option 3: Public plugin availability

Warren Buffett Brain is **not publicly listed** in ChatGPT's Plugins Directory as of the last repository update. The [Skills-only plugin package](dist/warren-buffett-brain-chatgpt-plugin.zip) exists, but a ZIP on GitHub is **not** an approved, installable public listing. Do not assume the project has an OpenAI-verified badge or a public one-click installation URL.

When an actual public listing is confirmed, this section can link to it. Until then, use the prompt above, an eligible Personal Skill import, or direct access to the open-source research.

## Option 4: Local MCP for compatible desktop clients

If your AI client supports **local stdio MCP**, you can run the [Python adapter](local-mcp/README.md) and retrieve source-linked notes with `search`, `fetch` and `research_overview`. This requires Python and a compatible desktop MCP client. It is **not** a public ChatGPT web/mobile connector.

The repository also contains an **optional self-hostable Cloudflare Worker reference** in [mcp/](mcp/README.md). Its source code is not proof that a public, working MCP endpoint is deployed. No public remote endpoint is included in the standard skill or plugin ZIP.

The prior experimental Buffett Brain MCP endpoint on ValuEdge's Supabase project was decommissioned; do not use or share it as a live connection.

## Questions that work well

- **History:** Why did Berkshire buy GEICO, and how did the investment evolve? Link original sources.
- **Moats:** What did See's Candies demonstrate about pricing power and economic goodwill?
- **Mistakes:** What went wrong with Dexter Shoe or General Re? Separate documented admissions from later interpretations.
- **A current stock:** Analyze GOOGL's competitive position and cash generation with **recent SEC filings**. State data dates.
- **Diligence:** What would have to be true for the investment thesis to fail?

For historical claims, a note in our index is a **secondary interpretation** unless the assistant has opened the original primary source. Sixty source links do not mean sixty full works were ingested or verified, and these notes are not a full-text archive of Berkshire letters or copyrighted books.

## Optional: research the price separately

Buffett Brain helps examine the **business**; it does not calculate live intrinsic value, track your portfolio or execute trades. If you want to examine a dated valuation model, [ValuEdge](https://valuedge.app/?utm_source=buffett_brain&utm_medium=github&utm_campaign=research_next_step) is an **optional, separate commercial product operated by this project's maintainer**. No ValuEdge account, integration or purchase is necessary to use Buffett Brain. Any value estimate depends on inputs and assumptions and is not Buffett's personal opinion.

Browse the [research website](https://kkfir13.github.io/warren-buffett-brain/), read [AGENTS.md](AGENTS.md) if you're using an assistant with repository access, or [open an issue](https://github.com/kkfir13/warren-buffett-brain/issues) if the setup is confusing.
