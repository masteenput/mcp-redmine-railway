FROM python:3.12-slim
RUN pip install mcp-proxy mcp-redmine
EXPOSE 8080
CMD ["mcp-proxy", "--pass-environment", "--port=8080", "--sse-host=0.0.0.0", "mcp-redmine"]