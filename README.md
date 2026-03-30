# lightrag-mcp

> MCP server for [LightRAG](https://github.com/HKUDS/LightRAG) — expose your local knowledge base to Claude Code in 3 lines

[![PyPI](https://img.shields.io/pypi/v/lightrag-mcp)](https://pypi.org/project/lightrag-mcp/)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple)](https://modelcontextprotocol.io)

## What is this?

`lightrag-mcp` is a lightweight [MCP server](https://modelcontextprotocol.io) that connects Claude Code to any running [LightRAG](https://github.com/HKUDS/LightRAG) instance. It adds three tools to Claude Code: `query_rag`, `insert_document`, and `rag_health`.

No configuration files. No cloud. Configure with environment variables.

## Requirements

- A running [LightRAG server](https://github.com/HKUDS/LightRAG) (default: `localhost:9621`)
- Python 3.11+

> Need a full local RAG stack? See [local-rag](https://github.com/Ricardo-Kaminski/local-rag) — a complete setup with Ollama, ingestion pipeline, and watcher daemon for Obsidian and Zotero.

## Installation

```bash
pip install lightrag-mcp
```

## Claude Code Configuration

Add to your Claude Code `settings.json` (`~/.claude/settings.json`):

```json
"mcpServers": {
  "lightrag": {
    "command": "lightrag-mcp",
    "env": {
      "LIGHTRAG_HOST": "localhost",
      "LIGHTRAG_PORT": "9621",
      "LIGHTRAG_DEFAULT_MODE": "hybrid"
    }
  }
}
```

Restart Claude Code. You now have three new tools available.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LIGHTRAG_HOST` | `localhost` | LightRAG server host |
| `LIGHTRAG_PORT` | `9621` | LightRAG server port |
| `LIGHTRAG_DEFAULT_MODE` | `hybrid` | Default query mode (`local`/`global`/`hybrid`) |

## MCP Tools

### `query_rag`
Query your knowledge base with natural language.

```
query_rag("What are the main themes in my research notes?")
query_rag("Find connections between topic A and topic B", mode="hybrid")
```

**Parameters:**
- `question` (required) — the question or topic to search
- `mode` (optional) — `local` (specific passages), `global` (broad themes), `hybrid` (both)

### `insert_document`
Index new text into the knowledge base.

```
insert_document("Your document text here...", description="report-2026-Q1.pdf")
```

**Parameters:**
- `text` (required) — document text to index
- `description` (optional) — label for this document

### `rag_health`
Check if the LightRAG server is reachable.

```
rag_health()
# → "LightRAG server: online (http://localhost:9621)"
```

## Using with uvx (no install needed)

```json
"mcpServers": {
  "lightrag": {
    "command": "uvx",
    "args": ["lightrag-mcp"]
  }
}
```

## License

MIT — see [LICENSE](LICENSE)
