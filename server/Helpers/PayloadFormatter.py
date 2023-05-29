"""Formatter

This file is used to format the data returned by this server

The methods available are:
- format_dates -> Returns a date as a string in format "YYYY-MM-DD"
- format_datasets -> Returns the performances for each stock in a Chart.js data object
"""

# Libraries
from datetime import datetime

def format_dates(stock_symbol, responses):
    """Formats the dates which will be used for the x-axis in the chart

    Parameters
    ----------
    stock_symbols : list
        List of the stock symbols
    responses : object
        key: stock symbol, value: the object returned by the Polygon API

    Returns
    -------
    list
        a list of dates formatted as "YYYY-MM-DD"
    """
    dates = []
    for result in responses[stock_symbol]["results"]:
        dates.append(datetime.fromtimestamp(int(result['t'])/1000).strftime('%Y-%m-%d'))
    return dates

def format_datasets(stock_symbols, performances):
    """Formats the datasets to match the Chart.js dataset object

    Parameters
    ----------
    stock_symbols : list
        List of the stock symbols
    performances : object
        The list of performances for each stock

    Returns
    -------
    list
        a list of objects formatted as Chart.js dataset objects, including the performances,
        label and color for each stock
    """
    # Adding colors that I like for the lines
    colors = ['rgba(145,199,177,1)', 'rgba(69,105,144,1)', 'rgba(222,165,75,1)']
    datasets = []
    for i, stock_symbol in enumerate(stock_symbols):
        datasets.append(
            {
                "label": stock_symbol,
                "data": performances[i],
                "fill": False,
                "borderColor": colors[i],
                "tension": 0
            },
        )
    return datasets