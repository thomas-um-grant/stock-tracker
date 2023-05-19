from flask import Flask, jsonify
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# testing get_stocks
@app.route('/stocks', methods=['GET'])
def get_stocks():
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
                        "label": 'Data One',
                        "borderColor": '#f87979',
                        "data": [40, 39, 10, 40, 39, 80, 40]
                    }
                    ]
                })
    print(response)
    return response


if __name__ == '__main__':
    app.run()