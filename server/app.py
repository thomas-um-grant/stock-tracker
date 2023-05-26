from flask import Flask, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler

# My modules
from Adapters import PolygonAPIAdapter as polygonAPI
import  APIs.GetStocks as stocksEndpoint

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

# cron job to collect latest stock infos
@scheduler.task('cron', id='update_stocks', minute='*')
def update_stocks():
    print(f'Updating stocks...')
    stock_symbols = ['AAPL', 'MSFT', 'TSLA'] 
    responses = {}
    for stock_symbol in stock_symbols:
        responses[stock_symbol] = polygonAPI.getStockInfos(stock_symbol)
    # Keep in in json file for now, maybe have an actual DB later on, the data is structure, might wanna go for a regular SQL
    stocksEndpoint.writeStockInfos(responses)

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


scheduler.start()

if __name__ == '__main__':
    # Run the Flask app
    app.run()