import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# My library
from Adapters import PolygonAPIAdapter as polygonAPI
from APIs import GetStocks

# Declaration of the task as a function.
def updateStocks():
    print(f'Updated stocks: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
    
    stock_symbols = ['AAPL', 'MSFT', 'TSLA'] 
    responses = {}
    for stock_symbol in stock_symbols:
        responses[stock_symbol] = polygonAPI.getStockInfos(stock_symbol)
    # Keep in in json file for now, maybe have an actual DB later on, the data is structure, might wanna go for a regular SQL
    GetStocks.writeStockInfos(responses)


# Create the background scheduler
scheduler = BackgroundScheduler()
# Create the job
scheduler.add_job(func=updateStocks, trigger="interval", seconds=3600) # Updates every hour, way enough.
# Start the scheduler
scheduler.start()

# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())