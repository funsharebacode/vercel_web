from flask import Flask
import requests
import json
from datetime import datetime
import pytz
import pywencai

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/user')
def user():
    # 股票代码
    codes = "sz000001,sz002467,sz002642,sz000014"
    # 设置请求头
    headers = {'referer': 'http://finance.sina.com.cn'}
    # 获取股票接口
    resp = requests.get('http://hq.sinajs.cn/list=' + codes, headers=headers, timeout=6).text
    # print(resp)
    # 创建 api数据接口
    data = resp.split(";")
    # 拼接接口字符
    stock_str = "{'stocks':["
    for stock in data[:-1]:
        stocks = stock.split("=")[1].split(",")
        rate = (float(stocks[3]) - float(stocks[2])) / float(stocks[2]) * 100
        stock_str += '{'
        stock_str += '"{}":"{}","{}":"{}%"'.format("name", stocks[0][1:], "rate",str(rate)[:5])
        stock_str += '},'
    stock_str += "]}"
    stock_str = stock_str.replace(",]}","]}")
    # print(stock_str)
    # 转换为json数据
    stock_json = json.dumps(stock_str,ensure_ascii=False,indent=4)
    return stock_json
    

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
        return "<h3>"+str(date.date())+"龙虎榜数据：</h3>"+str(content)
    except Exception as e:
        return '暂无相关数据...'
