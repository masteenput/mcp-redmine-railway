FROM python:3.12-slim

RUN pip install mcp-proxy mcp-redmine

EXPOSE 8080

CMD ["sh", "-c", "REDMINE_URL=$REDMINE_URL REDMINE_API_KEY=$REDMINE_API_KEY mcp-proxy --port=8080 --sse-host=0.0.0.0 mcp-redmine"]