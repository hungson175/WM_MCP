# FRED Macroeconomic Data MCP Server

A Model Context Protocol (MCP) server that provides access to Federal Reserve Economic Data (FRED) through Claude and other LLM clients. This server exposes FRED economic data series, search capabilities, and data retrieval tools.

## Features

- Access to common FRED economic indicators (GDP, Employment, Inflation, etc.)
- Search functionality for FRED data series
- Real-time data fetching from FRED API
- Standardized data format for LLM consumption
- Built using the MCP Python SDK for seamless integration

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) - Modern Python package installer
- [Claude Desktop](https://claude.ai/download) for local usage
- FRED API Key (get one from [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/WM_mcp.git
cd WM_mcp
```

2. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies using uv:
```bash
uv pip install "mcp[cli]>=1.6.0" "colorama>=0.4.6" "numpy>=2.2.4" "pandas>=2.2.3" "python-dotenv>=1.1.0" "requests>=2.32.3"
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your FRED API key:
```
FRED_API_KEY=your_fred_api_key_here
```

## Installing in Claude Desktop

1. Make sure Claude Desktop is installed and running
2. Open Claude Desktop settings:
   - Go to Settings > Developer > Edit Config
   - Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "FRED Macroeconomic Data Server": {
      "command": "/path/to/your/.local/bin/uv",
      "args": [
        "--directory",
        "/path/to/your/WM_mcp",
        "run",
        "fred_macroeco_server.py"
      ]
    }
  }
}
```
Replace `/path/to/your/` with your actual paths. You can find uv's path by running `which uv` in terminal.

## Usage in Claude

1. First, search online for "using MCP resource in Claude Desktop Client" to understand how to include MCP resources in your conversations.

2. Once you've added the resource, you can interact with FRED data. Example prompt:
```
Use FRED APIs to get GDPs of USA last 20 years, draw chart
```

## Available Resources

- `file://series/available` - List all available FRED series and their details

## Available Tools

- `fetch_series_data` - Fetch data for any FRED series
- `search_series` - Search for FRED series by description

## Development

For development and testing:

1. Run the MCP Inspector to test the server:
```bash
mcp dev fred_macroeco_server.py
```
This allows you to inspect resources, test tools, and verify server functionality.

2. For direct server execution (to check for issues):
```bash
python fred_macroeco_server.py
```

Note: The server uses stdio transport for communication with Claude Desktop. Use the MCP Inspector during development to catch and fix any issues before deploying to Claude Desktop.

## Troubleshooting

1. If you get API key errors:
   - Verify your FRED API key is correctly set in `.env`
   - Check that the `.env` file is in the correct directory

2. If the server doesn't appear in Claude Desktop:
   - Double-check your `claude_desktop_config.json` paths
   - Ensure uv and all dependencies are installed correctly
   - Try restarting Claude Desktop

## Acknowledgments

- Federal Reserve Bank of St. Louis for providing the FRED API
- Model Context Protocol team for the MCP SDK
- Anthropic for Claude and the Claude Desktop client
