import os
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from colorama import Fore, Style
import time
load_dotenv()

class FredClient:
    """
    A client for interacting with the Federal Reserve Economic Data (FRED) API.
    
    This client provides methods to fetch various economic data series, categories,
    and releases from the FRED database.
    """
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FRED API client.
        
        Args:
            api_key (str, optional): FRED API key. If not provided, will look for 'FRED_API_KEY' in environment variables.
        """
        self.api_key = api_key or os.getenv('FRED_API_KEY')
        if not self.api_key:
            raise ValueError("FRED API key must be provided either directly or through FRED_API_KEY environment variable")
        
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make a request to the FRED API.
        
        Args:
            endpoint (str): API endpoint to call
            params (dict, optional): Query parameters for the request
            
        Returns:
            dict: JSON response from the API
        """
        params = params or {}
        params['api_key'] = self.api_key
        params['file_type'] = 'json'
        
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        
        response.raise_for_status()
        return response.json()
    
    def get_series(self, series_id: str, observation_start: Optional[str] = None,
                   observation_end: Optional[str] = None, frequency: Optional[str] = None,
                   aggregation_method: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch a specific time series from FRED.
        
        Args:
            series_id (str): FRED series ID
            observation_start (str, optional): Start date in YYYY-MM-DD format
            observation_end (str, optional): End date in YYYY-MM-DD format
            frequency (str, optional): Frequency of data ('d', 'w', 'm', 'q', 'sa', 'a')
            aggregation_method (str, optional): Method for aggregating higher frequency data
            
        Returns:
            pd.DataFrame: DataFrame containing the series data
        """
        params = {
            'series_id': series_id,
            'observation_start': observation_start,
            'observation_end': observation_end,
            'frequency': frequency,
            'aggregation_method': aggregation_method
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        response = self._make_request('series/observations', params)
        
        # Convert to DataFrame
        df = pd.DataFrame(response['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        return df.set_index('date')
    
    def search_series(self, search_text: str, limit: int = 1000) -> List[Dict]:
        """
        Search for FRED series based on text.
        
        Args:
            search_text (str): Text to search for
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of matching series
        """
        params = {
            'search_text': search_text,
            'limit': limit
        }
        
        response = self._make_request('series/search', params)
        return response.get('seriess', [])
    
    def get_series_info(self, series_id: str) -> Dict:
        """
        Get detailed information about a specific series.
        
        Args:
            series_id (str): FRED series ID
            
        Returns:
            Dict: Series information
        """
        params = {'series_id': series_id}
        response = self._make_request('series', params)
        return response.get('seriess', [{}])[0]
    
    def get_category_series(self, category_id: int) -> List[Dict]:
        """
        Get all series in a category.
        
        Args:
            category_id (int): FRED category ID
            
        Returns:
            List[Dict]: List of series in the category
        """
        params = {'category_id': category_id}
        response = self._make_request('category/series', params)
        return response.get('seriess', [])
    
    def get_releases(self) -> List[Dict]:
        """
        Get all FRED releases.
        
        Returns:
            List[Dict]: List of releases
        """
        response = self._make_request('releases')
        return response.get('releases', [])
    
    def get_quarterly_gdp(self, n_quarters: int = 4) -> pd.DataFrame:
        """
        Get the last n quarters of GDP data.
        
        Args:
            n_quarters (int): Number of most recent quarters to return
            
        Returns:
            pd.DataFrame: DataFrame containing quarterly GDP data with columns:
                         - date: Quarter end date
                         - value: GDP value in billions of dollars
        """
        # GDP series ID is 'GDP' in FRED
        params = {
            'series_id': 'GDP',
            'frequency': 'q',  # Quarterly frequency
            'sort_order': 'desc',  # Get most recent first
            'limit': n_quarters
        }
        
        response = self._make_request('series/observations', params)
        # Convert to DataFrame
        df = pd.DataFrame(response['observations'])[['date', 'value']]
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Sort by date in ascending order
        df = df.sort_values('date').set_index('date')
        
        return df
    
    def get_series_data(self, series_id: str, frequency: str = 'q', n_limit: int = 10) -> pd.DataFrame:
        """
        Get the last n quarters of series data.
        
        Args:
            series_id (str): FRED series ID
            frequency (str): Frequency of data ('d', 'w', 'm', 'q', 'sa', 'a')
            n_limit (int): Number of most recent observations to return
            
        Returns:
            pd.DataFrame: DataFrame containing the series data
        """
        params = {
            'series_id': series_id,
            'frequency': frequency,
            'sort_order': 'desc',
            'limit': n_limit
        }
        response = self._make_request('series/observations', params)
        df = pd.DataFrame(response['observations'])[['date', 'value']]
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.sort_values('date').set_index('date')
        return df



if __name__ == "__main__":
    from fred_map_series import FRED_SERIES_DETAILS
    
    # Initialize the client
    fred = FredClient()
    
    failed_series = []
    empty_series = []
    successful_series = []
    
    print(Fore.CYAN + "\nTesting all FRED series mappings..." + Style.RESET_ALL)
    
    # Create output directories if they don't exist
    os.makedirs('output/data', exist_ok=True)
    
    for series_id, details in FRED_SERIES_DETAILS.items():
        try:
            print(Fore.GREEN + f"Processing - Series ID: {series_id}" + Style.RESET_ALL)
            frequency = details['frequency_code']
            description = details['description']
            series = fred.get_series_data(series_id=series_id, frequency=frequency, n_limit=12)
            
            # Save to CSV regardless of whether it's empty or not
            csv_path = f"output/data/{series_id}.csv"
            series.to_csv(csv_path)
            
            if series.empty:
                empty_series.append({
                    'id': series_id,
                    'frequency': frequency,
                    'description': description
                })
            else:
                successful_series.append({
                    'id': series_id,
                    'frequency': frequency,
                    'description': description,
                    'rows': len(series)
                })
            
        except Exception as e:
            failed_series.append({
                'id': series_id,
                'frequency': frequency,
                'description': description,
                'error': str(e)
            })
            
        time.sleep(0.5)
    
    # Write summary to fred_summary.txt
    with open('output/fred_summary.txt', 'w') as f:
        f.write("FRED API Series Summary Report\n")
        f.write("============================\n\n")
        
        f.write(f"Total series tested: {len(FRED_SERIES_DETAILS)}\n")
        f.write(f"Successful series: {len(successful_series)}\n")
        f.write(f"Empty series: {len(empty_series)}\n")
        f.write(f"Failed series: {len(failed_series)}\n\n")
        
        if successful_series:
            f.write("\nSuccessful Series:\n")
            f.write("=================\n")
            for series in successful_series:
                f.write(f"\nSeries ID: {series['id']}\n")
                f.write(f"Frequency: {series['frequency']}\n")
                f.write(f"Description: {series['description']}\n")
                f.write(f"Number of rows: {series['rows']}\n")
        
        if empty_series:
            f.write("\nEmpty Series:\n")
            f.write("============\n")
            for series in empty_series:
                f.write(f"\nSeries ID: {series['id']}\n")
                f.write(f"Frequency: {series['frequency']}\n")
                f.write(f"Description: {series['description']}\n")
        
        if failed_series:
            f.write("\nFailed Series:\n")
            f.write("=============\n")
            for series in failed_series:
                f.write(f"\nSeries ID: {series['id']}\n")
                f.write(f"Frequency: {series['frequency']}\n")
                f.write(f"Description: {series['description']}\n")
                f.write(f"Error: {series['error']}\n")
    
    # Still print to console for immediate feedback
    print(Fore.GREEN + f"\nProcessing complete!" + Style.RESET_ALL)
    print(f"Results saved to output/fred_summary.txt")
    print(f"Data files saved to output/data/*.csv")
