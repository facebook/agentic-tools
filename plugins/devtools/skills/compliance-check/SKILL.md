---
name: compliance-check
description: "Check compliance status for a Meta app — surfaces open required actions, active violations, and recommendations with remediation guidance. Use to audit compliance posture or resolve compliance blockers."
allowed-tools: mcp__devtools__devtools_compliance, mcp__devtools__devtools_app, mcp__devtools__devtools_app_list, mcp__devtools__devtools_skill_invocation
license: MIT
metadata:
  mcp:
    devtools:
      type: streamable-http
      url: "https://mcp.facebook.com/devtools"
---

# Compliance Check

Audit the compliance posture of a Meta app and provide remediation guidance.

## Prerequisites — MCP connection (read first)

This skill needs the Meta Social Technologies MCP server `devtools` (`https://mcp.facebook.com/devtools`, streamable-http). Plugin installs bundle it; skills-only installs such as `npx skills add` do not ([setup](https://github.com/facebook/agentic-tools#install-via-vercel-skillssh)).

**If the `mcp__devtools__*` tools are not available, STOP.** Do not invent tool output, including the step 1 tracking call. Ask the user to add the server and complete its OAuth flow (never ask for an access token), then continue.

## Workflow

1. **Start tracking.** Before any other work, call `devtools_skill_invocation` with action `start` and `skill_name` `compliance-check`. Pass `skill_name` `compliance-check` on every `devtools_*` tool call in the following steps.

2. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

3. **Collect data in parallel:**
   - `devtools_compliance` with action `status` — full compliance status
   - `devtools_app` with action `basic_settings` — app context (name, category, status)
   - `devtools_app` with action `data_protection_officer` — DPO contact info

4. **Analyze compliance status.** Categorize findings by severity:

   **Violations** (critical — may result in app restrictions or removal)
   - What the violation is
   - When it was flagged
   - What action is required
   - Deadline for resolution

   **Required Actions** (high — must be completed by deadline)
   - Description of the required action
   - Deadline
   - Steps to complete

   **Recommendations** (low — suggested improvements)
   - What's recommended and why
   - How to implement

5. **Produce the compliance report:**

   ### Report Format

   **App Overview**
   - App name, ID, category

   **Compliance Score**
   - Overall status: COMPLIANT / ACTION REQUIRED / VIOLATION
   - Count of items by severity

   **Violations** (if any)
   - Each violation with description, deadline, and remediation steps

   **Required Actions** (if any)
   - Each action with description, deadline, and steps to complete

   **Recommendations** (if any)
   - Each recommendation with description and implementation guidance

   **Data Protection Officer**
   - Current DPO contact info
   - Flag if DPO info is missing or incomplete

   **Action Plan**
   - Prioritized list: violations first, then required actions by deadline, then recommendations
   - For each item, provide specific steps the developer can take

6. **Suggest follow-ups:**
   - If violations exist: emphasize urgency and potential consequences
   - If DPO info is missing: explain why it matters and how to set it up
   - If app review is blocked by compliance: suggest `/app-review-prep` after resolving issues

7. **End tracking.** After completing all preceding steps, call `devtools_skill_invocation` with action `end` and `skill_name` `compliance-check`.

## Tips

- Compliance deadlines are hard deadlines — missing them can result in app restrictions.
- Some compliance items require changes in the Meta Developer Dashboard that can't be done via API. Flag these clearly as "manual action required in Developer Dashboard."
- If the app is fully compliant, keep the report brief and congratulatory.
