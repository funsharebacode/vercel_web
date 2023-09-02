# -*- coding: utf-8 -*-
from flask import Flask,render_template,request
import requests
import json
import re
from datetime import datetime
import pytz
import pywencai

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'

@app.route("/kcb")
def kcb():
    return render_template('kcb.html')

@app.route('/stock')
def html():
    return render_template('index.html')

@app.route('/user',methods=['GET','POST'])
def user():
    # 股票代码
    # stock_code = request.form.get('stock_code').split(",")
    # stocks = ''
    # for code in stock_code:
    #     if re.match(r'^(0|3)', code):
    #         stocks += 'sz' + code + ','
    #     elif re.match(r'^(6)', code):
    #         stocks += 'sh' + code + ','

    # stocks = stocks[:-1]
    # 设置请求头
    headers = {'referer': 'http://finance.sina.com.cn'}
    # 获取股票接口
    str = ''
    user_stocks = ['sz300315', 'sz002642']
    for s in user_stocks:
        str += s + ','
    resp = requests.get('http://hq.sinajs.cn/list=' + str[:-1], headers=headers, timeout=6).text
    # print(resp)
    # 创建 api数据接口
    
    # print(resp)
    
    data = resp.split(";")
    # 拼接接口字符
    info_api = {"stocks": []}
    for index,stock in enumerate(data[:-1]):
        stocks = stock.split("=")[1].split(",")
        rate = (float(stocks[3]) - float(stocks[2])) / float(stocks[2]) * 100
        info_api["stocks"].append({"code":user_stocks[index],"name":stocks[0][1:],"rate":('%.2f'%rate) + '%'})


    # 获取彩云天气接口
    caiyun = json.loads(requests.get(
        "https://api.caiyunapp.com/v2.6/TAkhjf8d1nlSlspN/121.442701,31.171717/weather?alert=true&dailysteps=1&hourlysteps=24").text)
    area = requests.get('https://api.caiyunapp.com/v2.6/TAkhjf8d1nlSlspN/121.442701,31.171717/realtime?alert=true').text
    # 天气预报地区
    city = caiyun["result"]["alert"]["adcodes"][0]["name"] + "|" + caiyun["result"]["alert"]["adcodes"][2]["name"]
    # 天气现象
    sky_con = {"CLEAR_DAY": "晴（白天）", "CLEAR_NIGHT": "晴（夜间）", "PARTLY_CLOUDY_DAY": "多云（白天）",
               "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
               "CLOUDY": "阴", "LIGHT_HAZE": "轻度雾霾", "MODERATE_HAZE": "中度雾霾", "HEAVY_HAZE": "重度雾霾",
               "LIGHT_RAIN": "小雨",
               "MODERATE_RAIN": "中雨", "HEAVY_RAIN": "大雨", "STORM_RAIN": "暴雨", "FOG": "雾", "LIGHT_SNOW": "小雪",
               "MODERATE_SNOW": "中雪",
               "HEAVY_SNOW": "大雪", "STORM_SNOW": "暴雪", "DUST": "浮尘", "SAND": "沙尘", "WIND": "大风"}
    # 气温（地表2米气温）
    temperature = int(caiyun["result"]["realtime"]["temperature"])
    # 天气现象
    skycon = sky_con[caiyun["result"]["realtime"]["skycon"]]
    # 气压
    pressure = '{}'.format(int(caiyun["result"]["realtime"]["pressure"]) / 100)
    # wind
    # 风速
    wind_speed = '{}'.format(caiyun["result"]["realtime"]["wind"]["speed"]) + '米'
    # 风向
    wind_direction = int(caiyun["result"]["daily"]["wind_08h_20h"][0]["avg"]["direction"])
    if wind_direction * 100 in range(1126, 3375):
        wind_direct = '北-东北风'
    elif wind_direction * 100 in range(3376, 5625):
        wind_direct = '东北风'
    elif wind_direction * 100 in range(5626 - 7875):
        wind_direct = '东-东北风'
    elif wind_direction * 100 in range(7876, 10125):
        wind_direct = '东风'
    elif wind_direction * 100 in range(10126, 12375):
        wind_direct = '东-东南风'
    elif wind_direction * 100 in range(12376, 14625):
        wind_direct = '东南风'
    elif wind_direction * 100 in range(14626, 16875):
        wind_direct = '南-东南风'
    elif wind_direction * 100 in range(16876, 19125):
        wind_direct = '南风'
    elif wind_direction * 100 in range(19126, 21375):
        wind_direct = '南-西南风'
    elif wind_direction * 100 in range(21376, 23625):
        wind_direct = '西南风'
    elif wind_direction * 100 in range(23626, 25875):
        wind_direct = '西-西南风'
    elif wind_direction * 100 in range(25876, 28125):
        wind_direct = '西风'
    elif wind_direction * 100 in range(28126, 30375):
        wind_direct = '西-西北风'
    elif wind_direction * 100 in range(30376, 32625):
        wind_direct = '西北风'
    elif wind_direction * 100 in range(32626, 34875):
        wind_direct = '北-西北风'
    else:
        wind_direct = '北风'

    # 天气质量
    description_a = caiyun["result"]["realtime"]["air_quality"]["description"]["chn"]
    description_b = caiyun["result"]["realtime"]["air_quality"]["description"]["usa"]
    # 最高气温
    max_temp = int(caiyun["result"]["daily"]["temperature"][0]["max"])
    # 最低气温
    min_temp = int(caiyun["result"]["daily"]["temperature"][0]["min"])
    # 未来两小时降水情况
    forecast_keypoint = caiyun["result"]["forecast_keypoint"]

    info_api["temperature"] = {"temperature":temperature,"skycon":skycon,"pressure":str(pressure),"wind_speed":wind_speed,"wind_direct":wind_direct,
                "description_a":description_a,"description_b":description_b,"max_temp":max_temp,"min_temp":min_temp,"forecast_keypoint":forecast_keypoint,
                "city":city}

    return json.dumps(info_api,ensure_ascii=False)
    

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
