# Agent Guide — Agentic Tools

This file helps AI agents navigate and use this repository effectively.

## What this repo is

A skills repository for AI coding agents that provides workflow-oriented guidance for the **Meta Developer Platform**. Skills wrap the Developer Tools MCP server tools into higher-level workflows for app management, webhook configuration, compliance auditing, app review preparation, API health monitoring, and documentation search.

## How this repo is organized

This repo is a **multi-plugin marketplace**. The marketplace manifest lives at the repo root (`.claude-plugin/marketplace.json`); each product group is a self-contained plugin under `plugins/<group>/`. Today there is one group, the **Developer Tools** plugin (`devtools`). To add another product group later, drop in a sibling `plugins/<group>/` and add an entry to `marketplace.json` — no restructuring.

Each plugin (`plugins/devtools/`) contains:

- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `.codex-plugin/plugin.json` — Codex plugin manifest
- `.mcp.json` — MCP server config, auto-bundled with the plugin
- `skills/<name>/SKILL.md` — the skills
- `hooks/` — session hooks

Skills follow the open [Agent Skills standard](https://agentskills.io) (`SKILL.md`), which Claude Code, Cursor, and Codex all understand. Agents should read `SKILL.md` for the skill invoked by the user. Each skill declares its `allowed-tools` in the frontmatter (used by Claude to scope MCP tool access; ignored harmlessly by other agents).

## MCP server dependency

All skills require the **Developer Tools MCP** server to be connected. This is a remote streamable-HTTP server (`https://mcp.facebook.com/devtools`). There is no standalone CLI — the skills drive the MCP for all their work, so it must be connected first.

- **Claude Code**: `claude plugin marketplace add facebook/agentic-tools` then `claude plugin install devtools@facebook`; connect with `/mcp`. The MCP config is bundled in the plugin's `.mcp.json`.
- **Cursor**: import via Settings → Rules → Add Rule → Remote Rule (GitHub), then enable the **Developer Tools MCP** (`devtools`) from Settings → MCP (config in `.cursor/mcp.json`).
- **Codex**: install via `$skill-installer`, and add the MCP to `~/.codex/config.toml` (see README).

## Skill index

| Skill | Directory | When to use |
|-------|-----------|-------------|
| app-health-check | `plugins/devtools/skills/app-health-check/` | Runs a comprehensive audit of a Meta app — settings, security, compliance, app review, rate limits, and API deprecations in one pass. |
| webhook-setup | `plugins/devtools/skills/webhook-setup/` | Sets up webhooks end-to-end — discovers topics, subscribes to fields, and verifies with a test payload. |
| app-review-prep | `plugins/devtools/skills/app-review-prep/` | Prepares a Meta app for App Review — checks status, requirements, privileges, submission history, and compliance blockers. |
| debug-webhooks | `plugins/devtools/skills/debug-webhooks/` | Troubleshoots webhook delivery issues — inspects subscriptions, sends test payloads, diagnoses misconfigurations. |
| compliance-check | `plugins/devtools/skills/compliance-check/` | Audits compliance posture — surfaces violations, required actions, and recommendations with remediation guidance. |
| api-health | `plugins/devtools/skills/api-health/` | Monitors API health — checks rate limits, call volume, and API deprecations with actionable thresholds. |
| api-integration | `plugins/devtools/skills/api-integration/` | Guides a developer through setting up a new Meta API integration — discovers APIs, fetches setup guides, authentication, permissions, and code examples. |
| search-docs | `plugins/devtools/skills/search-docs/` | Searches Meta developer documentation for API guides, references, and tutorials. |

## Directory structure

```
.
├── .claude-plugin/
│   └── marketplace.json         # Marketplace manifest (lists plugins by source)
├── .cursor/
│   └── mcp.json                 # Developer Tools MCP config for Cursor
├── plugins/
│   └── devtools/                # The Developer Tools plugin
│       ├── .claude-plugin/
│       │   └── plugin.json       # Claude Code plugin manifest
│       ├── .codex-plugin/
│       │   └── plugin.json       # Codex plugin manifest
│       ├── .mcp.json             # MCP server config (auto-bundled with plugin)
│       ├── skills/
│       │   ├── app-health-check/
│       │   ├── webhook-setup/
│       │   ├── app-review-prep/
│       │   ├── debug-webhooks/
│       │   ├── compliance-check/
│       │   ├── api-health/
│       │   ├── api-integration/
│       │   └── search-docs/
│       └── hooks/                # Session hooks (+ session-context.json)
├── AGENTS.md                    # This file
├── CLAUDE.md                    # Symlink → AGENTS.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE                      # MIT
└── README.md
```

## Guidelines for agents working in this repo

- **Skills are workflow-oriented.** Each skill orchestrates multiple MCP tool calls in a logical sequence, not just wrapping a single tool.
- **Identify the app first.** Ask for the app **name or ID**. If given a name (or no ID), resolve it to an `app_id` via `devtools_app_list` (action `list`). Every MCP tool except `devtools_discovery` and `devtools_app_list` requires an `app_id`.
- **Run independent calls in parallel.** Most skills collect data from multiple tools concurrently.
- **Report failures per-section.** If one MCP call fails, include the error in the relevant report section rather than aborting.
- **Cross-reference other skills.** When findings suggest a deeper investigation, point the user to the relevant skill.
