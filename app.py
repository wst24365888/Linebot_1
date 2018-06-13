from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import random as rd

import newton_separate

import urllib.request as url

import json

import urllib.parse

import requests

from bs4 import BeautifulSoup

app = Flask(__name__)

line_bot_api = LineBotApi('ew9Gu+/a0OB/IT90r8mEiLaipylgz85Kw9maa8624PWPZsvnggQrt1iEbkMaPXFyJD+u6P3zmvMYiY3k3fu0+/c6lGZTcpG0AdeUs+ChuJ00knWPevFv2Jxnjnv6b+J9BmZkBGO5Zsms74pn42KasAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c90f608354cca2df82c4e2b6167097c9')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if ' ' in event.message.text:
        cmd, messages = event.message.text.split()
    else:
        cmd = event.message.text

    reply = '目前有以下功能哦~\n\n1. 抽數字\n輸入\'抽 min,max\'\nex.\ninput: 抽 1,100\noutput: 87\n\n2. 多項式拆出一次式\n輸入\'拆 terms1,terms2,...\'\nex.\ninput: 拆 1,2,1\noutput: (x+1)\n\n3. 找圖片\nex.\ninput: 找 貓咪\noutput: 一些flickr連結'    

    if '早' in cmd or '嘿' in cmd or '安' in cmd or '嗨' in cmd or  '你好' in cmd or'hello' in cmd or 'hi' in cmd or 'hey' in cmd:
        hello_seed = rd.randint(1,4)
        if hello_seed == 1:
            reply = '安安'
        elif hello_seed == 2:
            reply = '嗨'
        elif hello_seed == 3:
            reply = 'hi'
        elif hello_seed == 4:
            reply = 'hello'

    elif '抽' in cmd:

        min_num, max_num = messages.split(',')
        min_num = int(min_num)
        max_num = int(max_num)
        reply = '{}'.format(rd.randint(min_num,max_num))

    elif '拆' in cmd:

        reply = newton_separate.run_main(messages)

    elif '找' in cmd:

        data = url.urlopen(url.Request('https://api.flickr.com/services/feeds/photos_public.gne?format=json&tags={}'.format(urllib.parse.quote_plus('{}'.format(messages))))).read().decode('utf-8')

        data_str = ''

        for i in range(15,len(data)-1):
            data_str += data[i]

        the_html = requests.get(json.loads(data_str)['items'][0]['link'])
        
        html_str = BeautifulSoup(the_html.text, 'html.parser')
    
        img_url = html_str.find(property="og:image")['content']

        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url))
        
        
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = "{}".format(reply)))


if __name__ == "__main__":
    app.run()