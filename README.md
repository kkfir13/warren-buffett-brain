# Warren Buffett Brain

**Research businesses with a Buffett-inspired framework. Check the evidence, question the moat, and separate a good company from a good price.**

Warren Buffett Brain is a free, independent, open-source library of historical Berkshire Hathaway research and reusable instructions for AI assistants. It is **not** Warren Buffett's actual brain, an official Berkshire product, a live-stock-price feed, or an AI that knows what Buffett would buy today.

**[Start with ChatGPT](CHATGPT.md)** · [Browse the research website](https://kkfir13.github.io/warren-buffett-brain/) · [Read the eight case studies](deep-dives/) · [Instructions for AI agents](AGENTS.md)

## Try it in ChatGPT right now

You can copy this prompt into [ChatGPT](https://chatgpt.com/) today. No Warren Buffett Brain installation or account is needed **to try the methodology**:

```text
Analyze [COMPANY / TICKER] using Buffett-inspired value-investing principles.

Explain how the business earns money, the evidence for and against its moat, management's capital allocation, owner-like cash flow, debt and the strongest bear case. Separate the quality of the business from whether the current share price offers a margin of safety.

Use dated primary filings and show your sources. Separate reported facts, your interpretation and assumptions. Do not invent quotes, prices or fair values, and do not pretend Buffett endorses this stock. Finish with the three most important things to investigate next.
```

**Important:** this is a normal ChatGPT prompt, **not** an installed skill. Pasting it does not load this repository's historical notes. Ask your assistant to read the linked research files only if it actually has access to the repository or you provide the files.

## Choose how to use the project

| What you want | Available now? | Start here |
| --- | --- | --- |
| Ask ChatGPT to analyze a company using the framework | **Yes** — ordinary prompt, no installation | [Copy the prompt](CHATGPT.md#1-try-the-method-in-chatgpt-now) |
| Browse Buffett/Berkshire historical evidence and original case studies | **Yes** — public repository and website | [Research index](knowledge/atlas.json) · [Case studies](deep-dives/) |
| Have an AI agent use **this repository's actual files** | **Yes**, if that agent can read these files | [AI agent guide](AGENTS.md) |
| Import the historical research as a ChatGPT Personal Skill | **Eligible accounts/workspaces only** | [Import instructions](CHATGPT.md#2-import-the-research-skill-if-your-account-supports-it) |
| Connect a local MCP server from a desktop client | **Yes**, with Python and a compatible stdio MCP client | [Local MCP setup](local-mcp/README.md) |
| Install Warren Buffett Brain directly from the public ChatGPT Plugins Directory | **Not yet** — the plugin is not publicly listed | [Availability explained](CHATGPT.md#3-public-plugin-availability) |

The prebuilt [Skills-only plugin ZIP](dist/warren-buffett-brain-chatgpt-plugin.zip) is a *package for plugin distribution*, not a one-click public ChatGPT installation. The separate [Personal Skill ZIP](dist/warren-buffett-brain-personal-skill.zip) is for users whose ChatGPT workspace supports skill uploads. They are **different archive formats**; neither includes a hosted MCP connection.

## What's in the research library?

- **55** independently written notes about documented investing principles, Berkshire decisions, mistakes and historical context.
- **60** external source links, including the Berkshire shareholder-letter index. A link **does not** mean a whole letter, meeting recording or book was copied or reviewed.
- **Eight** original long-form case studies, including GEICO, See's Candies, Coca-Cola, Goldman Sachs, BNSF and Berkshire's mistakes.
- Source-linked research records with **evidence**, **interpretation**, **limitations** and a trail back to original publishers.
- An offline Python search script and optional local MCP tools: `search`, `fetch`, and `research_overview`.

Try questions like: **What did See's Candies reveal about pricing power?** / **What went wrong with Dexter Shoe?** / **Does GOOGL generate enough cash to justify the price I would pay?**

For the current stock's filings, quotes or valuation, the assistant needs **separate up-to-date sources**. This repository does not supply live prices, a proprietary Buffett valuation score, trading functionality or brokerage access.

## For AI assistants and developers

Read [AGENTS.md](AGENTS.md) for the correct order of research, what files are available, how to cite original sources, and how to report missing evidence. The packaged skill instructions are in [skills/warren-buffett-brain/SKILL.md](skills/warren-buffett-brain/SKILL.md).

You can search the historical index locally, without running an LLM or connecting to a service:

```bash
python3 scripts/search_knowledge.py "GEICO competitive advantage" --json
```

Python is for local scripts and the optional desktop MCP, **not** a requirement for reading the website or pasting the ChatGPT prompt.

## From business quality to valuation (optional)

Understanding a company's moat does not establish that the stock is cheap. **[Continue the research in ValuEdge](https://valuedge.app/?utm_source=buffett_brain&utm_medium=github&utm_campaign=research_next_step)** if you want to examine separate model-based valuations and assumptions. ValuEdge is a **separate commercial research product operated by this project's maintainer**; it is not needed to use Buffett Brain and its estimates are not Buffett's views.

## Trust, rights, and contributions

This project is not affiliated with, endorsed by or operated by Warren Buffett or Berkshire Hathaway. Its original code and research summaries are MIT-licensed. Third-party books, shareholder letters, recordings, photographs, brands and other materials remain with their rights holders; this project links to them instead of redistributing full texts.

For source standards and corrections, see [research and rights](knowledge/README.md), [contributing](CONTRIBUTING.md), [privacy](PRIVACY.md) and [terms](TERMS.md). Report missing or misattributed evidence through [GitHub Issues](https://github.com/kkfir13/warren-buffett-brain/issues).

Maintainer-only deployment and submission details are in [docs/MAINTAINER.md](docs/MAINTAINER.md), not required for ordinary use.
