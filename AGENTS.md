# Agent Guide — Agentic Tools

This file helps AI agents navigate and use this repository effectively.

## What this repo is

A skills repository for AI coding agents that provides workflow-oriented guidance for the **Meta Social Technologies Developer Platform**. Skills wrap the Meta Social Technologies MCP server tools into higher-level workflows for app management, webhook configuration, compliance auditing, app review preparation, API health monitoring, and documentation search.

## Naming

These names are user-facing and easy to conflate. Use them exactly as written; do not invent variants.

| Thing | Canonical name | Notes |
|-------|----------------|-------|
| This repo / marketplace | **Meta Agentic Tools** | `displayName` in both marketplace manifests. Docs headings use the shorter "Agentic Tools", since the `facebook/agentic-tools` repo path already supplies the "Meta". |
| The plugin (`devtools`) | **Meta Social Technologies Developer** | Never append "plugin" to the name itself; write "the Meta Social Technologies Developer plugin". |
| The platform | **Meta Social Technologies Developer Platform** | developers.facebook.com. Also known as "Meta for Developers: Social Technologies". Note the plugin name is a prefix of this one, so avoid using both in the same sentence. |
| The MCP server | **Meta Social Technologies MCP** | Formerly "Meta Developer Tools MCP". Server id is still `devtools`; tools are still prefixed `devtools_`. |
| The skills | kebab-case ids | `app-health-check`, `webhook-setup`, etc. No branding in skill names. |

The plugin description is a single shared string, byte-identical across all five manifests. Change it in one place and propagate it to the other four.

**`devtools` is a frozen identifier, not a name.** It is the plugin id, the MCP server key in every `mcp.json`, the `mcp__devtools__devtools_*` tool namespace in all nine skills' `allowed-tools`, the `plugins/devtools/` path, and the `devtools@facebook` install target. It is pinned to the MCP endpoint `https://mcp.facebook.com/devtools`, so it does not follow display-name changes. Renaming it breaks existing installs.

## How this repo is organized

This repo is a **multi-plugin marketplace**. Two marketplace manifests live at the repo root — `.claude-plugin/marketplace.json` (Claude Code / Codex) and `.cursor-plugin/marketplace.json` (Cursor) — and each product group is a self-contained plugin under `plugins/<group>/`. Today there is one group, the **Meta Social Technologies Developer** plugin (`devtools`). To add another product group later, drop in a sibling `plugins/<group>/` and add an entry to both marketplace manifests — no restructuring.

Each plugin (`plugins/devtools/`) contains:

- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `.cursor-plugin/plugin.json` — Cursor plugin manifest
- `.codex-plugin/plugin.json` — Codex plugin manifest
- `.mcp.json` — MCP server config for Claude Code / Codex (auto-bundled with the plugin)
- `mcp.json` — MCP server config for Cursor (auto-discovered at the plugin root)
- `skills/<name>/SKILL.md` — the skills
- `hooks/` — session hooks

Skills follow the open [Agent Skills standard](https://agentskills.io) (`SKILL.md`), which Claude Code, Cursor, and Codex all understand. Agents should read `SKILL.md` for the skill invoked by the user. Each skill declares its `allowed-tools` in the frontmatter (used by Claude to scope MCP tool access; ignored harmlessly by other agents).

## MCP server dependency

All skills require the **Meta Social Technologies MCP** server to be connected — formerly named **Meta Developer Tools MCP**; the endpoint, the `devtools` plugin id, and the `devtools_` tool name prefix are unchanged. This is a remote streamable-HTTP server (`https://mcp.facebook.com/devtools`). There is no standalone CLI — the skills drive the MCP for all their work, so it must be connected first.

- **Claude Code**: `claude plugin marketplace add facebook/agentic-tools` then `claude plugin install devtools@facebook`; connect with `/mcp`. The MCP config is bundled in the plugin's `.mcp.json`.
- **Cursor**: install the `devtools` plugin from the Cursor marketplace (or load it locally from `~/.cursor/plugins/local/` while testing). The plugin auto-discovers the skills and the **Meta Social Technologies MCP** (`devtools`) from its bundled `mcp.json`; authenticate the MCP from Settings → MCP on first use.
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
| debug-access-token | `plugins/devtools/skills/debug-access-token/` | Diagnoses an access token issue (expired, wrong scopes, wrong app, invalid) without the token ever entering the agent context — guides the developer to inspect it via the web debugger or `debug_token` API and interprets the returned metadata. |

## Directory structure

```
.
├── server.json                  # Public MCP registry listing (registry.modelcontextprotocol.io)
├── .github/
│   └── workflows/
│       └── publish-mcp-registry.yml  # Publishes server.json to the registry via GitHub OIDC
├── .claude-plugin/
│   └── marketplace.json         # Claude Code / Codex marketplace manifest
├── .cursor-plugin/
│   └── marketplace.json         # Cursor marketplace manifest (lists plugins by source)
├── .cursor/
│   └── mcp.json                 # Meta Social Technologies MCP config for manual Cursor setup
├── plugins/
│   └── devtools/                # The Meta Social Technologies Developer plugin
│       ├── .claude-plugin/
│       │   └── plugin.json       # Claude Code plugin manifest
│       ├── .cursor-plugin/
│       │   └── plugin.json       # Cursor plugin manifest
│       ├── .codex-plugin/
│       │   └── plugin.json       # Codex plugin manifest
│       ├── .mcp.json             # MCP config for Claude Code / Codex (auto-bundled)
│       ├── mcp.json              # MCP config for Cursor (auto-discovered)
│       ├── skills/
│       │   ├── app-health-check/
│       │   ├── webhook-setup/
│       │   ├── app-review-prep/
│       │   ├── debug-webhooks/
│       │   ├── compliance-check/
│       │   ├── api-health/
│       │   ├── api-integration/
│       │   ├── search-docs/
│       │   └── debug-access-token/
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
