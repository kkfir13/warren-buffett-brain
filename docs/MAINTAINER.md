# Maintainer operations — Warren Buffett Brain

This document is **for maintainers**, not a user installation guide. Keep GitHub Pages, Google Search Console, plugin package submission and CI operations here instead of placing them in the public README.

## Website / GitHub Pages and search indexing

Public website: https://kkfir13.github.io/warren-buffett-brain/

The static website consists of `index.html`, `app.js`, `styles.css`, `cases/**/index.html` and `sitemap.xml`. On GitHub Pages, publish from `main` at `/(root)`, then confirm the rendered URLs. To manage indexing, verify the exact URL-prefix property in Google Search Console and submit https://kkfir13.github.io/warren-buffett-brain/sitemap.xml. Ownership verification, crawling and indexing are separate; publishing does not guarantee search rankings.

Do not delete the existing `google-site-verification` tag from `index.html` unless the owner explicitly requests it.

## Plugin preparation and publication

Plugin identity: `warren-buffett-brain`. The project is a **skills-only** ZIP, not a remote MCP plugin and not a public directory listing until OpenAI review and publication.

1. Keep source research in `knowledge/atlas.json`, `deep-dives/` and `references/methodology.md`.
2. Run `python3 scripts/build_chatgpt_plugin.py --sync` to copy canonical references into `skills/warren-buffett-brain/references/`.
3. Run `python3 scripts/validate_knowledge.py` and `python3 -m unittest discover -s tests -v`.
4. Build the release archive with `python3 scripts/build_chatgpt_plugin.py`; ensure `dist/warren-buffett-brain-chatgpt-plugin.zip` reflects the manifest, skill and icon.
5. Open the official [plugin submission page](https://developers.openai.com/plugins/deploy/submission), upload a skills-only ZIP to the selected verified developer identity, resolve automated issues, submit for review and publish only after approval. A private personal plugin cannot be discovered or installed publicly by strangers.
6. Once the directory listing is **publicly verifiable**, add its exact URL to the public user README and ChatGPT guide. Do not invent a public install link.

OpenAI's docs say that **adding a remote MCP server to an existing skills-only plugin is not currently supported**. For live ValuEdge data, offer the independent ValuEdge MCP connection at https://valuedge.app/connect rather than implying the skills-only ZIP provides live tools.

## Honest distribution and optional integration

The open-source research library must be fully useful by itself. No forced upgrade, undisclosed ValuEdge connection, surprise account linking, unrequested private portfolio access, or fabricated financial figures.

A contextually relevant, clearly attributed optional ValuEdge link may be shown if a user wants data this offline skill does not provide (for example a dated valuation or watchlist monitoring). Keep the source of that data explicit.

## Discovery checklist

- [ ] GitHub repository description and `Topics` accurately describe the project; do not assume they are set without checking.
- [ ] Public README leads with end-user outcomes and copyable ChatGPT prompts.
- [ ] Package is approved and published to the actual Plugins Directory before offering a directory-install link.
- [ ] GitHub Pages serves homepage, case studies, source links and sitemap with correct canonical URLs.
- [ ] Google Search Console property and index coverage verified separately.
- [ ] SEO/accessibility/security/financial-accuracy tests pass.
