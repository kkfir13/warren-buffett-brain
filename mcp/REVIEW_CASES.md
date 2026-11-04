# Public MCP review examples (draft)

Use these while submitting a **new With MCP** plugin for a verified, live endpoint. Replace expected tool names if metadata changes before final submission. These cases are documentation, not a substitute for portal testing.

## Positive (must use at least one MCP tool)

1. **Prompt:** "What did Warren Buffett learn from See's Candies?" **Tools:** `search`, `fetch`. **Expected:** Berkshire history, the source link, and clearly labeled interpretation.
2. **Prompt:** "Explain the timeline of Berkshire's GEICO investment." **Tools:** `search`, `fetch`. **Expected:** Historical evidence with years, original source URLs and explicit limitations.
3. **Prompt:** "Which Buffett mistakes are documented in the project's notes?" **Tools:** `search`, `fetch`. **Expected:** Attributed mistakes, distinguished from the researcher's conclusions.
4. **Prompt:** "What historical sources does Buffett Brain cover?" **Tools:** `research_overview`. **Expected:** Counts, coverage limitations and no claim that complete books or letters were ingested.
5. **Prompt:** "What do Buffett's Berkshire letters say about the BNSF acquisition?" **Tools:** `search`, `fetch`. **Expected:** Source-linked notes on the deal, no invented verbatim quotes.

## Negative (MCP must not be used for an unsupported operation)

1. **Prompt:** "Buy $1,000 of BRK.B in my brokerage account." **Expected:** No tool for trading; do not claim an order was placed.
2. **Prompt:** "Show me my private brokerage holdings." **Expected:** No private portfolio access, no account linking or fabricated holdings.
3. **Prompt:** "Give me the live price of NVIDIA to the second." **Expected:** Explain this research MCP has no live market-price feed; do not make up a price.

The project is independent of Warren Buffett and Berkshire Hathaway, and has no endorsement or personal Buffett persona.
