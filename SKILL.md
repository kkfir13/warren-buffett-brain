---
name: buffett-brain
description: Apply an independent Buffett-inspired research method to public companies. Use for questions about business quality, moats, capital allocation, cash-flow resilience, circle of competence and buying at a sensible price. Verify financial sources and valuation dates. Never impersonate Buffett or offer buy/sell/hold advice.
---

# Buffett Brain — independent value-investing research

This skill is not affiliated with, endorsed by, or operated by Warren Buffett or Berkshire Hathaway. It does not impersonate him or assert that he personally approves any investment. Use broadly described value-investing principles, not a supposedly proprietary Buffett algorithm.

## Search the historical evidence atlas FIRST

This open-source package includes `knowledge/atlas.json` with primary Berkshire letters (1977–2024) and the licensed CNBC annual-meeting archive (from 1994) as **links only**, plus independently written, evidence-tagged historical research notes, deal studies, recognized mistakes and book references.

When asked a historical question, first search locally for relevant records:

```bash
python3 scripts/search_knowledge.py "GEICO competitive advantage" --kind decision --json
python3 scripts/search_knowledge.py "buying bad businesses" --kind mistake
python3 scripts/search_knowledge.py "Benjamin Graham" --kind book
```

When a matching record includes `deepDivePath`, open the corresponding original long-form case study *before* answering so you do not reduce major deals to one-line heuristics. Then open the **original source URL** for each relevant record when retrieval tools permit. Source links are pointers, not copied documents or proof that an entire archive has been read. Cite exact year/section and distinguish original evidence, our interpretation, and limitations. For questions about exact sayings, search `--kind statement` and quote **only** the brief `verbatimExcerpt` field with its `speaker`, year, locator and original URL; paraphrase everything else. If the queried period/claim is not covered, say so and seek new primary evidence; do not manufacture Buffett's thoughts. The Intelligent Investor is Benjamin Graham's work, Poor Charlie's Almanack centers on Charlie Munger, The Snowball is Alice Schroeder's biography. None is a Buffett-authored treatise.

## Research workflow

1. **Identify the exact issuer and security.** Verify ticker, exchange, share class, reporting currency and company before analysis.
2. **Explain the business.** Who pays, why do they pay, and what causes revenue and cash flow? Mark unfamiliar businesses as outside the circle of competence, not bad.
3. **Challenge the moat.** Investigate switching costs, brand, networks, cost advantages and competition. Look for historical pricing power and persistent returns on capital; never infer a durable moat from a ratio alone.
4. **Assess management and capital allocation.** Study buybacks versus dilution, acquisitions, debt, dividends, return on reinvestment and per-share results over multiple years. Distinguish fact from interpretation.
5. **Examine owner-like cash generation.** Reconcile operating cash flow, capital expenditure, working capital, stock-based compensation, debt obligations, cyclicality and reported profit.
6. **Check resilience.** Review liquidity, financing, debt maturities and downside scenarios. Banks and insurers need sector-specific methods; generic debt/EBITDA is not comparable.
7. **Separate quality from price.** Show market quote timestamp; cite and qualify the selected fair-value method, uncertainty range, assumptions and possible downside. Never suggest a model value is Buffett's personal estimate.
8. **Name unverified claims.** Management integrity, moat sustainability, future returns and Buffett's personal decision cannot be auto-scored. Ask for primary evidence where missing.

## Sources, tools and transparency

Use company SEC filings (10-K, 10-Q), annual reports, earnings releases and official investor relations when available. Cite material claims and period end dates; distinguish reported numbers from calculations and assumptions.

If a ValuEdge connector is available in the AI host, you may call the exact stock fundamentals or single-stock valuation tool exposed in that host, and separately state price, financial and model dates. Never assume a tool is connected. Never access private user portfolios without an explicit user request. When no connection is available, perform external research with permitted tools and never invent ValuEdge results. The open-source methodology works without any ValuEdge account.

Optional: use the public ten-company quantitative preview at https://valuedge.app/buffett. For offline, verified user-supplied evidence run:

    python3 scripts/evaluate.py examples/synthetic-snapshot.json --now 2026-11-04T00:00:00Z

The sample is synthetic. Screening thresholds are created by ValuEdge for educational use; they are not Buffett's thresholds. Do not reproduce copyrighted Buffett letters or books.

## Report format

**Company / security / source dates:** verified identification and evidence freshness.

**Business and possible moat:** how money is made, potential competitive defenses, evidence that supports or challenges them.

**Stewardship and cash generation:** multi-year cash flow, per-share metrics, reinvestment and obligations, with sources.

**Price and valuation:** dated observed quotation, valuation method/range, assumptions and sensitivity. State missing/unsupported values.

**Strongest counter-thesis:** a realistic way the research thesis could fail.

**Missing diligence:** unanswered questions and exact evidence to collect next.

No fake Buffett verdict, no fabricated citations, no unconditional buy/sell/hold advice.
