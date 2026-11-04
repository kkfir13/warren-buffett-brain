# Warren Buffett Brain — privacy and data handling

Updated 4 November 2026

This document describes the open-source research website, the packaged ChatGPT skill and the optional local MCP adapter. The project does not currently operate a public remote MCP server. It requires no Buffett Brain account.

**Accounts and financial data:** The website, bundled skill and optional local MCP adapter require no personal account or broker connection. They do not request brokerage credentials, execute trades, read private portfolios or expose ValuEdge customer data.

**Queries:** The local MCP adapter processes search terms and record IDs on the user's machine. In ChatGPT, a bundled skill's requests and responses are processed according to ChatGPT's applicable privacy controls. The source code does not write search terms into an application database or create user profiles. The software returns source-linked historical research notes from a public, committed knowledge registry.

**Hosting and technical records:** GitHub Pages hosts the website; the standalone skill does not operate its own hosted backend. GitHub and the user's AI host may process normal technical requests under their own policies. If a user chooses to self-host the optional remote Worker implementation, that operator is separately responsible for its service logs. This is not a promise that an infrastructure provider retains no technical data.

**External sources:** Research answers link to outside publishers, including Berkshire Hathaway and CNBC. Opening an external link takes you to that publisher's website and privacy practices.

**Feedback:** GitHub Issues may publicly display information you submit there. Do not submit private financial, account, or identity data to public issues.

**Contact:** Use the project's [GitHub Issues](https://github.com/kkfir13/warren-buffett-brain/issues) for questions about the source code or data handling.

No feature in the published source code sells personal data or sends user queries to a commercial LLM API. Hosting operators should review their own logs, security settings and actual data flows before publishing this policy for their instance.
