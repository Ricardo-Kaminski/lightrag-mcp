# lightrag-mcp

> ⚠️ This package has been superseded by [local-rag](https://github.com/Ricardo-Kaminski/local-rag).

`local-rag` includes the MCP server plus a complete RAG stack: ingestion pipeline, watcher daemon, multi-source support (Obsidian + Zotero), CLI, and optional Claude API integration.

## Migration

Replace:
```bash
pip install lightrag-mcp
```

With:
```bash
pip install local-rag-stack
```

Update your `~/.claude/settings.json`:
```json
"mcpServers": {
  "lightrag": {
    "command": "local-rag",
    "args": ["mcp"]
  }
}
```

See [local-rag](https://github.com/Ricardo-Kaminski/local-rag) for full documentation.
