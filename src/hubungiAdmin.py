from flask import abort

from linebot import LineBotApi
from linebot.models import *

def sendToAdmin(message,user_id, admin_name):
    # Message adalah pesan yang akan dikirim ke admin
    # user_id adalah userID dari line
    # admin_name adalah nama admin, ada di dict admins
    global admins
    user_profile = line_bot_api.get_profile(user_id=user_id)
    # Menurutku message ke Admin dengan message ke user harus berbeda
    # karena sepertinya lebih baik jika admin tahu detailnya
    pesan = f"[{user_profile.display_name}]\n\n{message}\n\n[{user_id}]"
    line_bot_api.push_message(admins[admin_name], TextSendMessage(text=pesan)) # Tes kirim ke Alif

def sendToUser(message, admin_id, recipient_id):
     # message adalah pesan, bagian akhir message harus ada userID
     # admin id adalah id dari admin, nantinya akan di check     
    global admins
    user_profile = line_bot_api.get_profile(user_id=admin_id)
    if admins[user_profile.display_name] == admin_id:
        try: 
            line_bot_api.push_message(recipient_id, TextSendMessage(text=message.strip()))
            line_bot_api.push_message(admin_id, TextSendMessage(text='Pesan Terkirim!'))
        except:
            abort(400)

line_bot_api = LineBotApi('KBYcJt1ZmbmMnkQM0ZW6uREsAtE7QSARwDrVprACm91i3/zpvlJZVHXVVFnVDuRorEceLSqwx8qV/fIDE/qpJF1wdNMykK0kgHIxEeeNywBXIKvcWp+q9Rxw1a3C661yzKWgR/8AYzMt3eLgHAj3MwdB04t89/1O/w1cDnyilFU=')

admins = {
    'Alif Yasa' : 'Ua68faad875d238f2b77e6f4b1df027ab',
    'Adityapn'  : 'U1836a7b2a86cdb1036590eb08cf7b931'
}