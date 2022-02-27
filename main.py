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

#Channel ID
#1656927401

#Channel secret
#ce1d6367670fe42d41cf8225c165da3a

#チャンネルアクセストークン(長期)
#xISvQ2oOl07TRZFqHm+uSUM15JfFd2jgI3D9+d+nXTq3jwaax4lZWEw3Gd9HENN/jPZk1A0+xxpYoWJE3dhd7TkAbNf80720zzHPun9SP/KAuNTKazC1weCXP4ztQXxpIxdFQ4as/2sHAyO1puGYfAdB04t89/1O/w1cDnyilFU=


LINE_CHANNEL_ACCESS_TOKEN='xISvQ2oOl07TRZFqHm+uSUM15JfFd2jgI3D9+d+nXTq3jwaax4lZWEw3Gd9HENN/jPZk1A0+xxpYoWJE3dhd7TkAbNf80720zzHPun9SP/KAuNTKazC1weCXP4ztQXxpIxdFQ4as/2sHAyO1puGYfAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET='ce1d6367670fe42d41cf8225c165da3a'

line_bot_api = LineBotApi('xISvQ2oOl07TRZFqHm+uSUM15JfFd2jgI3D9+d+nXTq3jwaax4lZWEw3Gd9HENN/jPZk1A0+xxpYoWJE3dhd7TkAbNf80720zzHPun9SP/KAuNTKazC1weCXP4ztQXxpIxdFQ4as/2sHAyO1puGYfAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ce1d6367670fe42d41cf8225c165da3a')
app = Flask(__name__)

@app.route("/")#Flask動作確認のコード
def say_hello():
    return "Hello"


## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
        #署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
        # handleの処理を終えればOK
    return 'OK'
 
## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #if event.reply_token == "00000000000000000000000000000000":
    #    return
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。
 
# ポート番号の設定
if __name__ == "__main__":
    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=True)
