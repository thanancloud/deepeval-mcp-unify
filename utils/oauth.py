"""
Python-native OAuth 2.0 Authorization Code + PKCE flow for the CloudBees MCP server.

Discovers endpoints from the server's OAuth metadata, opens a local callback server
on port 3000, launches a headed Playwright browser for login, and caches tokens
in .auth-tokens.json. Re-uses cached tokens on subsequent runs; re-runs full flow
if expired.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import secrets
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from typing import Optional

import httpx
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv(Path(__file__).parent / ".env")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://mcp.saas-qa.beescloud.com/v1/mcp")
CLIENT_ID = "public-mcp-client"
REDIRECT_URI = "http://localhost:3000/oauth/callback"
TOKEN_CACHE = Path(__file__).parent.parent / ".auth-tokens.json"


def _generate_pkce() -> tuple[str, str]:
    """Return (code_verifier, code_challenge)."""
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


class _CallbackCapture:
    """Thread-safe holder for the authorization code captured via the redirect."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.code: Optional[str] = None
        self._loop = loop
        self._event = asyncio.Event()

    def set(self, code: str) -> None:
        self.code = code
        self._loop.call_soon_threadsafe(self._event.set)

    async def wait(self, timeout: float = 120.0) -> str:
        await asyncio.wait_for(self._event.wait(), timeout=timeout)
        assert self.code is not None
        return self.code


def _start_callback_server(capture: _CallbackCapture) -> HTTPServer:
    """Start a one-shot HTTP server on port 3000 that captures the OAuth code."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            params = dict(urllib.parse.parse_qsl(parsed.query))
            code = params.get("code", "")

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h2>Authorization successful &mdash; you may close this tab.</h2></body></html>"
            )

            if code:
                capture.set(code)

        def log_message(self, *_args: object) -> None:
            pass  # suppress request logs

    server = HTTPServer(("localhost", 3000), Handler)
    thread = Thread(target=server.handle_request, daemon=True)
    thread.start()
    return server


class MCPOAuthClient:
    """Full OAuth 2.0 authorization-code + PKCE flow for the CloudBees MCP server."""

    def __init__(self, server_url: str = MCP_SERVER_URL) -> None:
        self._server_url = server_url.rstrip("/")
        self._auth_url: Optional[str] = None
        self._token_url: Optional[str] = None

    # ── Discovery ──────────────────────────────────────────────────────────────

    async def _discover(self) -> None:
        """Load OAuth metadata from the server."""
        base = self._server_url.replace("/v1/mcp", "")
        async with httpx.AsyncClient() as client:
            # Step 1: try oauth-protected-resource → follow authorization_servers link
            try:
                resp = await client.get(f"{base}/.well-known/oauth-protected-resource", timeout=10)
                if resp.status_code == 200:
                    auth_server = resp.json().get("authorization_servers", [None])[0]
                    if auth_server:
                        meta_resp = await client.get(
                            f"{auth_server}/.well-known/oauth-authorization-server", timeout=10
                        )
                        if meta_resp.status_code == 200:
                            meta = meta_resp.json()
                            self._auth_url = meta["authorization_endpoint"]
                            self._token_url = meta["token_endpoint"]
                            return
            except Exception:
                pass

            # Step 2: fall back to direct well-known paths on the MCP host
            for url in [
                f"{self._server_url}/.well-known/oauth-authorization-server",
                f"{base}/.well-known/oauth-authorization-server",
            ]:
                try:
                    resp = await client.get(url, timeout=10)
                    if resp.status_code == 200:
                        meta = resp.json()
                        self._auth_url = meta["authorization_endpoint"]
                        self._token_url = meta["token_endpoint"]
                        return
                except Exception:
                    continue

        raise RuntimeError(
            f"Could not discover OAuth metadata from {self._server_url}. "
            "Check MCP_SERVER_URL and network connectivity."
        )

    # ── Token cache ────────────────────────────────────────────────────────────

    def _load_cached(self) -> Optional[dict]:
        if not TOKEN_CACHE.exists():
            return None
        try:
            data = json.loads(TOKEN_CACHE.read_text())
            expires_at = data.get("issued_at", 0) + data.get("expires_in", 0) * 1000
            # Treat tokens as expired 60 s early
            if time.time() * 1000 > expires_at - 60_000:
                return None
            return data
        except Exception:
            return None

    def is_token_expiring_soon(self, buffer_seconds: int = 120) -> bool:
        """Return True if the cached token is absent or expires within buffer_seconds."""
        cached = self._load_cached()
        if cached is None:
            return True
        expires_at = cached.get("issued_at", 0) + cached.get("expires_in", 0) * 1000
        return time.time() * 1000 > expires_at - buffer_seconds * 1000

    def _save_tokens(self, tokens: dict) -> None:
        tokens["issued_at"] = int(time.time() * 1000)
        TOKEN_CACHE.write_text(json.dumps(tokens, indent=2))

    # ── Browser flow ───────────────────────────────────────────────────────────

    async def _run_browser_flow(self, auth_url: str, capture: _CallbackCapture) -> None:
        email = os.getenv("MCP_TEST_USER_EMAIL", "")
        password = os.getenv("MCP_TEST_USER_PASSWORD", "")
        if not email or not password:
            raise RuntimeError(
                "MCP_TEST_USER_EMAIL and MCP_TEST_USER_PASSWORD must be set in .env"
            )

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto(auth_url)

            await page.get_by_role("textbox", name="Email").fill(email)
            await page.locator("#loginButton").click()
            await page.get_by_role("textbox", name="Password").fill(password)
            await page.locator("#loginButton").click()

            # Org selector — required to embed userSelectedOrganization claim in the token
            await page.get_by_role("button", name="Continue").click(timeout=20000)

            # Wait until the callback server captures the code
            await capture.wait(timeout=120.0)

            await browser.close()

    # ── Token exchange ─────────────────────────────────────────────────────────

    async def _exchange_code(self, code: str, verifier: str) -> dict:
        assert self._token_url, "Discover must be called first"
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "code_verifier": verifier,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()

    # ── Public API ─────────────────────────────────────────────────────────────

    async def refresh_access_token(self) -> str:
        """Exchange the cached refresh_token for a new access_token. No browser needed.

        Falls back to the full browser flow if no refresh_token is cached or if
        the refresh request is rejected (e.g. refresh token also expired).
        """
        cached = json.loads(TOKEN_CACHE.read_text()) if TOKEN_CACHE.exists() else {}
        refresh_token = cached.get("refresh_token")
        if not refresh_token:
            return await self.get_access_token()

        await self._discover()
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": CLIENT_ID,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )
            if resp.status_code != 200:
                return await self.get_access_token()
            tokens = resp.json()
        self._save_tokens(tokens)
        return tokens["access_token"]

    async def get_access_token(self) -> str:
        """Return a valid access token, running the full OAuth flow if needed."""
        cached = self._load_cached()
        if cached:
            return cached["access_token"]

        await self._discover()

        verifier, challenge = _generate_pkce()
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
        auth_url = f"{self._auth_url}?{urllib.parse.urlencode(params)}"

        capture = _CallbackCapture(asyncio.get_event_loop())
        _start_callback_server(capture)

        await self._run_browser_flow(auth_url, capture)

        code = capture.code
        assert code, "OAuth callback did not return an authorization code"

        tokens = await self._exchange_code(code, verifier)
        self._save_tokens(tokens)
        return tokens["access_token"]
