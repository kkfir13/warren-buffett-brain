# Buffett Brain 🧠
## Open-source Warren Buffett investing research — original sources, not mythology

**Buffett Brain is an independent, fully self-hostable research project** about Berkshire Hathaway, Warren Buffett's investing principles, historic deals, capital allocation, economic moats, mistakes, shareholder letters, and the influence of Benjamin Graham and Charlie Munger.

**Verified baseline:** 60 linked sources, 55 original evidence notes, 8 long-form transaction case studies, and four brief attributed quotations. The primary-source index covers links to official Berkshire shareholder letters for 1977–2024 plus SEC filings, CNBC's licensed meetings archive, and relevant book catalogs. **A linked letter is not a claim its entire contents have been reviewed.** All research can be used without a ValuEdge subscription.

## Live website and search indexing

The project also has a static website on GitHub Pages: [Warren Buffett Brain](https://kkfir13.github.io/warren-buffett-brain/). It contains a full-text local evidence explorer and **eight separate HTML research case studies**, with unique page titles, original references, canonical URLs, structured Article data and a [10-URL sitemap](https://kkfir13.github.io/warren-buffett-brain/sitemap.xml). All articles are independently written and linked to primary sources; no copyrighted source texts are mirrored.

After GitHub Pages publishes a commit, use [Google Search Console](https://search.google.com/search-console) to verify the URL-prefix property `https://kkfir13.github.io/warren-buffett-brain/`, submit the `sitemap.xml` URL and inspect/request indexing for the homepage. Google decides whether to crawl and index the site; publishing or submitting does not guarantee rankings.

## Remote MCP server (public endpoint requires deployment)

The source for a public, read-only **MCP Streamable HTTP server** is now in [mcp/](mcp/). It exposes evidence search, record fetch and research coverage without private accounts, live stock data or paid AI inference. **It has not yet been deployed to a public HTTPS host**, so there is currently no working URL to give other users. See the [deployment and testing guide](mcp/README.md). GitHub Pages hosts the separate static research website, not MCP requests.

## Use Warren Buffett Brain with ChatGPT

**No localhost setup is required for end users.** This repository now includes a packaged, self-contained **skills-only ChatGPT Plugin** with source-linked research and a repeatable analysis workflow. See the [ChatGPT integration and publication guide](CHATGPT.md).

**Publication status:** An open-source GitHub repository is not automatically a ChatGPT plugin. The package must pass OpenAI's review and be explicitly published in its Plugins Directory before a public install link can work. Do not confuse the public [research website](https://kkfir13.github.io/warren-buffett-brain/) with a ChatGPT plugin listing.

The [ready-to-submit plugin ZIP](dist/warren-buffett-brain-chatgpt-plugin.zip) is included; developers can also rebuild it with `python3 scripts/build_chatgpt_plugin.py`; the standalone skill and its offline reference corpus live under [skills/warren-buffett-brain/](skills/warren-buffett-brain/).

## Run locally (developers only)

This section is **only** for previewing the static website on your own computer. Requires Python 3 and a browser; no cloud AI, credentials, npm install, paid API or account.

```bash
git clone https://github.com/kkfir13/warren-buffett-brain.git buffett-brain
cd buffett-brain
python3 -m http.server 8000
```

**On the computer running the server**, visit **http://localhost:8000/** and search: `See's Candies`, `GEICO`, `Dexter Shoe`, `Goldman Sachs 2008`, `circle of competence` or `Benjamin Graham`.

### AI research instructions

The root [SKILL.md](SKILL.md) documents the original offline research workflow. The **ChatGPT-compatible package** uses [skills/warren-buffett-brain/SKILL.md](skills/warren-buffett-brain/SKILL.md) and **bundled sources** so end users don't need to run Python. Both are independent Buffett-inspired research methods, not an official Buffett persona.

### Offline research commands

```bash
python3 scripts/search_knowledge.py "GEICO turnaround" --limit 5
python3 scripts/search_knowledge.py "Dexter Shoe" --kind mistake
python3 scripts/search_knowledge.py "Buffett's statements" --kind statement
python3 scripts/validate_knowledge.py
python3 -m unittest discover -s tests -v
node --check app.js
```

## Project structure

- **[index.html](index.html), [app.js](app.js), [styles.css](styles.css):** responsive static research website suitable for basic GitHub Pages hosting.
- **[knowledge/atlas.json](knowledge/atlas.json):** machine-readable, externally sourced research registry.
- **[deep-dives/](deep-dives/):** historically grounded case studies for See's, GEICO, Coca-Cola, General Re/Dexter, Goldman, BNSF, Graham/Munger and the textiles/insurance pivot.
- **[SKILL.md](SKILL.md):** original offline research instructions; **[skills/warren-buffett-brain/](skills/warren-buffett-brain/):** ChatGPT plugin skill with bundled research.
- **[plugin.json](plugin.json), [CHATGPT.md](CHATGPT.md):** portable plugin manifest and verified publication guidance.
- **[scripts/build_chatgpt_plugin.py](scripts/build_chatgpt_plugin.py):** repeatable source sync and submission-ZIP builder.
- **[scripts/](scripts/), [tests/](tests/):** local search, research integrity, offline quantitative screening, unit tests.
- **[knowledge/README.md](knowledge/README.md):** source rights, attribution and expansion policies.

## Primary sources

[Berkshire Hathaway shareholder letters](https://www.berkshirehathaway.com/letters/letters.html) · [1996 Owner's Manual](https://www.berkshirehathaway.com/1996ar/manual.html) · [CNBC Warren Buffett Archive](https://buffett.cnbc.com/) · SEC regulatory filings.

The project does **not** reproduce complete copyrighted books, letters or video transcripts. The Intelligent Investor was written by **Benjamin Graham**, and Poor Charlie's Almanack centers on **Charlie Munger**. Historical context is attributed precisely.

## Contributing, license and relationship to ValuEdge

Open source under the [MIT license](LICENSE) for the code and original content (not third-party sources or trademarks). Contributions of verifiable case studies, exact section/page locators and corrections are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md) and [the ongoing evidence backlog](https://github.com/kkfir13/warren-buffett-brain/issues).

ValuEdge offers an **optional** separate [stock valuation research tool](https://valuedge.app/buffett). No ValuEdge account is required for Buffett Brain's code, website, agent skill or offline analyses.

**Independent, not endorsed by or affiliated with Warren Buffett or Berkshire Hathaway. Research and education, not investment advice.**

## GitHub Topics and Google discoverability

GitHub repository description: *Open-source Warren Buffett & Berkshire Hathaway research: shareholder letters, historical investment decisions, value investing principles, mistakes and a source-linked AI agent skill.*

Recommended GitHub Topics: `buffett-principles`, `warren-buffett`, `buffett`, `value-investing`, `berkshire-hathaway`, `shareholder-letters`, `investment-research`, `ai-skills`, `agent-skills`.

**Repository status:** Open-source research and plugin package are public; public ChatGPT plugin installation remains subject to OpenAI review and publication. GitHub Pages is a separate static website.
