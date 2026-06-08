---
name: api-health
description: "Monitor API health for a Meta app — check rate limits, call volume, and API deprecations. Use to diagnose throttling, plan capacity, or prepare for API version migrations."
allowed-tools: mcp__devtools__devtools_api_usage, mcp__devtools__devtools_app_list
license: MIT
---

# API Health

Monitor API usage, rate limits, and deprecations for a Meta app.

## Workflow

1. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

2. **Collect API health data in parallel:**
   - `devtools_api_usage` with action `rate_limits` — current rate limit status per metric
   - `devtools_api_usage` with action `call_volume` — total calls vs quota
   - `devtools_api_usage` with action `deprecations` — deprecated APIs and migration guides

3. **Analyze and report:**

   ### Report Format

   **Rate Limits**
   - Overall status: healthy / warning / throttled
   - Per-metric breakdown with usage percentages
   - Effective users count (DAU/WAU/MAU aggregate)
   - Flag any metric above 80% as a warning, above 100% as critical

   **Call Volume**
   - Total calls and quota
   - Usage rate (calls/quota ratio)
   - Flag if usage_rate > 0.8 as approaching limit, > 1.0 as throttled
   - If the user provided an endpoint filter, show filtered results

   **API Deprecations**
   - Latest platform version
   - Each deprecation with: type, name, severity, and recommendation
   - Link to migration guides where available

   **Action Items**
   - Prioritized by severity:
     1. Throttled rate limits (immediate action needed)
     2. High-severity deprecations (migration required)
     3. Warning-level rate limits (monitor or optimize)
     4. Low-severity deprecations (plan for future)

4. **Offer deeper investigation** based on findings:
   - If throttled: offer to check call volume for specific endpoints (`endpoint` param) to find the hot path
   - If deprecations found: offer to search docs (`/search-docs`) for migration guides
   - If healthy: suggest setting up a monitoring cadence

## Advanced Usage

### Check specific endpoint volume
If the user wants to investigate a specific API endpoint, call `devtools_api_usage` with action `call_volume` and pass the `endpoint` parameter (e.g., `/me/feed`) to filter results to that path.

### Custom lookback window
The `lookback_minutes` parameter controls the time range (default: 1440 = 1 day):
- Last hour: `lookback_minutes` = 60
- Last week: `lookback_minutes` = 10080
- Last 30 days: `lookback_minutes` = 43200

## Tips

- Rate limit thresholds: 80% = warning, 100% = throttled. These are based on usage_percentage in the rate_limits response.
- A usage_rate > 1.0 in call_volume means the app is actively being throttled.
- Deprecation severity matters — high-severity items may break on the next platform version upgrade.
- Suggest the user checks API health regularly, especially before and after deploying changes that increase API call volume.
