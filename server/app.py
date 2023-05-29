"""Stock Tracker App

This file is the entry point for the stock tracker backend API.
It allows the user to get up to date stock values and statistics regarding these stocks. 

This API receives calls from the front end client powered with Vue.js.

It requires the following packages to be installed within the Python environment:
- Flask-APScheduler==1.12.4
- exchange-calendars==4.2.7
- Flask==2.3.2
- Flask-Cors==3.0.10
- pandas==2.0.1
- pandas-market-calendars==4.1.4
- requests==2.30.0

The API endpoints are:
- GET /ping -> Returns "pong!" to check the server's sanity
- GET /stonks -> Returns an updated JSON object with all the stocks tracked
- GET /stats -> Returns an updated JSON object with all the stats regarding the stocks tracked

This file also contains a job running every minute to update stocks information using the Polygon API
"""

# Libraries
from flask import Flask, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler

# My modules
from Adapters import PolygonAPIAdapter as polygonAPI
import  APIs.GetStocks as stocksEndpoint

class Config:
    """Set the configuration values"""
    SCHEDULER_API_ENABLED = True

# Instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

@scheduler.task('cron', id='update_stocks', minute='*')
def update_stocks():
    """Cron job running every minute to update the stocks information using the Polygon API"""
    print(f'Updating stocks...')
    stock_symbols = ['AAPL', 'MSFT', 'TSLA'] 
    responses = {}
    for stock_symbol in stock_symbols:
        responses[stock_symbol] = polygonAPI.getStockInfos(stock_symbol)
    # Keep in in json file for now, maybe have an actual DB later on, the data is structure, might wanna go for a regular SQL
    stocksEndpoint.writeStockInfos(responses)

@app.route('/ping', methods=['GET'])
def ping_pong():
    """Endpoint to perform sanity check

    Returns
    -------
    string
        the string 'pong!'
    """
    return jsonify('pong!')

@app.route('/stonks', methods=['GET'])
def getStonks():
    """Get the most up-to-date stocks information

    Returns
    -------
    Object
        a payload formatted as the Chart.config.data object from Chart.js
    """
    return stocksEndpoint.getStonks()

# New endpoint in development
@app.route('/stonksV2', methods=['GET'])
def getStonksV2():
    return stocksEndpoint.getStonksV2()

# testing data
@app.route('/fake-stonks', methods=['GET'])
def get_latest_stocks():
    return stocksEndpoint.get_latest_stocks()

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get the latest statistics regarding the stocks

    Returns
    -------
    Object
        an object with statistics grouped by stock
    """
    return stocksEndpoint.get_latest_stats()

# Start the scheduler to run the cron job
scheduler.start()

if __name__ == '__main__':
    # Run the Flask app
    app.run()