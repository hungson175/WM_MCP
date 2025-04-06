from mcp.server.fastmcp import FastMCP
from data.fred_client import FredClient
from data.fred_map_series import FRED_SERIES_DETAILS
from typing import Dict, List, Optional
import pandas as pd

# Create MCP server
mcp = FastMCP("FRED Macroeconomic Data Server")

# Initialize FRED client
fred_client = FredClient()

# Resource to get available series information
@mcp.resource("file://series/available")
def get_available_series() -> Dict:
    """Get information about all available FRED series"""
    return FRED_SERIES_DETAILS

# # Resource to get series info
# @mcp.resource("series/info/{series_id}")
# def get_series_info(series_id: str) -> Dict:
#     """Get detailed information about a specific FRED series"""
#     if series_id not in FRED_SERIES_DETAILS:
#         raise ValueError(f"Series {series_id} not found")
#     return FRED_SERIES_DETAILS[series_id]

# Tool to fetch series data
@mcp.tool()
def fetch_series_data(series_id: str, n_observations: int = 12) -> Dict:
    """
    Fetch data for a specific FRED series
    
    Args:
        series_id: The FRED series identifier
        n_observations: Number of most recent observations to fetch (default: 12)
    
    Returns:
        Dict containing series data and metadata
    """
    if series_id not in FRED_SERIES_DETAILS:
        raise ValueError(f"Series {series_id} not found")
    
    series_info = FRED_SERIES_DETAILS[series_id]
    frequency = series_info['frequency_code']
    
    # Get the data
    df = fred_client.get_series_data(
        series_id=series_id,
        frequency=frequency,
        n_limit=n_observations
    )
    
    # Convert to dictionary format
    data = {
        'series_id': series_id,
        'description': series_info['description'],
        'frequency': frequency,
        'observations': df.reset_index().to_dict(orient='records')
    }
    
    return data

# Tool to search series
@mcp.tool()
def search_series(search_text: str, limit: int = 10) -> List[Dict]:
    """
    Search for FRED series based on text
    
    Args:
        search_text: Text to search for in series descriptions
        limit: Maximum number of results to return
    
    Returns:
        List of matching series information
    """
    results = fred_client.search_series(search_text=search_text, limit=limit)
    return results

if __name__ == "__main__":
    # For development/testing
    mcp.run("stdio")
