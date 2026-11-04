# Buffett Brain source and rights policy

The JSON atlas is a **source directory plus a curated selection** of original short analyses. It is not a corpus of extracted copyrighted books or transcripts, and it is not yet an exhaustive annotated record of Buffett's life.

- Official Berkshire shareholder letters for reporting years 1977–2024 are indexed via the [Berkshire letter index](https://www.berkshirehathaway.com/letters/letters.html). The original documents remain on Berkshire's website.
- Meetings and interviews are indexed via [CNBC's authorized Warren Buffett Archive](https://buffett.cnbc.com/warren-buffett-archive/), with an indexed annual-meeting range of 1994–2026 as reported by CNBC at collection time. We don't reproduce CNBC video or transcripts.
- Contemporary corporate press releases and SEC filings are the first choice for the exact terms of deals. Buffett's later letters are separately used for his retrospective interpretation and known mistakes.
- Book references distinguish Buffett's original words, Graham's teachings, Munger's mental models, Cunningham's editing and Schroeder's biography. Books are link-only.
- Each curated entry is original paraphrase, with `evidence` (what sources establish), `interpretation` (what researchers can learn), and `limitations` (what cannot be concluded).
- Never claim Buffett endorsed the project. Don't generate speeches impersonating Buffett or assert he'd buy a present-day stock.
- No verbatim ingestion of books, letters, speeches or transcripts without a separate permission audit. Commercial usage and distribution licenses for third-party content are not granted by their public availability.
- Contributors can add short factual summaries with exact source IDs, document locators, contradictory evidence, dates and clear attribution. Verified authorship and original-source links are mandatory.

## Coverage strategy

1. **Source registry**: stable IDs, years, official links and explicit rights boundary.
2. **Evidence entries**: original summaries of confirmed historical cases and ideas, including errors and counterexamples.
3. **Retrieval**: deterministic local search, returning document IDs and clickable original-source links. No LLM hallucinations or background scraping.
4. **Review backlog**: deeper annotation of each yearly letter, annual meeting and major business acquisition is still needed. A source link is not proof every passage has been read.
5. **Open-core**: software and written summaries are MIT-licensed; ValuEdge price feeds, private finance, user accounts, paid API entitlements and the valuation engine are not licensed into this repository.

### Contributing a new entry

Include `id`, `kind`, `year`, `title`, `summary`, `evidence`, `interpretation`, `limitations`, `sourceIds`, `topics`, `companies`, `locator`, `verification`, and `rights`. Use short original prose, not copied paragraphs. Source IDs must already exist in `sources`. Do not label a case as an investment success without period-specific outcome evidence. Run the validator and tests before opening a pull request.

The website uses a versioned copy of this atlas in `public/buffett/atlas.json`; update it from this public file when publishing changes, then check byte equality.

## Detailed long-form case studies

Eight case studies live in `deep-dives/`. They are original educational analysis, not primary transcripts. The `deepDivePath` field identifies them from the searchable atlas. Each has direct historical source references and distinguishes transaction evidence, an interpretive framework and what remains unknown.
