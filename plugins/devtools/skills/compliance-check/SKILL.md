---
name: compliance-check
description: "Check compliance status for a Meta app — surfaces open required actions, active violations, and recommendations with remediation guidance. Use to audit compliance posture or resolve compliance blockers."
allowed-tools: mcp__devtools__devtools_compliance, mcp__devtools__devtools_app, mcp__devtools__devtools_app_list
license: MIT
---

# Compliance Check

Audit the compliance posture of a Meta app and provide remediation guidance.

## Workflow

1. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

2. **Collect data in parallel:**
   - `devtools_compliance` with action `status` — full compliance status
   - `devtools_app` with action `basic_settings` — app context (name, category, status)
   - `devtools_app` with action `data_protection_officer` — DPO contact info

3. **Analyze compliance status.** Categorize findings by severity:

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

4. **Produce the compliance report:**

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

5. **Suggest follow-ups:**
   - If violations exist: emphasize urgency and potential consequences
   - If DPO info is missing: explain why it matters and how to set it up
   - If app review is blocked by compliance: suggest `/app-review-prep` after resolving issues

## Tips

- Compliance deadlines are hard deadlines — missing them can result in app restrictions.
- Some compliance items require changes in the Meta Developer Dashboard that can't be done via API. Flag these clearly as "manual action required in Developer Dashboard."
- If the app is fully compliant, keep the report brief and congratulatory.
