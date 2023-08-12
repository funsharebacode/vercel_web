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
    # 引入 pywencai 库
    res = pywencai.get(query='当前涨幅',find=['600519', '000010'])
    # 获取列名 -> 涨跌幅:前复权[20230811]
    rate = res.columns[3]
    # 获取前几行数据
    stock_detail = res[['股票简称',rate]][:3]
    # 创建字符串 stock_str = {'stocks':['贵州茅台','-2.18%'],['美丽生态','-2.98%'],['科净源','113.33']}
    stock_str = "{'stocks':["
    for index,row in stock_detail.iterrows():
        stock_str += '{'
        stock_str += '"{}":"{}","{}":"{}%"'.format("name",stock_detail.iloc[index]['股票简称'],"rate",stock_detail.iloc[index][rate][:-6])
        stock_str += '},'
    stock_str += "]}"
    stocks = stock_str.replace(",]}","]}")
    # 生成json api
    stock_api = json.dumps(stocks,ensure_ascii=False)
    
    return stocks

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
