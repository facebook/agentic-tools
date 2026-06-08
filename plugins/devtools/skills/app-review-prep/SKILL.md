---
name: app-review-prep
description: "Prepare a Meta app for App Review — checks current status, outstanding requirements, granted privileges, and submission history. Use before submitting an app for review."
allowed-tools: mcp__devtools__devtools_app_review, mcp__devtools__devtools_app, mcp__devtools__devtools_compliance, mcp__devtools__devtools_app_list
license: MIT
---

# App Review Prep

Check everything needed before submitting a Meta app for App Review.

## Workflow

1. **Identify the app.** Ask the user for the app **name or ID**. If they give a name (or aren't sure of the ID), call `devtools_app_list` (action `list`) and resolve it to an `app_id` — match the name case-insensitively. If several apps match or it's ambiguous, show the candidates (name, ID, viewer role) and ask the user to pick. If they give a numeric ID, use it directly.

2. **Collect review data in parallel.** Run all calls concurrently:
   - `devtools_app` with action `basic_settings` — app name, category, status for report context
   - `devtools_app_review` with action `status` — current review state
   - `devtools_app_review` with action `requirements` — what's needed for approval
   - `devtools_app_review` with action `privileges` — currently granted permissions/features
   - `devtools_app_review` with action `history` — past submissions and their outcomes
   - `devtools_compliance` with action `status` — compliance blockers that could prevent approval

3. **Analyze readiness.** Evaluate:
   - Are all required items complete?
   - Are there compliance violations that would block review?
   - Have previous submissions been rejected? If so, what was the reason?
   - Which permissions/features are already approved vs. still needed?

4. **Produce a readiness report:**

   ### Report Format

   **Current Status**
   - Review state (e.g., not submitted, in review, approved, rejected)
   - Last submission date and outcome (if any)

   **Granted Privileges**
   - List of approved permissions and features

   **Outstanding Requirements**
   - Each requirement with its completion status
   - Clear description of what's needed to fulfill incomplete items

   **Compliance Blockers**
   - Any violations or required actions that must be resolved before submission

   **Submission History**
   - Past submissions with dates, statuses, and rejection reasons (if any)
   - Pattern analysis if there are repeated rejections

   **Readiness Verdict**
   - READY: all requirements met, no blockers
   - NOT READY: list exactly what needs to be done, in priority order

5. **Suggest next steps** based on the verdict:
   - If NOT READY: specific actions to take, in order
   - If READY: guidance on what to expect during the review process
   - If there are compliance issues: suggest `/compliance-check` for remediation

## Tips

- Rejected submissions often cite the same issues. If history shows a pattern, call it out prominently.
- Compliance status is a prerequisite — resolve violations before worrying about other requirements.
- Some requirements need evidence (screenshots, privacy policy URLs, etc.) that can't be checked programmatically. Flag these as "manual verification needed."
