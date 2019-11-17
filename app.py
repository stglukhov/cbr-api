#!/usr/bin/env python3
"""Custom API for CBR"""
import json
import requests
import xmltodict
from datetime import datetime, timedelta
from flask import jsonify
from flask import Flask

__author__ = "sglukhov"
__version__ = "0.3.1"

app = Flask(__name__)
URL = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='

def parse_xml(code, date):
    """Get XML from CBR API and parse it for CharCode"""

    date = "{}/{}/{}".format(date.split('-')[2], date.split('-')[1], date.split('-')[0])
    r = requests.get(URL + date)
    xml_dict = xmltodict.parse(r.text)

    for i in xml_dict["ValCurs"]["Valute"]:
        if i["CharCode"] == code:
            return i["Value"]

@app.route('/')
def index():
    return 'Server Works!'
  
@app.route('/greet')
def say_hello():
    return 'Hello from Server'

@app.route('/api/rate/<code>')
def get_rate(code):
    """Check code's rate for tomorrow"""

    tomorrow = datetime.today() + timedelta(days=1)
    date = tomorrow.strftime("%Y-%m-%d")
    rate = parse_xml(code, date)
    answer = { "code": code, "rate": rate, "date": date  }
    return jsonify(answer)

@app.route('/api/rate/<code>/<date>')
def get_rate_date(code, date):
    """Check code's rate for particular date"""

    rate = parse_xml(code, date)
    answer = { "code": code, "rate": rate, "date": date  }
    return jsonify(answer)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
