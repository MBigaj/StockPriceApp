from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import sys

from machine_learning.model import activate_model

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/main", methods=['POST', 'GET'])
@cross_origin()
def get_form():
    data = request.get_json()
    days = data['days']
    company = data['company']
    print(data)
    activate_model(days, company)
    return 'done'

if __name__ == '__main__':
    app.run(debug=True)