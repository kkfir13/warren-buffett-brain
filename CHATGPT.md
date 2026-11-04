# Use Warren Buffett Brain with ChatGPT

This public repository contains a **skills-only ChatGPT Plugin package**. The plugin bundles original research notes and case studies. It does **not** need a localhost server, Python, an MCP server, a ValuEdge account or an OpenAI API key for the end user.

## For ChatGPT users

**Public directory status:** A GitHub repository is **not** an installed ChatGPT plugin. The package must first pass OpenAI review and be published in the universal Plugins Directory. Until a public directory listing is available, do not advertise a one-click installation or imply ChatGPT automatically loads a GitHub `SKILL.md`.

Once approved and published, open **Plugins** in ChatGPT, search for **Warren Buffett Brain**, install it, and use it on a supported ChatGPT surface. Availability and capabilities depend on your plan and product surface. Example prompts:

- "What did Buffett learn from buying See's Candies? Link to Berkshire's original evidence."
- "Explain the GEICO investment history, including the counterarguments."
- "Assess [company] using Buffett-style business-quality questions. Don't pretend Buffett endorsed it."

Alternatively, anyone can browse the [free research website](https://kkfir13.github.io/warren-buffett-brain/) or read the source-linked notes in GitHub without ChatGPT.

## For the maintainer: prepare and publish

1. Keep the canonical corpus in `knowledge/atlas.json`, `deep-dives/` and `references/methodology.md`. Synchronize the packaged copies in `skills/warren-buffett-brain/references/` by running `python3 scripts/build_chatgpt_plugin.py --sync`.
2. Run `python3 scripts/validate_knowledge.py` and `python3 -m unittest discover -s tests -v`.
3. Download the [ready-to-submit ZIP](dist/warren-buffett-brain-chatgpt-plugin.zip), or run `python3 scripts/build_chatgpt_plugin.py` to create a **clean ZIP** at `dist/warren-buffett-brain-chatgpt-plugin.zip`. The ZIP contains only `plugin.json`, `LICENSE` and `skills/`—not the website, tests or Python tools.
4. Use the official [OpenAI plugin submission flow](https://developers.openai.com/plugins/deploy/submission). Select a verified developer identity, upload the ZIP as a **Skills only** package, resolve metadata and skill review issues, submit for review, and then choose **Publish** after approval.
5. Verify the published directory URL and replace this "not yet public" notice only after real publication. Distribution to the entire public directory is **not** the same as sharing a personal/private plugin.

**Important:** This is a skills-only plugin. Adding a remote MCP server to an already published skills-only listing may require a new submission; plan this as a separate product if live market data becomes central. A plain GitHub URL cannot be registered as an MCP endpoint.

## Local website preview (optional, for developers only)

```bash
git clone https://github.com/kkfir13/warren-buffett-brain.git
cd warren-buffett-brain
python3 -m http.server 8000
```

`http://localhost:8000/` works **only on the computer running that command**. It is not a public website, an MCP endpoint, or a ChatGPT integration. Use the GitHub Pages URL for the public research site.

## Accuracy and scope

This is an independent Buffett-inspired educational resource, not a Buffett persona. The bundle contains **55 original evidence notes, 60 source links and eight case studies**, not full copyrighted books/letters/transcripts. Facts should cite original source URLs. Interpretations and valuation scenarios must be labeled. There is no broker connection, real-time quote feed, or privileged access to users' accounts.
