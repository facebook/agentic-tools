---
name: debug-webhooks
description: "Troubleshoot webhook issues for a Meta app — inspect active subscriptions, identify misconfiguration, and send test payloads to verify delivery. Use when webhooks aren't working as expected."
allowed-tools: mcp__devtools__devtools_webhook_list, mcp__devtools__devtools_webhook_manage, mcp__devtools__devtools_webhook_test, mcp__devtools__devtools_app_list
license: MIT
---

# Debug Webhooks

Diagnose and fix webhook delivery issues for a Meta app.

## Workflow

1. **Get context.** Ask the user for:
   - The app **name or ID** — if they give a name (or aren't sure of the ID), resolve it to an `app_id` via `devtools_app_list` (action `list`); if several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick
   - What's going wrong (not receiving events? wrong data? specific topic?)

2. **Inspect current state.** Run in parallel:
   - `devtools_webhook_list` with action `list_subscriptions` — all active subscriptions
   - `devtools_webhook_list` with action `list_topics` — all available topics (for comparison)

3. **Diagnose.** Check for common issues:

   **No subscriptions found**
   - The topic the user expects events from has no active subscription
   - Suggest using `/webhook-setup` to create one

   **Subscription exists but no events received**
   - Send a test payload: `devtools_webhook_test` with action `test_send` for the relevant topic and field
   - If test fails: callback URL may be down, unreachable, or not returning 200
   - If test succeeds but real events don't arrive: the issue is likely on the app side (permissions, page subscriptions, etc.)

   **Wrong fields subscribed**
   - Compare subscribed fields against what the user expects to receive
   - If fields are missing: use `devtools_webhook_manage` with action `update_fields`, passing the missing fields via `add_fields`
   - If extra fields cause noise: use `devtools_webhook_manage` with action `update_fields`, passing unwanted fields via `remove_fields`

   **Multiple subscriptions on same topic**
   - Flag potential conflicts or duplicate delivery

4. **Test delivery.** For each relevant subscription:
   - Call `devtools_webhook_test` with action `test_send`
   - Report whether the test payload was accepted by the callback endpoint

5. **Report findings:**

   ### Report Format

   **Active Subscriptions**
   - Topic, fields, callback URL for each

   **Issues Found**
   - Each issue with severity (critical / warning / info)
   - Root cause analysis
   - Suggested fix

   **Test Results**
   - Topic/field tested → success or failure
   - Response details if available

   **Recommended Actions**
   - Ordered list of fixes to apply

6. **Apply fixes** if the user agrees:
   - Add missing fields via `update_fields`
   - Remove unwanted fields via `update_fields`
   - For callback URL changes: unsubscribe and resubscribe (URL can only be set during subscribe)

## Common Issues Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No events received | No subscription exists | Subscribe to the topic |
| No events received | Callback URL returns non-200 | Fix server endpoint |
| No events received | App lacks page/account subscription | Subscribe the page to the app |
| Partial events | Missing fields in subscription | Add fields via update_fields |
| Duplicate events | Multiple subscriptions on same topic | Unsubscribe duplicates |
| Test works, real events don't | Permission or page-level issue | Check app permissions and page subscriptions |
