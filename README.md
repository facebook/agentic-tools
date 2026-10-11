# Agentic Tools

**Meta Agentic Tools** is Meta's marketplace of agent plugins and skills for developers building apps and integrations on the Meta Social Technologies Developer Platform (developers.facebook.com), also known as Meta for Developers: Social Technologies. Manage the Meta apps you build there: settings, webhooks, compliance, app review, and API health, via the [Meta Social Technologies MCP](https://developers.facebook.com/documentation/mcp/devtools-mcp).

> [!NOTE]
> **Meta Social Technologies MCP was formerly known as Meta Developer Tools MCP.** The server endpoint, the `devtools` plugin id, and the `devtools_` tool name prefix are unchanged, so existing installs and client configurations keep working.

This repo is structured as a **multi-plugin marketplace**: each product group ships as a self-contained plugin under `plugins/`, so it can host additional developer plugins alongside the first one, the **Meta Social Technologies Developer** plugin (`devtools`). The skills follow the open [Agent Skills standard](https://agentskills.io) (`SKILL.md`), so the same skills work in **Claude Code, Cursor, and Codex**.

> All skills call the remote **Meta Social Technologies MCP** server (`https://mcp.facebook.com/devtools`). There is no standalone CLI — the skills drive the MCP for all their work, so connect it after install.

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

Install the `devtools` plugin from the Cursor marketplace, then authenticate the MCP server:

1. Open the Cursor marketplace and install the `devtools` plugin (published from this repo). The plugin bundles the skills and the **Meta Social Technologies MCP** config.
2. Authenticate the remote **Meta Social Technologies MCP** server (`devtools`): **Settings → MCP**, then complete the OAuth flow.

To try it before it's published, copy or symlink `plugins/devtools` to `~/.cursor/plugins/local/devtools`, then run **Developer: Reload Window**.

### Codex

Install the skills with the built-in installer, pointing it at this repo:

```text
$skill-installer
```

Then add the **Meta Social Technologies MCP** server to `~/.codex/config.toml`:

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
| `/debug-access-token` | Diagnose an access token issue (expired, wrong scopes, wrong app, invalid) without the token ever entering the agent context |

## Architecture

```
agentic-tools/
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
└── plugins/
    └── devtools/                # The Meta Social Technologies Developer plugin
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
        │   ├── search-docs/
        │   └── debug-access-token/
        └── hooks/
            ├── session-init.sh       # Session-start hook
            └── session-context.json  # Context injected at session start
```

The Meta Social Technologies MCP is a remote server — it is not bundled as a process; users authenticate it in their agent.

## License

MIT
