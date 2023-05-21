from flask import Flask, jsonify
from flask_cors import CORS

# My modules
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

if __name__ == '__main__':
    app.run()