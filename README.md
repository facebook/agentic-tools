# Agentic Tools

This repo hosts the marketplace of workflow skills and plugins for the [Meta Developer Tools MCP](https://developers.facebook.com/documentation/mcp/devtools-mcp) — for developers building apps and integrations on the Meta Developer Platform (developers.facebook.com). Manage the Meta apps you build there: settings, webhooks, compliance, app review, and API health.

> [!NOTE]
> **Beta — v0.1.0 (first release).** The **Developer Tools MCP** and these skills are in **beta**: tool names, resources, and workflows may change between releases. Feedback and issues are very welcome.

This repo is structured as a **multi-plugin marketplace**: each product group ships as a self-contained plugin under `plugins/`, so it can host additional developer plugins alongside the first one, the **Developer Tools** plugin (`devtools`). The skills follow the open [Agent Skills standard](https://agentskills.io) (`SKILL.md`), so the same skills work in **Claude Code, Cursor, and Codex**.

> All skills call the remote **Developer Tools MCP** server (`https://mcp.facebook.com/devtools`). There is no standalone CLI — the skills drive the MCP for all their work, so connect it after install.

## Installation

### Claude Code

```bash
claude plugin marketplace add facebook/agentic-tools
claude plugin install devtools@facebook
```

Then connect the MCP server (its config is bundled with the plugin):

```
/mcp → connect to devtools → authenticate
```

### Cursor

Install the **Developer Tools** plugin from the Cursor marketplace, then authenticate the MCP server:

1. Open the Cursor marketplace and install the `devtools` plugin (published from this repo). The plugin bundles the skills and the **Developer Tools MCP** config.
2. Authenticate the remote **Developer Tools MCP** server (`devtools`): **Settings → MCP**, then complete the OAuth flow.

To try it before it's published, copy or symlink `plugins/devtools` to `~/.cursor/plugins/local/devtools`, then run **Developer: Reload Window**.

### Codex

Install the skills with the built-in installer, pointing it at this repo:

```text
$skill-installer
```

Then add the **Developer Tools MCP** server to `~/.codex/config.toml`:

```toml
[mcp_servers.devtools]
url = "https://mcp.facebook.com/devtools"
```

Codex will run its OAuth flow on first use. Restart Codex after editing the config.

## Skills

| Skill | Description |
|-------|-------------|
| `/app-health-check` | Full app audit — settings, security, compliance, and app review in one report |
| `/webhook-setup` | End-to-end webhook subscription wizard with test verification |
| `/app-review-prep` | App Review readiness check — requirements, privileges, and submission history |
| `/debug-webhooks` | Troubleshoot webhook delivery issues — inspect, test, and fix subscriptions |
| `/compliance-check` | Compliance audit — violations, required actions, and remediation guidance |
| `/api-health` | API health monitoring — rate limits, call volume, and deprecation warnings |
| `/api-integration` | Start a new API integration — fetches setup guides, auth, permissions, and code examples |
| `/search-docs` | Search Meta developer documentation for API guides and references |

## Architecture

```
agentic-tools/
├── .claude-plugin/
│   └── marketplace.json         # Claude Code / Codex marketplace manifest
├── .cursor-plugin/
│   └── marketplace.json         # Cursor marketplace manifest (lists plugins by source)
├── .cursor/
│   └── mcp.json                 # Developer Tools MCP config for manual Cursor setup
└── plugins/
    └── devtools/                # The Developer Tools plugin
        ├── .claude-plugin/
        │   └── plugin.json       # Claude Code plugin manifest
        ├── .cursor-plugin/
        │   └── plugin.json       # Cursor plugin manifest
        ├── .codex-plugin/
        │   └── plugin.json       # Codex plugin manifest
        ├── .mcp.json             # MCP config for Claude Code / Codex (auto-bundled)
        ├── mcp.json              # MCP config for Cursor (auto-discovered)
        ├── skills/               # Skill definitions (SKILL.md per workflow)
        │   ├── app-health-check/
        │   ├── webhook-setup/
        │   ├── app-review-prep/
        │   ├── debug-webhooks/
        │   ├── compliance-check/
        │   ├── api-health/
        │   ├── api-integration/
        │   └── search-docs/
        └── hooks/
            ├── session-init.sh       # Session-start hook
            └── session-context.json  # Context injected at session start
```

The Developer Tools MCP is a remote server — it is not bundled as a process; users authenticate it in their agent.

## License

MIT
