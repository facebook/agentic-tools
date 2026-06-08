# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public issue for security vulnerabilities.**

Instead, please report security issues by emailing security@meta.com, or using the repository's private vulnerability reporting feature on GitHub.

## Scope

This plugin does not execute arbitrary code or handle credentials directly. It provides skill definitions (structured prompts) that guide AI agents to use the Meta Developer Tools MCP server. The MCP server handles authentication and authorization independently.

Security concerns most relevant to this project:

- Skill definitions that could lead to unintended data exposure
- MCP configuration templates with hardcoded or leaked credentials
- Prompt injection vulnerabilities in skill workflows

## Response

Meta will acknowledge receipt of your report and follow up with next steps.
