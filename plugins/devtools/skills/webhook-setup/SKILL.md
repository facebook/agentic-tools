---
name: webhook-setup
description: "Set up webhooks for a Meta app end-to-end — discover available topics, subscribe to fields, and verify with a test payload. Use when configuring webhooks for the first time or adding new subscriptions."
allowed-tools: mcp__devtools__devtools_webhook_list, mcp__devtools__devtools_webhook_manage, mcp__devtools__devtools_webhook_test, mcp__devtools__devtools_app_list
license: MIT
---

# Webhook Setup

Interactive wizard to configure webhooks on a Meta app from scratch.

## Workflow

1. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

2. **Check existing state.** Run in parallel:
   - `devtools_webhook_list` with action `list_topics` — show all available webhook topics
   - `devtools_webhook_list` with action `list_subscriptions` — show what's already subscribed

3. **Present the options.** Show the user:
   - Available topics (e.g., `page`, `user`, `instagram`, `whatsapp_business_account`)
   - Which topics already have active subscriptions
   - For each topic, list the subscribable fields

4. **Collect subscription details.** Ask the user for:
   - **Topic** — which webhook topic to subscribe to
   - **Fields** — which fields within that topic (e.g., `feed`, `messages`)
   - **Callback URL** — their HTTPS endpoint (must be live and pass Meta's verification challenge)
   - **Verify token** — the token their server expects for the verification handshake

5. **Subscribe.** Call `devtools_webhook_manage` with action `subscribe`:
   - Pass `topic`, `fields`, `callback_url`, `verify_token`
   - If the subscription fails, explain the likely cause:
     - Callback URL not reachable → server must be running and publicly accessible
     - Verification failed → verify token mismatch or endpoint not responding to GET challenge
     - Invalid fields → check field names against the topic's available fields

6. **Verify with a test payload.** After successful subscription:
   - Call `devtools_webhook_test` with action `test_send` for one of the subscribed fields
   - Confirm whether the test payload was delivered
   - If test fails, suggest checking server logs and endpoint configuration

7. **Summary.** Show the final state:
   - Topic and fields subscribed
   - Callback URL configured
   - Test result (success/failure)

## Tips

- If the user wants to modify an existing subscription (add/remove fields), use `devtools_webhook_manage` with action `update_fields` instead of unsubscribe + resubscribe.
- Always verify after subscribing — a successful subscribe call doesn't guarantee payloads will be delivered correctly.
- Remind users that their callback URL must handle both the GET verification challenge and POST event payloads.
