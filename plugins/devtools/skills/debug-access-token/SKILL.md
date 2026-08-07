---
name: debug-access-token
description: "Diagnose a Meta access token problem (expired, wrong scopes, wrong app, invalid) WITHOUT the token ever entering the agent or AI provider context. Guides the developer to inspect the token themselves via the Access Token Debugger web tool or the public debug_token Graph API, then interprets the returned metadata. Use when an API call fails with an auth/OAuthException error (e.g. code 190) or a token isn't behaving as expected."
allowed-tools: mcp__devtools__devtools_discovery
license: MIT
---

# Debug Access Token

Help a developer figure out why a Meta access token is failing — without ever handling the raw token yourself.

## Security first — never handle a live token

An access token is a bearer credential: whoever holds it can act as its owner. Anything pasted into this chat enters the agent's context and is transmitted to the AI provider (logs, history, retention). Treat a token like a password.

1. **Do NOT ask the developer to paste an access token (or an app secret) into this chat.** Inspect tokens using the developer-run options below, and ask only for the resulting metadata.
2. **If a token was already pasted**, tell the developer to **revoke/rotate it** (Graph API Explorer, or the app dashboard → regenerate), then continue with the metadata flow below using a fresh token.

## Workflow

1. **Confirm the symptom.** Ask what failed:
   - The error `code` and `subcode` (e.g. `190` / `463`)
   - Which endpoint/request failed
   - Which app the call was made with, and what the token is expected to do (which permissions/scopes)

2. **Have the developer inspect the token themselves.** Offer either option — both run in the developer's own environment and return only metadata, never routing the token through this agent:

   - **A. Access Token Debugger (web):** open [https://developers.facebook.com/tools/debug/accesstoken/](https://developers.facebook.com/tools/debug/accesstoken/), paste the token there (a Meta first-party surface, not this agent), and read the results panel.
   - **B. `debug_token` Graph API via the bundled script:** this skill ships a ready-to-run script, `scripts/debug_token_probe.py`, that reads the token and app secret from **environment variables** (by name — never their values) and prints only redacted metadata; the developer sets the env vars and runs it in their own shell, then brings back only the printed JSON. See the **Using the `debug_token` script** section below for how to run it and the expected output. Reference: [debug_token docs](https://developers.facebook.com/docs/graph-api/reference/debug_token/). Never ask the developer to send you the token or the app secret.

   If the developer needs exact, current steps, use `devtools_discovery` (action `search_docs`) to fetch the latest Access Token Debugger / `debug_token` documentation.

3. **Ask only for the redacted metadata.** Request they copy back the debug output with PII removed. Keep: `is_valid`, `type`, `app_id`, `application`, `issued_at`, `expires_at`, `data_access_expires_at`, `scopes` / `granular_scopes`, and any `error.code` / `error.subcode` / `error.message`. **Tell them to redact `user_id` and any profile IDs** — you do not need them to diagnose the failure. (The bundled script already emits only this allow-listed, redacted subset.) See **Using the `debug_token` script** below for an example of the token-free output to expect.

4. **Interpret the metadata and report** (format below).

## Using the `debug_token` script (Option B)

When the developer prefers the API over the web debugger, point them at the script
bundled with this skill, `scripts/debug_token_probe.py`. It reads the credentials
from **environment variables in the developer's own shell** — **by name**, never
their values — so no token or secret ever appears in the chat, in a script you
author, or on a command line. The shell provides the values at run time, and the
script prints only redacted metadata. Do not re-derive or paste the script into the
chat; it is already checked in and vetted — just tell the developer how to run it.

**Give the developer the absolute path.** The script lives inside the installed
plugin, not in the developer's working directory, so a relative path will not
resolve for them. Substitute the absolute path of this skill's directory — you know
it, having just read `SKILL.md` from there — wherever `<skill-dir>` appears below.

Have them run this in a **throwaway shell, not the shell they start their agent
from**: an exported variable is inherited by every process that shell launches, so a
token left exported can reach an agent started later from the same terminal.

Prompt for the two secrets. `-s` hides the input, so neither value is echoed to
the screen or typed on a command line. **The prompt syntax differs by shell** —
in zsh, `read -p` means "read from a coprocess", not "print this prompt", so the
bash form fails there:

```bash
# bash
read -rsp 'Access token: ' FB_INPUT_TOKEN; echo
read -rsp 'App secret:   ' FB_APP_SECRET; echo
```

```zsh
# zsh (the macOS default)
read -rs 'FB_INPUT_TOKEN?Access token: '; echo
read -rs 'FB_APP_SECRET?App secret:   '; echo
```

Then, in either shell:

```bash
export FB_APP_ID='<your app id>'
export FB_INPUT_TOKEN FB_APP_SECRET

python3 <skill-dir>/scripts/debug_token_probe.py

unset FB_INPUT_TOKEN FB_APP_SECRET FB_APP_ID
```

The script needs only the Python 3 standard library — no packages to install. The
developer pastes back only the printed JSON. Example of the token-free output to
expect — note there is **no token, no app secret, and no `user_id`**; that is the
whole point:

```json
{
  "is_valid": true,
  "type": "USER",
  "app_id": "1234567890123456",
  "application": "Example App",
  "issued_at": 1785000000,
  "expires_at": 1792800000,
  "data_access_expires_at": 1800000000,
  "scopes": ["public_profile", "email", "pages_show_list", "pages_read_engagement"]
}
```

## Interpretation & Report Format

**Token summary**
- Valid? Token `type` (User / Page / App / System User)?
- Owning app: does `app_id` match the app the call was made with?
- Expiry: `expires_at` in the past → expired; `0` → never expires; `data_access_expires_at` in the past → data-access window lapsed (re-auth needed).
- Scopes present vs. the scopes the failing call requires.

**Diagnosis (common cases)**

| Signal | Meaning | Fix |
|--------|---------|-----|
| `is_valid=false`, error 190 subcode 463 | Session expired | Re-authenticate the user |
| `is_valid=false`, error 190 (no subcode) | Invalid or revoked token | Re-issue the token |
| `expires_at` in the past | Expired short-lived token | Exchange for a long-lived token, or re-login |
| Required scope missing from `scopes` | Permission not granted/approved | Request the scope; run App Review (`/app-review-prep`) |
| `app_id` ≠ the calling app | Token minted for a different app | Use a token issued by the correct app |
| `type` not what the endpoint expects (User vs Page vs App) | Wrong token type | Mint the correct token type for that endpoint |

**Next steps**
- Concrete remediation for the diagnosed cause, then cross-links (below).

## Acceptable vs unacceptable usage

- ✅ Interpreting **redacted** `debug_token` metadata the developer brings back
- ✅ Linking the developer to the web Access Token Debugger
- ✅ Pointing the developer to the bundled `scripts/debug_token_probe.py` (reads the token/app secret from **environment variables** by name) for them to run themselves
- ✅ Emitting a command that references the credentials **by environment-variable
  name only** (`"$FB_INPUT_TOKEN"`), for the developer to run in their own shell
- ❌ Accepting a raw or live access token as chat input
- ❌ Asking for an app secret
- ❌ Echoing a token back, or storing a token anywhere
- ❌ Emitting a command containing a literal token or app secret — including a
  placeholder the developer substitutes. The value would land in their shell
  history and, for the life of the process, in `ps` output
- ❌ Running the `read` / `export` commands or the script **yourself**. The
  developer runs them in their own shell; you never hold the credential

## Tips

- Error code `190` is the catch-all `OAuthException`; the **subcode** disambiguates it (463 = expired, 467 = invalid, etc.). Always ask for the subcode.
- If the developer can't run `debug_token`, the web Access Token Debugger needs no setup — start there.
- Related: `/api-integration` (token types & auth setup) and `/api-health` (rate limits/quota, once the token works).
