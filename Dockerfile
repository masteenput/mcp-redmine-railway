FROM python:3.12-slim

# Install both packages
RUN pip install mcp-proxy mcp-redmine --break-system-packages

# Expose the SSE port
EXPOSE 8080

# mcp-proxy wraps the stdio server and exposes it as SSE
CMD ["mcp-proxy", "--pass-environment", "--port=8080", "--sse-host=0.0.0.0", "mcp-redmine"]