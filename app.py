from flask import Flask
import requests
import json
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/user')
def user():
    return 'user...'

@app.route('/data')
def get_web_data():
    date = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        url = 'https://stockapi.com.cn/v1/base/dragonTiger?date='+str(date.date())
        res = requests.get(url)
        res_text = res.text
        stocks = json.loads(res_text)
    
        content = set()
    
        for stock in stocks["data"]:
            content.add(stock["name"])

        # for r in content:
        #     print(r)
        return "<h3>"+date+"龙虎榜数据：</h3>"+str(content)

      except Exception as e:
          return '暂无相关数据...'
