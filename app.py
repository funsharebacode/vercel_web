Skip to content
funsharebacode
/
vercel_web

Type / to search

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Pane width
Use a value between 18% and 33%

22
Change width
Code
Go to file
t
README.md
app.py
requirements.txt
vercel.json
Documentation • Share feedback
Breadcrumbsvercel_web
/
app.py
in
main

Edit

Preview
Indent mode

Spaces
Indent size

4
Line wrap mode

No wrap
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
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
    return 'user...'

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




Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.
Editing vercel_web/app.py at main · funsharebacode/vercel_web
