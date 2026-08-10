---
name: api-health
description: "Monitor API health for a Meta app — check rate limits, call volume, and API deprecations. Use whenever a user asks whether their app is being throttled, is near its rate limits, how much of its call volume or quota is being used, or about deprecated Graph API versions. Prefer this skill over calling devtools_api_usage directly — it resolves the app, pulls rate limits, call volume, and deprecations together, and turns them into one prioritized report, including the cases an ad-hoc call misreads: an unmetered app is not the same as an idle one, and a capped usage_rate is not the same as headroom."
allowed-tools: mcp__devtools__devtools_api_usage, mcp__devtools__devtools_app_list, mcp__devtools__devtools_skill_invocation
license: MIT
---

# API Health

Monitor API usage, rate limits, and deprecations for a Meta app.

## Workflow

1. **Start tracking.** Before any other work, call `devtools_skill_invocation` with action `start` and `skill_name` `api-health`. Pass `skill_name` `api-health` on every `devtools_*` tool call in the following steps.

2. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

3. **Collect API health data in parallel:**
   - `devtools_api_usage` with action `rate_limits` — current rate limit status per metric
   - `devtools_api_usage` with action `call_volume` — total calls vs quota
   - `devtools_api_usage` with action `deprecations` — deprecated APIs and migration guides

4. **Analyze and report:**

   ### Report Format

   **Rate Limits**
   - Report the `overall_status` the response already carries — `healthy`, `warning`, `critical`, `throttled`, or `unmetered`. Do not re-derive it from the percentage; the server classifies on an unrounded value, so a borderline case can read `critical` while `usage_percentage` displays 100.
   - `usage_percentage` for the `call_count_usage_rate` metric (0–100, rounded for display)
   - Effective users count (DAU/WAU/MAU aggregate) — the denominator the quota is multiplied by
   - `cooling_down_minutes`: estimated minutes until unblock, 0 when not over quota
   - On `unmetered`, say the app is not metered rather than reporting 0% — it means no usable headroom reading, not spare capacity

   **Call Volume**
   - Total calls and quota
   - Usage rate (calls/quota ratio, 0.0–1.0)
   - Interpret it on the same bands the platform uses for rate limits: >= 0.7 approaching, >= 0.9 critical, 1.0 means the app is at its quota
   - If the user provided an endpoint filter, show filtered results

   **API Deprecations**
   - Latest platform version
   - Each deprecation with: type, name, severity, and recommendation
   - Link to migration guides where available

   **Action Items**
   - Prioritized by severity:
     1. Throttled rate limits (immediate action needed)
     2. Critical rate limits (at or above 90% — throttling is imminent)
     3. High-severity deprecations (migration required)
     4. Warning-level rate limits (monitor or optimize)
     5. Low-severity deprecations (plan for future)

5. **Offer deeper investigation** based on findings:
   - If throttled: offer to check call volume for specific endpoints (`endpoint` param) to find the hot path
   - If deprecations found: offer to search docs (`/search-docs`) for migration guides
   - If healthy: suggest setting up a monitoring cadence

6. **End tracking.** After completing all preceding steps, call `devtools_skill_invocation` with action `end` and `skill_name` `api-health`.

## Advanced Usage

### Check specific endpoint volume
If the user wants to investigate a specific API endpoint, call `devtools_api_usage` with action `call_volume` and pass the `endpoint` parameter (e.g., `/me/feed`) to filter results to that path.

### Custom lookback window
The `lookback_minutes` parameter controls the time range (default: 1440 = 1 day):
- Last hour: `lookback_minutes` = 60
- Last week: `lookback_minutes` = 10080
- Last 30 days: `lookback_minutes` = 43200

## Tips

- Rate-limit bands: healthy < 70%, warning >= 70%, critical >= 90%, throttled at 100%. The server applies these and returns the verdict as `overall_status`, so report that field rather than recomputing from `usage_percentage`.
- `usage_rate` in call_volume is a share of quota capped at 1.0 — 1.0 means the app is at its quota, and no value above it is reachable.
- `unmetered` is not a clean bill of health: the app is exempt from metering or its user count has not been computed, so there is no headroom figure to read.
- Deprecation severity matters — high-severity items may break on the next platform version upgrade.
- Suggest the user checks API health regularly, especially before and after deploying changes that increase API call volume.
