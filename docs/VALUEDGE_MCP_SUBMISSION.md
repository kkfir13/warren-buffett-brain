# Warren Buffett Brain — public ChatGPT plugin with ValuEdge MCP

## Purpose

This is an alternative public submission package for the existing Warren Buffett Brain research library. Its visible listing remains **Warren Buffett Brain**, while its **new internal package name** is **warren-buffett-brain-mcp**. It includes the independent historical skill and uses ValuEdge's existing remote server for *optional* modern-stock research.

The older draft version 1.3.0 was a **skills-only** plugin. OpenAI's published instructions state that an MCP cannot be added to an existing skills-only plugin, so this must be a **new With MCP** submission, not "Upload new version" on the existing draft.

Do not overwrite or alter the separate ValuEdge plugin or its production MCP server.

## Package

- Build the independent skills archive first: python3 scripts/build_chatgpt_plugin.py
- Build the MCP-backed submission ZIP: python3 scripts/build_valuedge_mcp_plugin.py
- Upload only dist/warren-buffett-brain-valuedge-mcp.zip for the new submission.
- The package contains the full bundled source atlas, eight case studies, method notes, assets, one skill and an mcp.json with exactly one server named valuedge.

The ValuEdge endpoint is https://valuedge.app/mcp, with Streamable HTTP and mixed public/OAuth access. The server's public tools include search_securities, get_stock_valuation, get_stock_fundamentals, compare_stocks and screen_stocks. Its private personal tools require a user-initiated ValuEdge authorization and eligible Unlimited access. The public skill does not need that account. The project is not affiliated with Buffett or Berkshire Hathaway.

## Submit

1. Open the OpenAI Plugins submission portal. Select **Upload new or existing plugin**, then the **With MCP** flow for a new plugin.
2. Upload the new ZIP. Confirm that the listing is Warren Buffett Brain and the installed server is valuedge at https://valuedge.app/mcp. Do not use the existing skills-only draft.
3. Open MCPs, select the server, and Connect. Use the authentication configuration shown by the portal, complete domain verification and scan tools.
4. A shared ValuEdge endpoint may already have a domain-challenge token for another plugin. Follow the portal's permitted domain verification options. Do **not** replace an existing live verification token without confirming it is safe; OpenAI advises using an eligible parent origin or distinct hostname if the challenge URL conflicts.
5. Inspect the scanned tool metadata, annotations and justifications. The server's actual metadata takes precedence over descriptions typed in the portal. Correct issues on the production server and rescan when necessary.
6. The package preloads five positive and three negative review cases. Verify every case in a real connected client and adjust test cases via a new ZIP if a case does not match actual behavior.
7. Record a short walkthrough that proves the main MCP calls on supported surfaces; host the recording at an accessible HTTPS URL and provide it in the review form. The ZIP intentionally contains no fabricated recording URL.
8. Supply an eligible demo account to the review team through the secure dashboard if OAuth-restricted features are included in their review. Never put passwords or secrets into the package, repository or plugin metadata.
9. Resolve privacy/terms issues, finish identity verification, ensure relevant declarations accurately reflect data flows, and submit for review. Approval is not publication: publish the approved plugin separately.

## Review risks and remaining manual checks

- Whether the submission portal allows a second branded plugin to use the existing ValuEdge MCP endpoint has not been verified. Submit as a distinct use case, not a disguised duplicate of the existing ValuEdge listing.
- The server's existing authorization discovery, domain challenge, annotation justifications and permissions must pass the live portal scan. A successful standalone ValuEdge tool call does not prove all these checks.
- The new package uses mixed authentication because ValuEdge advertises no-login public research and OAuth-gated private data. The plugin does not embed client credentials. If OAuth discovery fails, inspect ValuEdge's production authorization metadata rather than guessing endpoints.
- A review demo-recording URL and any reviewer account credentials must be completed in the portal before submission.
- Keep the current skills-only ZIP untouched; it remains a different distribution.

## Official sources

- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission-errors
- https://valuedge.app/connect
