from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/main", methods=['POST', 'GET'])
@cross_origin()
def get_form():
    # data = request.args.get('body')
    data = request.get_json()
    days = data['days']
    company = data['company']
    print(days, company)
    return 'yssa'

if __name__ == '__main__':
    app.run(debug=True)