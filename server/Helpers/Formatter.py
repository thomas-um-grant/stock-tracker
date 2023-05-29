"""Formatter

This file is used to format the data returned by this server

The methods available are:
- format_dates -> Returns a date as a string in format "YYYY-MM-DD"
- format_datasets -> Returns the performances for each stock in a Chart.js data object
"""

# Libraries
from datetime import datetime

def format_dates(responses):
    """Formats the dates which will be used for the x-axis in the chart

    Parameters
    ----------
    responses : object
        key: stock symbol, value: the object returned by the Polygon API

    Returns
    -------
    list
        a list of dates formatted as "YYYY-MM-DD"
    """
    dates = []
    # Find the largest dataset
    largest_set = 0
    symbol_for_xaxis = ''
    for symbol, data in responses.items():
        if data["resultsCount"] > largest_set:
            symbol_for_xaxis = symbol

    # Get all the Unix timestamps to create the x-axis with dates in "YYYY-MM-DD" format         
    for result in responses[symbol_for_xaxis]["results"]:
        dates.append(datetime.fromtimestamp(int(result['t'])/1000).strftime('%Y-%m-%d'))
    return dates

def format_datasets(performances):
    """Formats the datasets to match the Chart.js dataset object

    Parameters
    ----------
    performances : object
        The list of performances for each stock

    Returns
    -------
    list
        a list of objects formatted as Chart.js dataset objects, including the performances,
        label and color for each stock
    """

    colors = ['rgba(145,199,177,1)', # Cambrige Blue
              'rgba(69,105,144,1)', # Lapis Lazuli
              'rgba(222,165,75,1)', # Earth Yellow
              'rgba(91,96,87,1)', # Ebony
              'rgba(242,166,90,1)', # Sandy Brown
              'rgba(119,47,26,1)', # Sienna
              'rgba(199,234,228,1)', # Mint Green
              'rgba(252,188,184,1)', # Melon
              'rgba(255,217,114,1)', # Jasmine
              'rgba(191,204,148,1)', # Sage
              'rgba(52,73,102,1)', # Indigo Dye
              'rgba(202,207,214,1)', # French Gray
            ]
    datasets = []
    color = 0
    for stock_symbol, performance in performances.items():
        datasets.append(
            {
                "label": stock_symbol,
                "data": performance,
                "fill": False,
                "borderColor": colors[color],
                "tension": 0
            },
        )
        color += 1
        if color == len(colors):
            color = 0

    return datasets