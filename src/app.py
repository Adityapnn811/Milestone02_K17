import mode_switch as ms

import psycopg2     # PostgreSQL
import pytz         # Untuk waktu dan tanggal
from flask import Flask, request, abort


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from datetime import datetime

app = Flask(__name__)

id_admin = "U2cc53b28669cf7c907d47e8653c08c6a"

# Heroku PostgreSQL Setups
psql_riwayatcakap = 'riwayatcakap'
psql_host = 'ec2-54-196-65-186.compute-1.amazonaws.com'
psql_database = 'd12jneq73g7u2'
psql_user = 'aaqgmutpyfxgmx'
psql_port = 5432
psql_password = '614e04f0ec7d6a687c0b4e8c6a9941391d70349037ac3b1384149752bd7eeacd'
psql_uri = 'postgres://aaqgmutpyfxgmx:614e04f0ec7d6a687c0b4e8c6a9941391d70349037ac3b1384149752bd7eeacd@ec2-54-196-65-186.compute-1.amazonaws.com:5432/d12jneq73g7u2'
psql_herokucli = 'heroku pg:psql postgresql-trapezoidal-98002 --app kirana-bot'

if __name__ == '__main__':
    psql_conn = psycopg2.connect(host=psql_host,
                                 database=psql_database, 
                                 user=psql_user,
                                 password=psql_password,
                                 port=psql_port)
    psql_cur = psql_conn.cursor()

# Channel Access Token (atas) dan Channel Secret (bawah)
line_bot_api = LineBotApi('KBYcJt1ZmbmMnkQM0ZW6uREsAtE7QSARwDrVprACm91i3/zpvlJZVHXVVFnVDuRorEceLSqwx8qV/fIDE/qpJF1wdNMykK0kgHIxEeeNywBXIKvcWp+q9Rxw1a3C661yzKWgR/8AYzMt3eLgHAj3MwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38cb174b5ffbf238b2b7048c47676654')

# Callback untuk aplikasi Admin
@app.route("/admin-chat", methods=['POST', 'GET'])
def callback_admin():
    try:
        json_data = request.json
        id_user = json_data["id_user"]
        pesan_admin = json_data["pesan_admin"]
        sent_msg = TextSendMessage(text=pesan_admin)
        line_bot_api.push_message(id_user, sent_msg)
        return 'OK'
    except:
        return 'NOT OK'

# callback Post Request
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

# Menghandle pesan teks yang masuk
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_profile = line_bot_api.get_profile(user_id=user_id)
    user_msg = event.message.text

    psql_cur.execute("SELECT * FROM dilayani_admin WHERE id_user=%s;", (user_id))
    hasil_dilayani = psql_cur.fetchone()
    if hasil_dilayani:
        if "mode bot" in user_msg.lower():
            id_admin_free = hasil_dilayani[1]
            psql_cur.execute("DELETE FROM dilayani_admin WHERE id_user=%s;", (user_id))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Bot"), TextSendMessage(text="Sekarang kamu berbicara dengan Bot")])
            line_bot_api.push_message(id_admin_free, TextSendMessage(text=user_profile.display_name + " BERHENTI MENGHUBUNGI ADMIN"))
            psql_cur.execute("SELECT * FROM antrean_admin;")
            first_antrean = psql_cur.fetchone()
            if first_antrean:
                id_user_firstantre = first_antrean[0]
                psql_cur.execute("INSERT INTO dilayani_admin VALUES ('{}', '{}', {});".format(id_user_firstantre, id_admin_free, datetime.now().timestamp()))
                psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s", (id_user_firstantre))
                line_bot_api.push_message(id_user_firstantre, [TextSendMessage(text="Berpindah ke Mode Admin"), TextSendMessage(text="Sekarang kamu menghubungi Admin, jika sudah selesai ketik \"mode bot\"")])
                line_bot_api.push_message(id_admin_free, TextSendMessage(text=line_bot_api.get_profile(user_id=id_user_firstantre).display_name + " MENGHUBUNGI ADMIN"))
            else:
                pass
            psql_conn.commit()
            return
        id_admin_melayani = hasil_dilayani[1]
        line_bot_api.push_message(id_admin_melayani, TextSendMessage(text=user_msg))
        return
    
    psql_cur.execute("SELECT * FROM antrean_admin WHERE id_user=%s;", (user_id))
    hasil_antrean = psql_cur.fetchone()
    if hasil_antrean:
        psql_cur.execute("SELECT * FROM dilayani_admin;")
        sedang_dilayani = psql_cur.fetchall()
        if user_msg.lower == "batal admin":
            psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s;", (user_id))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Membatalkan menghubungi Admin..."), TextSendMessage(text="Sekarang kamu berbicara dengan Bot")])
        elif sedang_dilayani and len(sedang_dilayani) < ms.admin_count:
            id_admins_sibuk = []
            for pelayanan in sedang_dilayani:
                id_admins_sibuk.append(pelayanan[1])
            id_admins_free = list(set(ms.id_admins) - set(id_admins_sibuk))
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, id_admins_free[0], datetime.now().timestamp()))
            psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s;", (user_id))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Selamat, sekarang kamu menghubungi Admin, jika sudah selesai ketik \"mode bot\""))
        elif not sedang_dilayani and ms.admin_count > 0:
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, ms.id_admins[0], datetime.now().timestamp()))
            psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s;", (user_id))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Selamat, sekarang kamu menghubungi Admin, jika sudah selesai ketik \"mode bot\""))
        else:
            # Mohon bersabar Anda urutan xx, atau "batal admin"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Mohon bersabar, Admin sedang menghubungi pengguna lain. Untuk tidak jadi/batal, ketik \"batal admin\""))
        psql_conn.commit()
        return
    
    if user_id in ms.id_admins:
        psql_cur.execute("SELECT * FROM dilayani_admin WHERE id_admin=%s", (user_id))
        admin_melayani = psql_cur.fetchone()
        if admin_melayani:
            line_bot_api.push_message(admin_melayani[0], TextSendMessage(text=user_msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Anda sedang tidak melayani pengguna"))
        return

    if "mode admin" in user_msg:
        psql_cur.execute("SELECT * FROM dilayani_admin;")
        sedang_dilayani = psql_cur.fetchall()
        if sedang_dilayani and len(sedang_dilayani) < ms.admin_count:
            id_admins_sibuk = []
            for pelayanan in sedang_dilayani:
                id_admins_sibuk.append(pelayanan[1])
            id_admins_free = list(set(ms.id_admins) - set(id_admins_sibuk))
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, id_admins_free[0], datetime.now().timestapm()))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Admin"), TextSendMessage(text="Sekarang kamu berbicara dengan Admin, ketik \"mode bot\" jika sudah selesai")])
        elif  not sedang_dilayani and  ms.admin_count > 0:
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, ms.id_admins[0], datetime.now().timestamp()))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Admin"), TextSendMessage(text="Sekarang kamu berbicara dengan Admin, ketik \"mode bot\" jika sudah selesai")])            
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Mohon bersabar, Admin sedang menghubungi pengguna lain. Untuk tidak jadi/batal, ketik \"batal admin\""))
        psql_conn.commit()
        return
    
    # Di bawah ini bagian logika percakapan pengguna
    # Sementara masih echo pesan pengguna, silakan ditambah, dan dihapus saja komentar ini jika sudah
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_msg))
    return

    psql_cur.execute("SELECT * FROM chatadmin;")
    result = psql_cur.fetchone()

    # Jika admin mengirim pesan, dan ada client yang menghubungi admin
    if result != None and user_id == id_admin:
        id_client = result[0]
        line_bot_api.push_message(id_client, TextSendMessage(text=event.message.text))
    # Jika user mengirim pesan, dan user sedang menghubungi admin
    elif result != None:
        id_client = result[0]
        if "mode bot" in event.message.text.lower():
            psql_cur.execute("DELETE FROM chatadmin WHERE id_user='{}';".format(id_client))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Bot"), TextSendMessage(text="Sekarang Anda berbicara dengan Bot")])
        else:
            line_bot_api.push_message(id_admin, TextSendMessage(text=event.message.text))
    else:
        if "mode admin" in event.message.text.lower():
            psql_cur.execute("INSERT INTO chatadmin VALUES ('{}');".format(user_id))
            line_bot_api.push_message(id_admin, TextSendMessage(text="Nama user {}".format(user_profile.display_name)))
            line_bot_api.reply_message(event.reply_token,
                                        [TextSendMessage(text="Berpindah ke Mode Admin"),
                                        TextSendMessage(text="Sekarang Anda berbicara dengan Admin")])
            return
        try:
            time_now = datetime.now(pytz.timezone('Etc/GMT-7'))
            pesan_sql = "('{}', '{}', {}, '{}-{}-{} {:02}:{:02}', '{}')".format(
                    user_profile.display_name.replace("'", "''"), user_id, int(datetime.now().timestamp()),
                    time_now.day, time_now.month, time_now.year, time_now.hour, time_now.minute,
                    event.message.text.replace("'", "''"))
            psql_cur.execute("INSERT INTO riwayatcakap VALUES " + pesan_sql + ";")
            sent_msg = TextSendMessage(text=pesan_sql)
            line_bot_api.reply_message(event.reply_token, sent_msg)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Maaf, suatu error terjadi"))
    psql_conn.commit()

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)