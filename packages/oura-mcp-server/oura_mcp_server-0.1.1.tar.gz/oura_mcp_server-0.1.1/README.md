# Oura MCP Server

This is a [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) server that provides access to the Oura API. It allows language models to query sleep, readiness, and resilience data from Oura API.

## Requirements

- Python 3.12+
- An Oura API access token
- UV (recommended) or pip

## Installation

### Using UV (Recommended)

UV is a fast, reliable Python package installer and resolver. To install and run the server with UV:

## Available Tools

The server exposes the following tools:

### Date Range Queries

- `get_sleep_data(start_date: str, end_date: str)`: Get sleep data for a specific date range
- `get_readiness_data(start_date: str, end_date: str)`: Get readiness data for a specific date range
- `get_resilience_data(start_date: str, end_date: str)`: Get resilience data for a specific date range

Dates should be provided in ISO format (`YYYY-MM-DD`).

### Today's Data Queries

- `get_today_sleep_data()`: Get sleep data for today
- `get_today_readiness_data()`: Get readiness data for today
- `get_today_resilience_data()`: Get resilience data for today

## Usage

### Claude for Desktop

Update your `claude_desktop_config.json` (locaated in `~/Library/Application\ Support/Claude/claude_desktop_config.json` on macOS and `%APPDATA%/Claude/claude_desktop_config.json` on Windows) to include the following:

```json
{
    "mcpServers": {
        "oura": {
            "command": "uv",
            "args": [
                "--directory",
                "/Users/tomek/workspace/oura-mcp-server",
                "run",
                "server.py"
            ],
            "env": {
                "OURA_API_TOKEN": "YOUR_OURA_API_TOKEN"
            }
        },
    }
}
```

## Example Queries

Once connected, you can ask Claude questions like:

- "What's my sleep score for today?"
- "Show me my readiness data for the past week"
- "How was my sleep from January 1st to January 7th?"
- "What's my resilience score today?"

## Error Handling

The server provides human-readable error messages for common issues:

- Invalid date formats
- API authentication errors
- Network connectivity problems

## License

This project is licensed under the MIT License - see the LICENSE file for details.
