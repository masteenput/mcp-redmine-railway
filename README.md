# mcp-redmine-railway

Docker image serving [mcp-redmine](https://pypi.org/project/mcp-redmine/) over
MCP streamable HTTP, protected by a bearer token. Deployed on Coolify at
`https://mcp-redmine.inspectai.eu/mcp`.

## Environment

| Variable | Required | |
|---|---|---|
| `REDMINE_URL` | yes | e.g. `https://redmine.inspectai.eu` |
| `REDMINE_API_KEY` | yes | Redmine user API key |
| `MCP_AUTH_TOKEN` | yes | ≥ 32 chars; clients send `Authorization: Bearer <token>` |

The container refuses to start without `MCP_AUTH_TOKEN`.

## Coolify

- Build pack: Dockerfile, **Ports Exposes: 8080**
- Health check: `GET /status` (no auth)

## Client (Claude Code)

```sh
claude mcp add --transport http redmine https://mcp-redmine.inspectai.eu/mcp \
  --header "Authorization: Bearer $(cat ~/.config/mcp-redmine/http-token)"
```

## Updating

Bump `mcp-redmine` in `requirements.txt`. Keep versions pinned: unpinned
installs have already broken the build once (mcp 2.x vs mcp-proxy).
