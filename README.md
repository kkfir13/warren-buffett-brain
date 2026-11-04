# Buffett Brain 🧠
## Open-source Warren Buffett investing research — original sources, not mythology

**Buffett Brain is an independent, fully self-hostable research project** about Berkshire Hathaway, Warren Buffett's investing principles, historic deals, capital allocation, economic moats, mistakes, shareholder letters, and the influence of Benjamin Graham and Charlie Munger.

**Verified baseline:** 60 linked sources, 55 original evidence notes, 8 long-form transaction case studies, and four brief attributed quotations. The primary-source index covers links to official Berkshire shareholder letters for 1977–2024 plus SEC filings, CNBC's licensed meetings archive, and relevant book catalogs. **A linked letter is not a claim its entire contents have been reviewed.** All research can be used without a ValuEdge subscription.

## Run the research website

Requires Python 3 and a browser; no cloud AI, credentials, npm install, paid API or account.

```bash
git clone https://github.com/kkfir13/warren-buffett-brain.git buffett-brain
cd buffett-brain
python3 -m http.server 8000
```

Visit **http://localhost:8000/** and search: `See's Candies`, `GEICO`, `Dexter Shoe`, `Goldman Sachs 2008`, `circle of competence` or `Benjamin Graham`.

### Install the AI skill

[SKILL.md](SKILL.md) is a portable Agent Skills instruction file for Claude Code, Codex, and compatible assistants. It searches the local evidence registry, demands primary-source citations, distinguishes factual history from our commentary, and refuses to fabricate Buffett opinions. It is not an official Buffett persona.

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
- **[SKILL.md](SKILL.md):** research instructions for compatible AI agents.
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

**Repository status:** This is the independent, public Warren Buffett Brain source repository. After GitHub Pages is enabled, the project can also be explored in a browser without cloning.
