"""Stocks

This file is used to get information regarding stocks and their statistics

The methods available are:
- get_stocks -> Returns the performances of each stock in a Chart.js readable format
- get_stats -> Returns the statistics for each stock tracked 
- read_stock_infos -> Returns the json where all the stock information is stored
- write_stock_infos -> Update the json where all the stock information is stored
"""

# Libraries
from flask import jsonify
import json

# My modules
from Helpers import Formatter as formatter
from Helpers import Stats as stats

def get_stocks():
    """Get infos for each stock

    Returns
    -------
    Object
        The performances of each stock in a Chart.js readable format
    """
    # read from db
    stocks = read_stock_infos()
    
    # Format dates for x-axis
    labels = formatter.format_dates(stocks)
    # TODO: Later on we could actually do some validations on that if there is a whole in their entries

    # Calculate performances for each stock symbol
    performances = stats.calculate_performances(stocks)

    # Format datasets with data for y-axis
    datasets = formatter.format_datasets(performances)

    # Create return object
    data = {
                "labels": labels,
                "datasets": datasets,
            }

    return jsonify(data)

def get_stats():
    """Get statistics on all stocks

    Returns
    -------
    Object
        The statistics for each stock tracked
    """
    # read from db
    stocks = read_stock_infos()
    # gather stats
    # cumulative returns
    cumul_returns = stats.calculate_cumulative_return(stocks)
    # annualized return
    annualized_returns = stats.calculate_annualized_return(stocks)
    #annualized volatility
    annualized_vol = stats.calculate_annualized_volatility(stocks)
    statistics = {
        'AAPL': [cumul_returns[0], annualized_returns[0], annualized_vol[0]],
        'MSFT': [cumul_returns[1], annualized_returns[1], annualized_vol[1]],
        'TSLA': [cumul_returns[2], annualized_returns[2], annualized_vol[2]]
    }
    return jsonify(statistics)

def read_stock_infos():
    """Read json file where I store the info gathered from the API

    Returns
    -------
    Object
        The stocks information stored in a json file
    """

    file_path = 'StockInfos.json'
    with open(file_path, 'r') as file_object:  
        return json.load(file_object) 

def write_stock_infos(data):
    """Write json file where I store the info gathered from the API"""

    file_path = "StockInfos.json"
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)