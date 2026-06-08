---
name: app-health-check
description: "Run a comprehensive health check on a Meta app — audits settings, security, compliance, app review status, rate limits, and API deprecations in one pass. Use when you want a full picture of an app's current state."
allowed-tools: mcp__devtools__devtools_app, mcp__devtools__devtools_app_review, mcp__devtools__devtools_compliance, mcp__devtools__devtools_api_usage, mcp__devtools__devtools_app_list
license: MIT
---

# App Health Check

Run a full audit of a Meta app and produce an actionable report.

## Workflow

1. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

2. **Collect data in parallel.** Run all calls concurrently to minimize latency:
   - `devtools_app` with action `basic_settings` — app name, category, platform, contact info
   - `devtools_app` with action `security` — app secret rotation, allowed domains, data deletion URL
   - `devtools_compliance` with action `status` — open required actions, violations, recommendations
   - `devtools_app_review` with action `status` — current review state, pending submissions
   - `devtools_api_usage` with action `rate_limits` — current rate limit health
   - `devtools_api_usage` with action `deprecations` — deprecated APIs needing migration

3. **Synthesize the report.** Organize findings into these sections:

   ### Report Format

   **App Overview**
   - App name, ID, category, status

   **Security**
   - Highlight any issues: missing data deletion URL, stale app secret, overly broad domain allowlist
   - Flag if App Secret has not been rotated recently

   **Compliance**
   - List any open required actions with deadlines
   - List any active violations
   - Summarize recommendations

   **App Review**
   - Current review status
   - Any pending or rejected submissions
   - Permissions/features that still need review

   **API Health**
   - Rate limit status (healthy / warning / throttled)
   - Any metrics above 80% usage
   - Deprecated APIs with severity and migration recommendations

   **Action Items**
   - Prioritized list of things to fix, ordered by severity (violations > required actions > recommendations > improvements)

4. **Offer next steps.** Suggest relevant follow-up skills:
   - `/compliance-check` for deeper compliance remediation
   - `/app-review-prep` if there are pending review requirements
   - `/webhook-setup` if webhooks aren't configured yet
   - `/api-health` for deeper API usage analysis and endpoint-level investigation

## Tips

- If any MCP call fails, report the failure in the relevant section rather than aborting the whole check.
- Always include the app ID in the report header for easy reference.
- For apps with no issues, keep the report short — don't pad with unnecessary detail.
