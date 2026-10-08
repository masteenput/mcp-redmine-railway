"""Serve mcp-redmine over streamable HTTP behind a bearer-token check.

The server holds a Redmine API key, so the public endpoint must never be
reachable without MCP_AUTH_TOKEN. Routes:
  /mcp     MCP streamable HTTP (token required)
  /status  health check (open)
"""
import hmac
import os
import sys

import uvicorn

token = os.environ.get("MCP_AUTH_TOKEN", "")
if len(token) < 32:
    sys.exit("MCP_AUTH_TOKEN must be set (at least 32 characters)")

from mcp_redmine.server import mcp  # noqa: E402  (needs REDMINE_* env)

OPEN_PATHS = {"/status"}


class BearerAuth:
    def __init__(self, app, token: str) -> None:
        self.app = app
        self.expected = f"Bearer {token}".encode()

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            if scope["path"] in OPEN_PATHS:
                await self._reply(send, 200, b"ok")
                return
            given = dict(scope["headers"]).get(b"authorization", b"")
            if not hmac.compare_digest(given, self.expected):
                await self._reply(send, 401, b"Unauthorized", [(b"www-authenticate", b"Bearer")])
                return
        await self.app(scope, receive, send)

    @staticmethod
    async def _reply(send, status, body, headers=()):
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [(b"content-type", b"text/plain"), *headers],
        })
        await send({"type": "http.response.body", "body": body})


# host="0.0.0.0" leaves DNS-rebinding host checks off, which the public
# domain behind Coolify's proxy needs; the bearer token guards access instead.
app = BearerAuth(mcp.streamable_http_app(host="0.0.0.0"), token)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")),
                proxy_headers=True, forwarded_allow_ips="*")
