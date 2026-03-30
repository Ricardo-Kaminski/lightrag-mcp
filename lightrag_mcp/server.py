"""MCP server that exposes a LightRAG instance as Claude Code tools."""

import asyncio
import os
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

_HOST = os.getenv("LIGHTRAG_HOST", "localhost")
_PORT = os.getenv("LIGHTRAG_PORT", "9621")
_DEFAULT_MODE = os.getenv("LIGHTRAG_DEFAULT_MODE", "hybrid")
_BASE_URL = f"http://{_HOST}:{_PORT}"

server = Server("lightrag-mcp")


class LightRAGError(Exception):
    pass


def _health() -> bool:
    try:
        r = requests.get(f"{_BASE_URL}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def _query(question: str, mode: str) -> str:
    r = requests.post(
        f"{_BASE_URL}/query",
        json={"query": question, "mode": mode},
        timeout=60,
    )
    if r.status_code != 200:
        raise LightRAGError(f"Query failed [{r.status_code}]: {r.text}")
    return r.json()["response"]


def _insert(text: str, description: str = "") -> None:
    r = requests.post(
        f"{_BASE_URL}/documents/text",
        json={"input_text": text, "description": description},
        timeout=120,
    )
    if r.status_code != 200:
        raise LightRAGError(f"Insert failed [{r.status_code}]: {r.text}")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="query_rag",
            description="Query the local RAG knowledge base (LightRAG)",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Question or topic to search",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["local", "global", "hybrid"],
                        "default": _DEFAULT_MODE,
                        "description": (
                            "local=specific chunks, "
                            "global=broad overview, "
                            "hybrid=both (recommended)"
                        ),
                    },
                },
                "required": ["question"],
            },
        ),
        types.Tool(
            name="insert_document",
            description="Insert text into the RAG knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Document text to index",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional label for this document (e.g. filename)",
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="rag_health",
            description="Check whether the LightRAG server is reachable",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "query_rag":
        mode = arguments.get("mode", _DEFAULT_MODE)
        try:
            result = _query(arguments["question"], mode)
            return [types.TextContent(type="text", text=result)]
        except LightRAGError as e:
            return [types.TextContent(type="text", text=f"Error: {e}")]

    elif name == "insert_document":
        try:
            _insert(arguments["text"], arguments.get("description", ""))
            return [types.TextContent(type="text", text="Document indexed successfully.")]
        except LightRAGError as e:
            return [types.TextContent(type="text", text=f"Error: {e}")]

    elif name == "rag_health":
        status = "online" if _health() else "offline"
        return [types.TextContent(type="text", text=f"LightRAG server: {status} ({_BASE_URL})")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def _main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run() -> None:
    """Entry point for `lightrag-mcp` CLI command."""
    asyncio.run(_main())
