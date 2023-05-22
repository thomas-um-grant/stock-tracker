from flask import Flask, jsonify
from flask_cors import CORS
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# My modules
from Adapters import PolygonAPIAdapter as polygonAPI
import  APIs.GetStocks as stocksEndpoint

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# Return a single payload formatted as the Chart.config.data object from Chart.js
@app.route('/stonks', methods=['GET'])
def getStonks():
    return stocksEndpoint.getStonks()

# New endpoint in development
@app.route('/stonksV2', methods=['GET'])
def getStonksV2():
    return stocksEndpoint.getStonksV2()

# testing data
@app.route('/fake-stonks', methods=['GET'])
def get_latest_stocks():
    return stocksEndpoint.get_latest_stocks()

# get statistics
@app.route('/stats', methods=['GET'])
def get_stats():
    return stocksEndpoint.get_latest_stats()

# Job to update the stocks periodically
def updateStocks():
    print(f'Updating stocks: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
    stock_symbols = ['AAPL', 'MSFT', 'TSLA'] 
    responses = {}
    for stock_symbol in stock_symbols:
        responses[stock_symbol] = polygonAPI.getStockInfos(stock_symbol)
    # Keep in in json file for now, maybe have an actual DB later on, the data is structure, might wanna go for a regular SQL
    stocksEndpoint.writeStockInfos(responses)

def startScheduler():
    # Create the background scheduler
    scheduler = BackgroundScheduler()
    # Create the job
    scheduler.add_job(func=updateStocks, trigger="interval", seconds=90)
    # Start the scheduler
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':\
    # Start the scheduler
    startScheduler()
    app.run()