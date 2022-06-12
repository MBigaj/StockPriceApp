import requests
from flask import Flask
import json

app = Flask(__name__)

@app.route('/main', methods=['POST', 'GET'])
def get_form():
    pass


if __name__ == '__main__':
    app.run(debug=True)