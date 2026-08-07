#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Diagnose a Meta access token via the debug_token Graph API — safely.

Reads three values from environment variables set in your OWN shell, so no
credential is ever written into this file, onto a command line, or into an
agent chat:

    FB_INPUT_TOKEN   the access token you want to debug (the "subject")
    FB_APP_ID        the app id that owns the integration
    FB_APP_SECRET    that app's secret (used only to build the app access token)

debug_token takes TWO tokens: the token under test (input_token) and a SEPARATE
app credential (access_token = FB_APP_ID|FB_APP_SECRET) that authorizes the call
— the token cannot debug itself.

Only a redacted, non-PII subset of the response is printed to stdout as JSON:
user_id and any granular_scopes target ids are dropped. The raw token and app
secret are never printed, even on error.

Usage — run this in a throwaway shell, not the one you start an agent from: an
exported variable is inherited by every process that shell launches.

    # bash (-s hides the input so it is never echoed or typed on a command line)
    read -rsp 'Access token: ' FB_INPUT_TOKEN; echo
    read -rsp 'App secret:   ' FB_APP_SECRET; echo

    # zsh, where -p instead means "read from a coprocess"
    read -rs 'FB_INPUT_TOKEN?Access token: '; echo
    read -rs 'FB_APP_SECRET?App secret:   '; echo

    # then, in either shell
    export FB_APP_ID='<your app id>'
    export FB_INPUT_TOKEN FB_APP_SECRET
    python3 /path/to/debug_token_probe.py
    unset FB_INPUT_TOKEN FB_APP_SECRET FB_APP_ID
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH_URL = "https://graph.facebook.com/debug_token"

# Allow-list of fields we surface. debug_token can carry identifying values in
# fields we don't anticipate, so we allow-list rather than deny-list — a
# deny-list would leak any field we forgot to name.
ALLOWED_FIELDS = (
    "is_valid",
    "type",
    "app_id",
    "application",
    "issued_at",
    "expires_at",
    "data_access_expires_at",
    "scopes",
    "error",
)


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"error: environment variable {name} is not set")
    return value


def _scrub(text: str, *secrets: str) -> str:
    # Graph error strings are server-controlled free text, and everything this
    # script prints is meant to be pasted back into an agent chat. Scrubbing at
    # the single output choke point makes "never printed, even on error" true by
    # construction rather than by inspection of every branch.
    for secret in secrets:
        text = text.replace(secret, "<redacted>")
    return text


def _redact(data: dict) -> dict:
    out = {field: data[field] for field in ALLOWED_FIELDS if field in data}
    # granular_scopes can carry target_ids (PII) — keep only the scope names.
    granular = data.get("granular_scopes")
    if isinstance(granular, list):
        out["granular_scopes"] = [
            entry["scope"]
            for entry in granular
            if isinstance(entry, dict) and "scope" in entry
        ]
    return out


def main() -> None:
    input_token = _require_env("FB_INPUT_TOKEN")
    app_id = _require_env("FB_APP_ID")
    app_secret = _require_env("FB_APP_SECRET")

    # The app access token is the documented app_id|app_secret form. It stays
    # local — never logged, never printed.
    app_access_token = f"{app_id}|{app_secret}"
    query = urllib.parse.urlencode(
        {"input_token": input_token, "access_token": app_access_token}
    )
    request = urllib.request.Request(f"{GRAPH_URL}?{query}")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        # Graph returns structured JSON errors. Surface code/message only —
        # never the request URL, which embeds the credentials. The body may be
        # unreadable (OSError) or valid JSON that isn't an object, so treat
        # anything but a well-formed error dict as "no detail available".
        try:
            body = json.load(exc)
        except (ValueError, OSError):
            body = None
        err = body.get("error") if isinstance(body, dict) else None
        if not isinstance(err, dict):
            sys.exit(f"error: debug_token request failed with HTTP {exc.code}")
        detail = (
            f"(code {err.get('code', exc.code)}): {err.get('message', 'unknown error')}"
        )
        sys.exit(
            "error: debug_token request failed "
            f"{_scrub(detail, input_token, app_secret)}"
        )
    except urllib.error.URLError as exc:
        reason = _scrub(str(exc.reason), input_token, app_secret)
        sys.exit(f"error: could not reach the Graph API: {reason}")

    data = payload.get("data")
    if not isinstance(data, dict):
        sys.exit("error: debug_token returned no data for this token")
    rendered = json.dumps(_redact(data), indent=2, sort_keys=True)
    sys.stdout.write(_scrub(rendered, input_token, app_secret) + "\n")


if __name__ == "__main__":
    main()
