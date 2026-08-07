# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public issue for security vulnerabilities.**

Instead, please report security issues by emailing security@meta.com, or using the repository's private vulnerability reporting feature on GitHub.

## Scope

This plugin is primarily skill definitions (structured prompts) that guide AI agents to use the Meta Developer Tools MCP server. The MCP server handles authentication and authorization independently. Agents are not given a shell by these skills, and no skill accepts a credential as input.

One skill, `debug-access-token`, bundles a helper script (`scripts/debug_token_probe.py`) that **you** run in **your own** shell. It reads an access token and app secret from environment variables you set, calls the public `debug_token` Graph API, and prints only a redacted, non-PII subset of the response. The agent never executes it and never sees the credential values — only the redacted output you choose to share back.

Security concerns most relevant to this project:

- Skill definitions that could lead to unintended data exposure
- MCP configuration templates with hardcoded or leaked credentials
- Prompt injection vulnerabilities in skill workflows
- Any path by which a bundled script could disclose a credential it was given

## Response

Meta will acknowledge receipt of your report and follow up with next steps.
