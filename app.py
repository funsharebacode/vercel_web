from flask import Flask
import requests
import json
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/user')
def user():
    t = time.localtime()
    return r'{t}'

@app.route('/data')
def get_web_data():
    t = time.localtime()
    date = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)
    res = requests.get("https://stockapi.com.cn/v1/base/dragonTiger?date="+date)
    res_text = res.text
    stocks = json.loads(res_text)

    content = set()

    for stock in stocks["data"]:
        content.add(stock["name"])

    # for r in content:
    #     print(r)
    return "<h3>"+date+"龙虎榜数据：</h3>"+str(content)
