"""Polygon API Adapter

This file is used to connect and gather data from the Polygon API

The methods available are:
- getStockInfos -> Returns a Polygon stock information object regarding a stock
"""

# Libraries
from datetime import date, timedelta
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def getStockInfos(stock_symbol):
    """Get a stock information from the Polygon API

    Parameters
    ----------
    stock_symbol : string
        A stock symbol

    Returns
    -------
    Object
        An object containing information of a stock results over time (daily)
    """
    # With the free tier, I can only go back 2 years max (504 days since there are 252 traiding days in a year), so even if I request the last 1000 days I'll be limited :(
    sDate = (date.today() + timedelta(days=-1000)).strftime("%Y-%m-%d")
    eDate = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d") # Can't get today's date (no stats registered yet, makes sense)

    # TODO: That apiKey gotta go somewhere safer, shouldn't be hardcoded, Docker secrets is the way
    # Gotta check this out later: https://docs.docker.com/engine/swarm/secrets/
    url = 'https://api.polygon.io/v2/aggs/ticker/'+ stock_symbol +'/range/1/day/'+ sDate +'/'+ eDate +'?apiKey=UiIW3EHMLXHQ6_kM8tkG4frd66mrJcXo'

    # Retries
    retry_strategy = Retry(
            total=3,  # Number of retries
            backoff_factor=65,  # Delay between retries (1min because I use a free tier so I only can do 5 calls per min)
            status_forcelist=[429, 500, 502, 503, 504]  # HTTP status codes to retry
        )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    session = requests.Session()
    session.mount('https://', adapter)
    
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
        return response.json()  # The API returns JSON data that I will use and format later on
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None