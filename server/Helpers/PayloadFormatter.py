from datetime import datetime

def formatDates(stock_symbol, responses):
    dates = []
    for result in responses[stock_symbol]["results"]:
        dates.append(datetime.fromtimestamp(int(result['t'])/1000).strftime('%Y-%m-%d'))
    return dates

def formatDatasets(stock_symbols, performances):
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
    

# Essentially doing the same thing than v1, but I want to randomize the color, and make it all dynamic
def formatDatasetsV2():
    pass



    datasets = []

    for stock_symbol in stock_symbols:
        stock_performance = []
        deviation = 0
        hasDeviation = False

        for result in responses[stock_symbol]["results"]:
            weight_price_increase = 8
            open_price = result['o']
            close_price = result['c']

            weight_price_fluctuaction = 1
            high_price = result['h']
            low_price = result['l']

            performance = (close_price - open_price)*weight_price_increase - (high_price - low_price)*weight_price_fluctuaction

            if not hasDeviation:
                deviation = 100 - performance
                hasDeviation = True

            # TODO: Set back to: stock_performance.append(performance + deviation)
            stock_performance.append(close_price)
        
        datasets.append({ "name": stock_symbol, "performances": stock_performance })
    
    return datasets
        