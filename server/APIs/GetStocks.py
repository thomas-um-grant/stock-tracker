from flask import jsonify, request
from datetime import datetime
import json

# My modules
from Helpers import PayloadFormatter as formatter
from Helpers import Stats as stats
from Adapters import PolygonAPIAdapter as polygonAPI

# Get infos for each stock
def getStonks():
    # In v1, we have a fixed set of stocks
    stock_symbols = ['AAPL', 'MSFT', 'TSLA']  
    # read from db
    stonks = readStockInfos()
    responses = {}
    
    for stock_symbol in stock_symbols:
        if stock_symbol in stonks:
            # get latest trading day
            latest_trading_day = stats.getLatestTradingDay().date()
            # latest date saved:
            latest_input = stonks[stock_symbol]['results'][stonks[stock_symbol]['resultsCount'] - 1]['t'] / 1000
            latest_date_in_db = datetime.fromtimestamp(latest_input).date()
            # Double check if there is a need to update the stocks, otherwise, return the current value of stonks
            # We know there is a need to update the stocks if the latest_trading_day is smaller or equal to the latest_date_in_db
            if latest_trading_day <= latest_date_in_db: 
                # We already have the latest infos so no need to call the API
                responses = stonks
            else:
                # Otherwise we call Polygon API to get them
                responses[stock_symbol] = polygonAPI.getStockInfos(stock_symbol)
                # Keep in in json file for now, maybe have an actual DB later on, the data is structure, might wanna go for a regular SQL
                writeStockInfos(responses)
        else:
            # Otherwise we call Polygon API to get them
            responses[stock_symbol] = polygonAPI.getStockInfos(stock_symbol)
            # Keep in in json file for now, maybe have an actual DB later on, the data is structure, might wanna go for a regular SQL
            writeStockInfos(responses)
    
    # Format dates for x-axis
    labels = formatter.formatDates(stock_symbols[0], responses) # We only need x-axis from one of the entry because all the dates will match
                                                                # TODO: Later on we could actually do some validations on that if there is a whole in their entries

    # Calculate performances for each stock symbol
    performances = stats.calculatePerformances(stock_symbols, responses)

    # Format datasets with data for y-axis
    datasets = formatter.formatDatasets(stock_symbols, performances)

    # Create return object
    data = {
                "labels": labels,
                "datasets": datasets,
            }

    return jsonify(data)

# Get infos for each stock based on params -> In dev
def getStonksV2():
    # Getting the params
    # TODO: Data validation on the date - need to be strictly lower than today and bigger than 2 years ago
    date = request.args.get("startDate")
    stock_symbols = request.args.getlist("stocks[]")

    # Getting the response for each stock symbol
    responses = {}
    for stock_symbol in stock_symbols:
        responses[stock_symbol] = polygonAPI.getStockInfos(date, stock_symbol)
    
    # Keep in json file
    writeStockInfos(responses)
    
    # Format dates for x-axis
    labels = formatter.formatDates(stock_symbols[0], responses)

    # Calculate performances for each stock symbol
    performances = stats.calculatePerformances(stock_symbols, responses)

    # Format datasets with data for y-axis
    datasets = formatter.formatDatasetsV2(stock_symbols, performances)

    # Create return object
    stonks = {
                "labels": labels,
                "datasets": datasets
            }

    return jsonify(stonks)

# Fake data to do testing
def get_latest_stocks():
    response = jsonify({
                    "labels": [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July'
                    ],
                    "datasets": [
                        {
                            "label": 'AAPL',
                            "data": [100, 39, 109, 40, 139, 80, 40],
                            "fill": False,
                            "borderColor": 'rgba(145,199,177,1)',
                            "tension": 0.1
                        },
                        {
                            "label": 'MSFT',
                            "data": [100, 45, 78, 87, 123, 145, 112],
                            "fill": False,
                            "borderColor": 'rgba(69,105,144,1)',
                            "tension": 0.1
                        },
                        {
                            "label": 'TSLA',
                            "data": [100, 80, 162, 97, 132, 80, 50],
                            "fill": False,
                            "borderColor": 'rgba(222,165,75,1)',
                            "tension": 0.1
                        }
                    ]
                })
    return response

# Get statistics on all stocks
def get_latest_stats():
    stock_symbols = ['AAPL', 'MSFT', 'TSLA']
    # read from db
    stonks = readStockInfos()
    # gather stats
    # cumulative returns
    cumul_returns = stats.calculateCumulativeReturn(stock_symbols, stonks)
    # annualized return
    annualized_returns = stats.calculateAnnualizedReturn(stock_symbols, stonks)
    #annualized volatility
    annualized_vol = stats.calculateAnnualizedVolatility(stock_symbols, stonks)
    statistics = {
        'AAPL': [cumul_returns[0], annualized_returns[0], annualized_vol[0]],
        'MSFT': [cumul_returns[1], annualized_returns[1], annualized_vol[1]],
        'TSLA': [cumul_returns[2], annualized_returns[2], annualized_vol[2]]
    }
    return jsonify(statistics)

# Read json file where I store the info gathered from the API
def readStockInfos():
    file_path = 'stockInfos.json'
    with open(file_path, 'r') as file_object:  
        return json.load(file_object) 

# Write json file
def writeStockInfos(data):
    file_path = "stockInfos.json"
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)