---
name: search-docs
description: "Search Meta developer documentation for API guides, references, and tutorials. Use when looking up how a Meta API works, finding integration guides, or exploring platform capabilities."
allowed-tools: mcp__devtools__devtools_discovery
license: MIT
---

# Search Docs

Search the Meta Developer Platform documentation to answer API questions, find integration guides, and explore platform capabilities.

## Workflow

1. **Understand the query.** Determine what the user is looking for:
   - API reference (e.g., "how does the Page API work?")
   - Integration guide (e.g., "how to set up Instagram webhooks?")
   - Troubleshooting (e.g., "why am I getting error code 190?")
   - Feature discovery (e.g., "what can I do with the WhatsApp Business API?")

2. **Search.** Call `devtools_discovery` with action `search_docs`:
   - Formulate a clear, specific query
   - Start with `max_results` of 5
   - If results are too broad, refine the query and search again

3. **Present results.** For each result:
   - Title and brief description
   - Direct relevance to the user's question
   - Key takeaways or next steps

4. **Refine if needed.** If initial results don't answer the question:
   - Try alternative search terms (e.g., "Graph API permissions" instead of "Facebook API access")
   - Use pagination via `offset` to explore more results
   - Broaden or narrow the query based on what was returned

5. **Synthesize.** Don't just list links — extract the answer:
   - Summarize the relevant documentation
   - Highlight key requirements, limitations, or gotchas
   - Provide code patterns or configuration steps if applicable

## Search Tips

- Use product-specific terms: "WhatsApp Business API" not "WhatsApp API"
- Include the specific operation: "create ad campaign" not "ads"
- For error codes, search the exact code: "error 190" or "OAuthException"
- For permissions, include the permission name: "pages_read_engagement permission"

## When to suggest other skills

- If the user is looking up webhook configuration → suggest `/webhook-setup`
- If the user is researching app review requirements → suggest `/app-review-prep`
- If the user is troubleshooting compliance → suggest `/compliance-check`
