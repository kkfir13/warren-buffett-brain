# Warren Buffett Brain

**Research a stock with Buffett-inspired discipline. Follow the actual Berkshire evidence.**

Warren Buffett Brain is an independent, open-source investment research library and AI skill. It helps you study historical Buffett decisions—and ask better questions about companies you research today.

[**Use Warren Buffett Brain in ChatGPT →**](CHATGPT.md) · [Download the Skills-only plugin](dist/warren-buffett-brain-chatgpt-plugin.zip) · [Download for eligible Personal Skills users](dist/warren-buffett-brain-personal-skill.zip) · [Explore the original case studies](https://kkfir13.github.io/warren-buffett-brain/cases/) · [Browse the source archive](https://kkfir13.github.io/warren-buffett-brain/) · [View the AI skill](skills/warren-buffett-brain/SKILL.md)

> **ChatGPT availability:** The Buffett Brain plugin package exists, but it is **not publicly listed** in the ChatGPT Plugins Directory yet. You can try the research prompt below in ChatGPT now; that does not install the plugin or automatically load its bundled reference files. The installable skill will be available to other users only after directory approval and publication.

## No hosted backend — the research travels with the skill

**No Supabase, no ValuEdge servers, no paid inference API, and no always-on backend are needed** for the Buffett Brain plugin. Its historical research notes and original case studies are packaged with the Skills-only ZIP. ChatGPT itself remains an online product; "offline" here means **no dedicated server for the plugin**, not that ChatGPT works without an internet connection.

Advanced desktop MCP users can instead use the [local stdio MCP](local-mcp/README.md), which runs on their own device using Python and needs no hosting. A remote MCP is **not** included in the main ZIP.

## Try it in ChatGPT right now — no installation

Open [ChatGPT](https://chatgpt.com/) and paste this prompt, replacing the company or ticker:

```text
Research [COMPANY OR TICKER] using Warren Buffett-inspired value-investing principles. Explain how the business earns money, the evidence for or against a durable competitive moat, management's capital allocation, cash-flow quality, debt and the strongest bear case.

Separate business quality from the price I'd pay. Use dated primary filings and cite your sources. If reliable current prices or valuation inputs are unavailable, say so instead of inventing numbers. Distinguish documented Buffett history from your own interpretation; don't pretend Buffett has endorsed the stock.

Finish with the three most important facts I should verify next.
```

This works as an **ordinary ChatGPT research prompt**. The Buffett Brain plugin, when installed in a supported ChatGPT environment, adds a packaged collection of independently written historical evidence notes and case studies.

## What can you ask?

| Your question | What the research should examine |
| --- | --- |
| **Why did Buffett invest in GEICO?** | His early investigation, GEICO's crisis, management and underwriting risks |
| **What did See's Candies teach Buffett?** | Economic goodwill, pricing power and incremental capital requirements |
| **Analyze Microsoft like a business owner.** | Moat evidence, returns on capital, cash flows, debt, valuation assumptions and risks |
| **Where did Buffett get it wrong?** | Dexter Shoe, General Re and the economic cost of issuing Berkshire stock |
| **Is this stock a good business at a good price?** | A business-quality checklist *separately* from dated valuation evidence |

[Explore eight full investment case studies](https://kkfir13.github.io/warren-buffett-brain/cases/) · [Read the source-linked evidence index](knowledge/atlas.json)

## A great business is not always a great price

Buffett Brain helps you understand **the business, its moat, cash generation and risks**. But knowing that a company is high quality does not tell you whether the **price you would pay leaves a margin of safety**.

**[Continue the research in ValuEdge](https://valuedge.app/?utm_source=buffett_brain&utm_medium=github&utm_campaign=research_next_step)**: examine model-based intrinsic value, challenge valuation assumptions, and follow the gap between price and estimated value. ValuEdge is a separate research product operated by the maintainer of Buffett Brain.

If you have a specific goal, you can go directly to the [Intrinsic Value Screener](https://valuedge.app/features/intrinsic-value/screener?utm_source=buffett_brain&utm_medium=github&utm_campaign=research_next_step), [Fair Value Watchlist](https://valuedge.app/features/fair-value-watchlist?utm_source=buffett_brain&utm_medium=github&utm_campaign=research_next_step), or [Smart Alerts](https://valuedge.app/features/smart-alerts?utm_source=buffett_brain&utm_medium=github&utm_campaign=research_next_step).

**Optional, not a dependency:** Buffett Brain's original research stays free and useful without ValuEdge. Valuation models have limitations; never treat an estimated fair value as Buffett's personal view or as a trading instruction.

## What is included in the open-source project?

- **55** original historical research notes across Berkshire decisions, investing principles, mistakes, books and brief attributed statements.
- **60** external source links, including the official Berkshire shareholder-letter archive covering 1977–2024. *Links are not complete copies of the letters or evidence that every letter has been fully reviewed.*
- **Eight** original source-linked investment case studies, from GEICO and See's Candies to Goldman Sachs, BNSF and admitted errors.
- A zero-hosting [local MCP desktop adapter](local-mcp/README.md), plus a self-hostable [research website](https://kkfir13.github.io/warren-buffett-brain/), [ChatGPT-ready skill](skills/warren-buffett-brain/SKILL.md), offline search tool, documented methodology and unit tests.

**Independent project:** not affiliated with, endorsed by or operated by Warren Buffett or Berkshire Hathaway. Benjamin Graham wrote *The Intelligent Investor*; Charlie Munger and Alice Schroeder have distinct works and views. Original content and code are MIT-licensed; books, letters, transcripts and other third-party materials retain their rights. Educational research only, not investment advice.

## Open source means you can inspect and improve it

Browse [the original evidence](knowledge/atlas.json), [case studies](deep-dives/), [research methodology](references/methodology.md) or [contribute a documented correction](CONTRIBUTING.md).

For maintainers, publication steps, plugin packaging, GitHub Pages and Search Console live in [MAINTAINER.md](docs/MAINTAINER.md)—not in the end-user getting-started guide.
