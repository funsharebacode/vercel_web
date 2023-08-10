from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/user')
def user():
    return 'user...'

@app.route('/data')
def get_web_data():
    res = requests.get("https://baidu.com")
    res_text = res.text
    return res_text

