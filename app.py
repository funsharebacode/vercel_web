from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/user')
def user():
    return 'user...'

@app.route('/data')
def get_web_data():
    res = requests.get("https://stockapi.com.cn/v1/base/dragonTiger?date=2023-07-21")
    res_text = res.text
    stocks = json.loads(res_text)

    content = set()


    for stock in stocks["data"]:
        content.add(stock["name"])

    # for r in content:
    #     print(r)
    return str(content)



