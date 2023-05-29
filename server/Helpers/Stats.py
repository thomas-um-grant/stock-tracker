"""Stats

This file is used to perform calculations and uncover statistics regarding the stocks tracked

The methods available are:
- calculate_performances -> Returns the performances calculated per stock
- calculate_cumulative_return -> Returns a list of cumulative returns calculated per stock
- calculate_annualized_return -> Returns a list of annualized returns calculated per stock
- calculate_annualized_volatility -> Returns a list of annualized volatility calculated per stock
"""

# Libraries
import math

def calculate_performances(stock_symbols, responses):
    """Calculates the performances of each stock

    Parameters
    ----------
    stock_symbols : list
        List of the stock symbols
    responses : object
        key: stock symbol, value: the object returned by the Polygon API

    Returns
    -------
    list
        a list of performances for each stock
    """
    performances = []

    for stock_symbol in stock_symbols:
        stock_performance = []
        deviation = 0
        hasDeviation = False

        for result in responses[stock_symbol]["results"]:
            close_price = result['c']
            if not hasDeviation:
                deviation = 100 - close_price
                hasDeviation = True

            stock_performance.append(close_price + deviation)
        
        performances.append(stock_performance)
    
    return performances

def calculate_cumulative_return(stock_symbols, stock_infos):
    """Calculates the cumulative return of each stock

    The cumulative return on the past 2 years is: (close price - open price) / open price
    Therefore we need the first and last entries of each stocks information

    Parameters
    ----------
    stock_symbols : list
        List of the stock symbols
    stock_infos : object
        key: stock symbol, value: the object returned by the Polygon API

    Returns
    -------
    list
        a list with the cumulative return of each stock
    """

    cumul_returns = []

    for stock_symbol in stock_symbols:
        open_price = stock_infos[stock_symbol]["results"][0]["o"]
        close_price = stock_infos[stock_symbol]["results"][stock_infos[stock_symbol]["resultsCount"]-1]['c']
        cumul_return = (close_price - open_price) / open_price
        cumul_returns.append(round(cumul_return.real, 3))

    return cumul_returns

def calculate_annualized_return(stock_symbols, stock_infos):
    """Calculates the annualized return of each stock

    The annualized return on the past 2 years is: ( (close price / open price)^(1 / num of years) ) -1
    Therefore we need the first and last entries of each stocks information
    To calculate the number of years, we just have to divide the num of entires epr 252, which constitue a "trading year"

    Parameters
    ----------
    stock_symbols : list
        List of the stock symbols
    stock_infos : object
        key: stock symbol, value: the object returned by the Polygon API

    Returns
    -------
    list
        a list with the annualized return of each stock
    """
    annualized_returns = []

    for stock_symbol in stock_symbols:
        open_price = stock_infos[stock_symbol]['results'][0]['o']
        close_price = stock_infos[stock_symbol]['results'][stock_infos[stock_symbol]['resultsCount']-1]['c']
        num_of_years = stock_infos[stock_symbol]['resultsCount'] / 252
        annualized_return = (pow(((close_price - open_price)/open_price),(1 / num_of_years))) - 1
        annualized_returns.append(round(annualized_return.real,3))

    return annualized_returns

def calculate_annualized_volatility(stock_symbols, stock_infos):
    """Calculates the annualized volatility of each stock

    The annualized volatility on the past 2 years is: standard deviation of ( [sum(daily % change - mean(all entries)]**2 /  (number of entries -1))
    Therefore we need to loop through all entries of each stock information to get the daily % change
    We can sum them up, divide them and finally look at the standard deviation

    Parameters
    ----------
    stock_symbols : list
        List of the stock symbols
    stock_infos : object
        key: stock symbol, value: the object returned by the Polygon API

    Returns
    -------
    list
        a list with the annualized volatility of each stock
    """
    annualized_volatilities = []

    for stock_symbol in stock_symbols:
        daily_changes = [] # => =((close_price/open_price)-1)*100

        # Create a list of [daily % change ]
        for result in stock_infos[stock_symbol]['results'][1:]:
            open_price = result['o']
            close_price = result['c']
            daily_changes.append(((close_price/open_price)-1)*100)
        # Calculate the mean
        mean_daily_changes = sum(daily_changes)/len(daily_changes)
        # Reduce each of them by the average and square it
        daily_changes = [(val-mean_daily_changes)**2 for val in daily_changes]
        # Divide by N - 1
        temp = sum(daily_changes)/(stock_infos[stock_symbol]['resultsCount']-1)
        # Now we can get the standard deviation by doing square root of the previous result
        annualized_volatility = math.sqrt(temp)
        annualized_volatilities.append(round(annualized_volatility.real,3))

    return annualized_volatilities