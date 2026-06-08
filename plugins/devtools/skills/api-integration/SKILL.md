---
name: api-integration
description: "Guide a developer through setting up a Meta API integration from scratch — discovers the right APIs, fetches setup guides, authentication requirements, permissions, and code examples. Use when the user wants to build with a specific Meta product (WhatsApp, Instagram, Messenger, Pages, Ads, etc.)."
allowed-tools: mcp__devtools__devtools_discovery, mcp__devtools__devtools_app, mcp__devtools__devtools_app_review, mcp__devtools__devtools_app_list
license: MIT
---

# API Integration

Help a developer go from "I want to integrate with X" to having everything they need to start writing code.

## Workflow

1. **Identify the integration.** Ask the user what they want to build if not clear. Common integrations:
   - WhatsApp Business API (send/receive messages, templates, media)
   - Instagram Graph API (publish content, read insights, manage comments)
   - Messenger Platform (chatbots, send API, webhooks)
   - Pages API (post content, read insights, manage pages)
   - Marketing API (create campaigns, manage ads, read analytics)
   - Login with Facebook / Login with Instagram
   - Facebook Login for Business

2. **Research the integration.** Run multiple searches to build a complete picture. Do NOT stop at one search — layer queries to cover all aspects:

   **Search 1 — Overview and getting started:**
   - `devtools_discovery` → `search_docs` with the product name + "getting started" or "overview"
   - e.g., "WhatsApp Business API getting started"

   **Search 2 — Authentication and access tokens:**
   - `devtools_discovery` → `search_docs` for authentication requirements
   - e.g., "WhatsApp Business API access token authentication"

   **Search 3 — Required permissions and app review:**
   - `devtools_discovery` → `search_docs` for permissions
   - e.g., "WhatsApp Business API permissions"
   - Also check the app if an app_id is provided: `devtools_app_review` → `requirements` and `privileges`

   **Search 4 — Core API endpoints:**
   - `devtools_discovery` → `search_docs` for the specific operations the user needs
   - e.g., "WhatsApp send message API" or "Instagram publish media API"

   **Search 5 — Webhooks (if applicable):**
   - `devtools_discovery` → `search_docs` for webhook setup
   - e.g., "WhatsApp webhooks setup"

   **Search 6 — Rate limits and quotas:**
   - `devtools_discovery` → `search_docs` for product-specific rate limits and throughput tiers
   - e.g., "WhatsApp Business API rate limits messaging tiers" or "Instagram API rate limits"

   **Search 7 — Code examples and SDKs:**
   - `devtools_discovery` → `search_docs` for SDK, client library, or code samples
   - Try product-specific queries first: "WhatsApp Business Platform Node.js" or "Instagram Graph API Python"
   - If no SDK results, search for "Graph API client library" or the product's quickstart guide
   - Fall back to constructing examples from the endpoint documentation in Search 4

   Run searches 1-5 in parallel for speed. Run 6-7 after if needed. Use `max_results` of 10 and pagination via `offset` to get comprehensive results. Refine queries if initial results are too broad or miss key topics.

3. **Check app readiness** (if the user has an app):
   - If they referred to the app by **name** (or aren't sure of the ID), resolve it to an `app_id` first via `devtools_app_list` (action `list`); if ambiguous, show the candidates (name, ID, viewer role) and ask them to pick
   - `devtools_app` → `basic_settings` to confirm app type and status
   - `devtools_app_review` → `privileges` to see what's already approved
   - `devtools_app_review` → `requirements` to see what's needed

4. **Synthesize an integration guide.** Extract the key information from search results — do NOT dump raw results. Organize findings into an actionable document:

   ### Guide Format

   **Overview**
   - What the API does and what the user can build with it
   - Link to the official product documentation

   **Prerequisites**
   - Meta Developer account
   - App type required (Business, Consumer, etc.)
   - Any product-specific prerequisites (e.g., WhatsApp Business Account, Facebook Page)

   **Authentication**
   - Token type needed (User, Page, System User, etc.)
   - How to generate tokens
   - Token permissions/scopes required
   - Token expiration and refresh flow

   **Required Permissions**
   - List each permission needed and what it grants
   - Which permissions need App Review vs. are auto-approved
   - If app_id provided: which are already granted vs. still needed

   **Setup Steps**
   - Step-by-step from zero to first API call
   - Include webhook setup if the integration requires it

   **Key API Endpoints**
   - Each endpoint with: method, URL pattern, key parameters, example response
   - Focused on what the user asked for, not an exhaustive list

   **Code Example**
   - A working starter example in the user's preferred language
   - Include authentication, a basic API call, and error handling
   - Use the official SDK if one exists, raw HTTP (curl/fetch) if not
   - Include webhook handler code if the integration is webhook-based

   **Rate Limits and Quotas**
   - Product-specific rate limits and throughput tiers (e.g., WhatsApp messaging tiers: 1K/10K/100K/unlimited)
   - Per-endpoint rate limits if applicable
   - Suggest `/api-health` for ongoing monitoring

   **Common Pitfalls**
   - Product-specific gotchas the docs call out
   - Permission mistakes, token type confusion, webhook verification issues

5. **Offer next steps:**
   - `/app-review-prep` if permissions need App Review
   - `/webhook-setup` if the integration uses webhooks
   - `/api-health` to monitor usage once live

## Tips

- Always search multiple times with different queries. A single search rarely covers authentication + permissions + endpoints + examples.
- Prefer the user's stated language/framework for code examples. Default to Node.js/JavaScript if not specified.
- If the user has an app_id, cross-reference their current permissions against what the integration requires — this saves them time.
- Some integrations (WhatsApp, Instagram) require a Business-type app. Call this out early if the user's app is the wrong type.
- Webhook-based integrations (Messenger, WhatsApp) won't work without a callback URL. Suggest `/webhook-setup` proactively.
