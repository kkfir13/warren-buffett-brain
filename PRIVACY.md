# Warren Buffett Brain — privacy and data handling

Updated 4 November 2026

This document describes the open-source research website and the public read-only MCP server code in this repository. An MCP hosting URL must be deployed and verified before it is publicly advertised.

**Accounts and financial data:** The website and MCP research tools require no personal account or broker connection. They do not request brokerage credentials, execute trades, read private portfolios or expose ValuEdge customer data.

**Queries:** The MCP implementation processes search terms and record IDs in memory to answer research queries. The source code does not write search terms into an application database or create user profiles. The software returns source-linked historical research notes from a public, committed knowledge registry.

**Hosting and technical records:** GitHub Pages hosts the website; any deployed MCP instance is operated by the selected infrastructure provider (for example, Cloudflare Workers). Those providers may process IP addresses, requests and operational logs under their own policies. The Worker code logs transport errors but does not deliberately log full search queries. This is not a promise that an infrastructure provider retains no technical data.

**External sources:** Research answers link to outside publishers, including Berkshire Hathaway and CNBC. Opening an external link takes you to that publisher's website and privacy practices.

**Feedback:** GitHub Issues may publicly display information you submit there. Do not submit private financial, account, or identity data to public issues.

**Contact:** Use the project's [GitHub Issues](https://github.com/kkfir13/warren-buffett-brain/issues) for questions about the source code or data handling.

No feature in the published source code sells personal data or sends user queries to a commercial LLM API. Hosting operators should review their own logs, security settings and actual data flows before publishing this policy for their instance.
