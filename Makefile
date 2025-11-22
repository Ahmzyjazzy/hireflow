install:
	@command -v uv >/dev/null 2>&1 || { \
		echo "🚀 Installing uv..."; \
		curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; \
		source $$HOME/.local/bin/env; \
	}
	@echo "🔧 Syncing Python dependencies..."
	uv sync

dev:
	uv run adk api_server . --allow_origins="*"

mcp:
	uv run python3 -m hireflow_agent.mcp_server.server

playground:
	uv run adk web --port 8501
