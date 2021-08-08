from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from checker import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('KBYcJt1ZmbmMnkQM0ZW6uREsAtE7QSARwDrVprACm91i3/zpvlJZVHXVVFnVDuRorEceLSqwx8qV/fIDE/qpJF1wdNMykK0kgHIxEeeNywBXIKvcWp+q9Rxw1a3C661yzKWgR/8AYzMt3eLgHAj3MwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('38cb174b5ffbf238b2b7048c47676654')

# 監聽所有來自 /callback Post Request
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

def sendToAdmin(message,user_id, admin_name):
    # Message adalah pesan yang akan dikirim ke admin
    # user_id adalah userID dari line
    # admin_name adalah nama admin, ada di dict admins
    admins = {
        'Alif Yasa' : 'Ua68faad875d238f2b77e6f4b1df027ab'
    }
    user_profile = line_bot_api.get_profile(user_id=user_id)
    # Menurutku message ke Admin dengan message ke user harus berbeda
    # karena sepertinya lebih baik jika admin tahu detailnya
    pesan = f"{user_profile.display_name}: {message}\n\nuserID: `{user_id}`"
    line_bot_api.push_message(admins[admin_name], TextSendMessage(text=pesan)) # Tes kirim ke Alif

def sendToUser(message, admin_id, recipient_id):
     # message adalah pesan, bagian akhir message harus ada userID
     # admin id adalah id dari admin, nantinya akan di check     
    admins = {
        'Alif Yasa' : 'Ua68faad875d238f2b77e6f4b1df027ab'
    }
    user_profile = line_bot_api.get_profile(user_id=admin_id)
    if admins[user_profile.display_name] == admin_id:
        try: 
            line_bot_api.push_message(recipient_id, TextSendMessage(text=message.strip()))
        except:
            abort(400)
    

# Take user's sent text
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_raw = event.message.text
    message = message_raw.lower()
    sendToAdmin(message_raw[-33:], user_id, 'Alif Yasa')
    list_sapaan = ["halo", "halo", "hi", "hai"]
    list_katakunci = ["stres", "lonely", "sepi", "depresi", "bundir", "bunuh"]
    list_response = ["iya", "tidak"]
    if checker(message, list_sapaan):
        reply_msg = "Hai aku Kirana, disini aku akan menemani kamu. Boleh kalo mau curhat yah"
        sent_msg = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(event.reply_token, sent_msg)
    elif checker(message, list_katakunci):
        if "stress" in message:
            reply_msg = "Wahh, kamu lagi banyak kerjaan yah? Atau mungkin lagi banyak pikiran? Semangat terus yaaa. Aku punya artikel yang membantu kamu"
            sent_msg = TextSendMessage(text=reply_msg)
        reply_response = "Apakah jawabanku membantu kamu? Ketik 'iya' jika membantu"
        sent_response = TextSendMessage(text=reply_response)
        line_bot_api.reply_message(event.reply_token, [sent_response, sent_msg])
    elif checker(message, list_response):
        if "iya" in message:
            reply_msg = "Terima kasih, semoga hidup kamu membaik ya"
            sent_msg = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(event.reply_token, sent_msg)
        else:
            reply_msg = "Maaf ya kalau aku kurang membantu. Ini aku kasih kontak admin yang bisa membantu kamu"
            sent_msg = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(event.reply_token, sent_msg)
    else:
        reply_msg = "Maaf, aku kurang paham nih sama apa yang kamu katakan. Mungkin bisa diperjelas"
        sent_msg = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(event.reply_token, sent_msg)
    if message_raw[:3] == "###":
        sendToUser(message_raw[3:], user_id, message_raw[-33:])


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
