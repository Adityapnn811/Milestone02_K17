from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('KBYcJt1ZmbmMnkQM0ZW6uREsAtE7QSARwDrVprACm91i3/zpvlJZVHXVVFnVDuRorEceLSqwx8qV/fIDE/qpJF1wdNMykK0kgHIxEeeNywBXIKvcWp+q9Rxw1a3C661yzKWgR/8AYzMt3eLgHAj3MwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('38cb174b5ffbf238b2b7048c47676654')

# callback 的 Post Request
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
    msg = event.message.text
    if msg == 'cat image':
        #url = 'https://bryanahusna-first-line-bot.herokuapp.com/statics/cat-cartoon.jpg' #url = request.url_root + 'statics/cat-cartoon.jpg'
        url = 'https://cdn.pixabay.com/photo/2021/06/27/14/32/raspberry-6368999_960_720.png'
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=url))
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(url, url))
    elif msg == 'kirim beberapa':
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='Keren'), TextSendMessage(text='sekali')])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Mantap'))
    elif msg == 'hai' :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Hallo'))
    elif msg == 'hallo' :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Hai'))
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
