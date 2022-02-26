# -*- coding: utf-8 -*-
#Webアプリケーションの仕組みとラインボットの仕組みが同じだからflaskを使う

from flask import Flask, request, abort
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)




#アクセストークン
#iuDwl1NzVNVdqLUn2kNvIsxUAZKOLiVJJVYw9/AOh6CIfGlxrsSKVd0Rdmn0K5P7NgvkIW6dOfj+AfABYkSWdEgYBvGNGLkP4O3bfUW5BIGC365NA8spC/KW8TRH22nLnt3AnGmEPRQmVCgeD2lDoAdB04t89/1O/w1cDnyilFU=
#チャンネルシークレット
#30187ee0e0d1a397b44add525ad55d07

line_bot_api = LineBotApi('0LEHVBVv/h167RB74qpA0svT1Q+pvcCoy5hBACEFg0HBx7lZz+ZtbGZmmUEwDwkQNgvkIW6dOfj+AfABYkSWdEgYBvGNGLkP4O3bfUW5BIH7o5QZXk4p8uraZvQCVOLsSkxyfUCgBXUdITPm8ROr/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('30187ee0e0d1a397b44add525ad55d07')
app = Flask(__name__)

@app.route("/")#Flask動作確認のコード
def say_hello():
    return "Hello"


##########ここから↓LINEBOTの存在を知らしめる処理####################
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
##########ここまで↑LINEBOTの存在を知らしめる処理####################


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()


