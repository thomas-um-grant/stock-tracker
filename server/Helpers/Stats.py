from datetime import datetime, date, timedelta
import pandas as pd
import pandas_market_calendars as mcal
import math

def calculatePerformances(stock_symbols, responses):
    performances = []

    for stock_symbol in stock_symbols:
        stock_performance = []
        deviation = 0
        hasDeviation = False

        for result in responses[stock_symbol]["results"]:
            weight_price_increase = 2
            open_price = result['o']
            close_price = result['c']

            weight_price_fluctuaction = 1
            high_price = result['h']
            low_price = result['l']

            # I thought it could be interesting to calculate the performance based on the price difference between opening and closing as well as the price fluctuation
            # giving them both a weight. I played around with it but not happy with the results, doesn't look cool on the chart, so leaving it be as the price closing

            # performance = (close_price - open_price)*weight_price_increase - (high_price - low_price)*weight_price_fluctuaction

            if not hasDeviation:
                deviation = 100 - close_price
                hasDeviation = True

            stock_performance.append(close_price + deviation)
        
        performances.append(stock_performance)
    
    return performances

# Cumulative returns
def calculateCumulativeReturn(stock_symbols, stockInfos):
    # cumulative return on the past 2 years = (close price - open price) / open price
    # so we are looking at the first and last entries in our payload
    cumul_returns = []

    for stock_symbol in stock_symbols:
        open_price = stockInfos[stock_symbol]["results"][0]["o"]
        close_price = stockInfos[stock_symbol]["results"][stockInfos[stock_symbol]["resultsCount"]-1]['c']
        cumul_return = (close_price - open_price) / open_price
        cumul_returns.append(round(cumul_return.real, 3))

    return cumul_returns

# Annualized returns
def calculateAnnualizedReturn(stock_symbols, stockInfos):
    # annualized return on the past 2 years = ( (close price / open price)^(1 / num of years) ) -1
    # so we are looking at the first and last entries in our payload again
    # to calculate the num of years, we just have to divide the num of entires epr 252, which constitue a "trading year"
    annualized_returns = []

    for stock_symbol in stock_symbols:
        open_price = stockInfos[stock_symbol]['results'][0]['o']
        close_price = stockInfos[stock_symbol]['results'][stockInfos[stock_symbol]['resultsCount']-1]['c']
        num_of_years = stockInfos[stock_symbol]['resultsCount'] / 252
        annualized_return = (pow(((close_price - open_price)/open_price),(1 / num_of_years))) - 1
        annualized_returns.append(round(annualized_return.real,3))

    return annualized_returns

# Annualized volatility
def calculateAnnualizedVolatility(stock_symbols, stockInfos):
    # annualized volatility on the past 2 years = standard deviation of ( [sum(daily % change - mean(all entries)]**2 /  (number of entries -1))
    # so we are going to loop through all entries to get the daily % change
    # Then we can sum them up, divide them and finally look at the standard deviation
    annualized_volatilities = []

    for stock_symbol in stock_symbols:
        daily_changes = [] # => =((close_price/open_price)-1)*100

        # Create a list of [daily % change ]
        for result in stockInfos[stock_symbol]['results'][1:]:
            open_price = result['o']
            close_price = result['c']
            daily_changes.append(((close_price/open_price)-1)*100)
        # Calculate the mean
        mean_daily_changes = sum(daily_changes)/len(daily_changes)
        # Reduce each of them by the average and square it
        daily_changes = [(val-mean_daily_changes)**2 for val in daily_changes]
        # Divide by N - 1
        temp = sum(daily_changes)/(stockInfos[stock_symbol]['resultsCount']-1)
        # Now we can get the standard deviation by doing square root of the previous result
        annualized_volatility = math.sqrt(temp)
        annualized_volatilities.append(round(annualized_volatility.real,3))

    return annualized_volatilities

# Get the latest trading day
def getLatestTradingDay():
    exchange_calendar = mcal.get_calendar('NYSE')
    start_date = pd.Timestamp(date.today() + timedelta(days=-10))  # Specify your desired start date
    end_date = pd.Timestamp(date.today())  # Specify your desired end date
    schedule = exchange_calendar.schedule(start_date=start_date, end_date=end_date)
    today = pd.Timestamp.today().normalize()  # Get the current date and remove the time component
    trading_days = schedule[schedule.index <= today]
    latest_trading_day = trading_days.sort_index(ascending=False).iloc[0]
    return datetime.strptime(str(latest_trading_day[len(latest_trading_day)-1]).split()[0], "%Y-%m-%d")