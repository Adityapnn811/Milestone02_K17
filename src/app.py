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
from checker import *
import random

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

# Buat fungsi random
def Random_Motivasi():
    random.seed(datetime.now())
    mot = ["Bisaa gais", "kamu di hati", "i love Bryan", "We love you"]
    return mot[random.randint(0,len(mot)-1)]

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
    user_msg = event.message.text.lower()
    nama = user_profile.display_name

    # Fitur mode admin
    psql_cur.execute("SELECT * FROM dilayani_admin WHERE id_user=%s;", (user_id,))
    hasil_dilayani = psql_cur.fetchone()
    if hasil_dilayani:
        if "mode bot" in user_msg.lower():
            id_admin_free = hasil_dilayani[1]
            psql_cur.execute("DELETE FROM dilayani_admin WHERE id_user=%s;", (user_id,))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Bot..."), TextSendMessage(text="Sekarang kamu berbicara dengan Bot")])
            line_bot_api.push_message(id_admin_free, TextSendMessage(text=user_profile.display_name + " BERHENTI MENGHUBUNGI ADMIN"))
            psql_cur.execute("SELECT * FROM antrean_admin;")
            first_antrean = psql_cur.fetchone()
            if first_antrean:
                id_user_firstantre = first_antrean[0]
                psql_cur.execute("INSERT INTO dilayani_admin VALUES ('{}', '{}', {});".format(id_user_firstantre, id_admin_free, datetime.now().timestamp()))
                psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s", (id_user_firstantre,))
                line_bot_api.push_message(id_user_firstantre, [TextSendMessage(text="Berpindah ke Mode Admin..."), TextSendMessage(text="Sekarang kamu menghubungi Admin, jika sudah selesai ketik \"mode bot\"")])
                line_bot_api.push_message(id_admin_free, TextSendMessage(text=line_bot_api.get_profile(user_id=id_user_firstantre).display_name + " MENGHUBUNGI ADMIN"))
            else:
                pass
            psql_conn.commit()
            return
        id_admin_melayani = hasil_dilayani[1]
        line_bot_api.push_message(id_admin_melayani, TextSendMessage(text=user_msg))
        return

    psql_cur.execute("SELECT * FROM antrean_admin WHERE id_user=%s;", (user_id,))
    hasil_antrean = psql_cur.fetchone()
    if hasil_antrean:
        psql_cur.execute("SELECT * FROM dilayani_admin;")
        sedang_dilayani = psql_cur.fetchall()
        if "batal admin" in user_msg.lower():
            psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s;", (user_id,))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Membatalkan menghubungi Admin..."), TextSendMessage(text="Sekarang kamu berbicara dengan Bot")])
        elif sedang_dilayani and len(sedang_dilayani) < ms.admin_count:
            id_admins_sibuk = []
            for pelayanan in sedang_dilayani:
                id_admins_sibuk.append(pelayanan[1])
            id_admins_free = list(set(ms.id_admins) - set(id_admins_sibuk))
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, id_admins_free[0], datetime.now().timestamp()))
            psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s;", (user_id,))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Selamat, sekarang kamu menghubungi Admin, jika sudah selesai ketik \"mode bot\""))
        elif not sedang_dilayani and ms.admin_count > 0:
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, ms.id_admins[0], datetime.now().timestamp()))
            psql_cur.execute("DELETE FROM antrean_admin WHERE id_user=%s;", (user_id,))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Selamat, sekarang kamu menghubungi Admin, jika sudah selesai ketik \"mode bot\""))
        else:
            # Mohon bersabar Anda urutan xx, atau "batal admin"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Mohon bersabar, Admin sedang menghubungi pengguna lain. Untuk tidak jadi/batal, ketik \"batal admin\""))
        psql_conn.commit()
        return

    if user_id in ms.id_admins:
        psql_cur.execute("SELECT * FROM dilayani_admin WHERE id_admin=%s", (user_id,))
        admin_melayani = psql_cur.fetchone()
        if admin_melayani:
            if "stoppen pengguna" in user_msg.lower():
                psql_cur.execute("DELETE FROM dilayani_admin WHERE id_admin=%s", (user_id,))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Anda MENGHENTIKAN CHAT " + line_bot_api.get_profile(user_id=admin_melayani[0]).display_name))
                line_bot_api.push_message(admin_melayani[0], [TextSendMessage(text="Admin menghentikan percakapan kamu..."), TextSendMessage(text="Sekarang kamu berbicara dengan Bot")])
                psql_conn.commit()
            else:
                line_bot_api.push_message(admin_melayani[0], TextSendMessage(text=user_msg))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Anda sedang tidak melayani pengguna"))
        return

    if "mode admin" in user_msg.lower():
        psql_cur.execute("SELECT * FROM dilayani_admin;")
        sedang_dilayani = psql_cur.fetchall()
        if sedang_dilayani and len(sedang_dilayani) < ms.admin_count:
            id_admins_sibuk = []
            for pelayanan in sedang_dilayani:
                id_admins_sibuk.append(pelayanan[1])
            id_admins_free = list(set(ms.id_admins) - set(id_admins_sibuk))

            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, id_admins_free[0], datetime.now().timestapm()))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Admin..."), TextSendMessage(text="Sekarang kamu berbicara dengan Admin, ketik \"mode bot\" jika sudah selesai")])
            line_bot_api.push_message(id_admins_free[0], TextSendMessage(text=user_profile.display_name + " MENGHUBUNGI ADMIN"))
        elif  not sedang_dilayani and  ms.admin_count > 0:
            psql_cur.execute("INSERT INTO dilayani_admin VALUES (%s, %s, %s);", (user_id, ms.id_admins[0], datetime.now().timestamp()))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Berpindah ke Mode Admin..."), TextSendMessage(text="Sekarang kamu berbicara dengan Admin, ketik \"mode bot\" jika sudah selesai")])
            line_bot_api.push_message(ms.id_admins[0], TextSendMessage(text=user_profile.display_name + " MENGHUBUNGI ADMIN"))
        else:
            psql_cur.execute("INSERT INTO antrean_admin VALUES (%s);", (user_id,))
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="Mohon bersabar, Admin sedang menghubungi pengguna lain"), TextSendMessage(text="Kamu dimasukkan ke antrean Admin. Untuk tidak jadi/batal, ketik \"batal admin\"")])
        psql_conn.commit()
        return

# Fitur carousel info dari bot dan motivasiin pengguna, nanti bisa ditambahin carousel mode bot sama admin
    if 'info' in user_msg.lower():
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='Yuk ketahui dirimu!', title='Artikel Kesehatan Mental', actions=[
                URIAction(label='Baca di sini!', uri='https://www.halodoc.com/kesehatan/kesehatan-mental')
            ]),
            CarouselColumn(text='Motivasi-in kamu', title='Semangat!', actions=[
                MessageAction(label='Motivate me!', text=Random_Motivasi())
            ]),
            CarouselColumn(text='Ngobrol sama admin yu', title='Admin', actions=[
                MessageAction(label='Kontak Admin', text="mode admin")
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Fitur Bot', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

# Di bawah ini bagian logika percakapan pengguna
    list_sapaan = ["halo", "hallo", "hi", "hai", "hello"]
    list_katakunci = ["stres","stress","bosen","bosan","bully","bullying","rundung","takut","capek","lelah","anxiety","cemas","gelisah", "lonely", "sepi", "depresi", "bundir", "bunuh"]
    list_response = ["iya", "tidak","y","g","ya","ga","tak","enggak"]
    if checker(user_msg, list_sapaan):
        reply_msg = f"Halo, {nama}! Aku Kirana! Apakah ada yang bisa Kirana bantu untuk kamu? Jika ingin tahu apa yang bisa Kirana lakukan, ketik 'Bot Help'."
        sent_msg = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(event.reply_token, sent_msg)
    elif checker(user_msg, list_katakunci):
        if 'stress' in user_msg.lower() or 'stres' in user_msg.lower():
            reply_msg = "Wahh, kamu lagi banyak kerjaan yah? Atau mungkin lagi banyak pikiran? Semangat terus yaaa. Aku punya artikel yang membantu kamu \nhttp://grhasia.jogjaprov.go.id/berita/371/manajemen-stress.html \nhttps://www.alodokter.com/ternyata-tidak-sulit-mengatasi-stres  \nhttps://hellosehat.com/mental/stres/cara-unik-menghilangkan-stres/"
            sent_msg = TextSendMessage(text=reply_msg)
        if 'bosan' in user_msg.lower() or 'bosen' in user_msg.lower() or 'jenuh' in user_msg.lower():
            reply_msg = "Haiiiii, lagi bosan yaa?? Kamu bisa isi waktu luangmu dengan kegiatan yang bermanfaat nih! Contohnya, belajar skill baru ataupun berolahraga. Kamu juga bisa menghibur dirimu sendiri menggunakan media hiburan. Kalau belum cukup, kamu bisa kontak admin kami, yuk! \nhttps://dosenpsikologi.com/cara-menghilangkan-rasa-bosan"
            sent_msg = TextSendMessage(text=reply_msg)
        if 'bully' in user_msg.lower() or 'bullying' in user_msg.lower() or 'rundung' in user_msg.lower():
            reply_msg = "Heii, kamu orang yang kuat. Hidup ini memang kejam, memaksamu untuk tumbuh lebih cepat karena keadaan. Its okay, aku percaya kamu bisa bangkit lagi dari semua ini. Semoga artikel ini bisa membantu yaa \nhttps://www.sehatq.com/artikel/trauma-psikologis-bisa-lumpuhkan-kehidupan-ini-cara-menyembuhkannya"
            sent_msg = TextSendMessage(text=reply_msg)
        if 'anxiety' in user_msg.lower() or 'cemas' in user_msg.lower() or 'gelisah' in user_msg.lower():
            reply_msg ="Terkadang apa yang kamu cemaskan tidak seburuk kenyataannya kok. Baca ini, yuk! \nhttp://www.p2ptm.kemkes.go.id/artikel-sehat/olah-raga-atasi-gangguan-kecemasan"
            sent_msg = TextSendMessage(text=reply_msg)
        if 'takut' in user_msg.lower() :
            reply_msg ="Iya gapapa kok, wajar muncul ketakutan di dalam dirimu. Sekarang tenangin diri kamu dulu ya, mungkin artikel ini bisa membantu \nhttps://www.sehatq.com/artikel/mengenal-alasan-di-balik-rasa-takut-pada-manusia"
            sent_msg = TextSendMessage(text=reply_msg)
        if 'capek' in user_msg.lower() or 'lelah' in user_msg.lower() :
            reply_msg ="Rehat dulu yuk dari semuanya. Istirahatkan pikiran, mental, dan fisikmu supaya kamu bisa berenergi kembali. Ini ada artikel buat kamu, semoga membantu ya! \nhttps://www.hipwee.com/tag/capek/"
            sent_msg = TextSendMessage(text=reply_msg)
        reply_response = "Apakah jawabanku membantu kamu? Ketik 'iya' jika membantu"
        sent_response = TextSendMessage(text=reply_response)
        line_bot_api.reply_message(event.reply_token, [sent_msg, sent_response])
    elif checker(user_msg, list_response):
        if "iya" in user_msg or "ya" in user_msg or "y" in user_msg:
            reply_msg = "Terima kasih, semoga hidup kamu membaik ya :D"
            sent_msg = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(event.reply_token, sent_msg)
        else:
            reply_msg = "Maaf ya kalau aku kurang membantu. Ini aku kasih kontak admin yang bisa membantu kamu"
            sent_msg = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(event.reply_token, sent_msg)
    elif user_msg == "bot help":
        reply_msg = """
 ▁ ▂ ▄ ▅ ▆ ▇ █ Fitur-Fitur Kirana █ ▇ ▆ ▅ ▄ ▂ ▁

Pengguna dapat berbicara langsung ke bot mengenai masalah-masalah yang ada, Bot akan menjawab dengan solusi-solusi singkat yang dianggap berguna bagi Pengguna.

 ░▒▓█ Curhat ke Admin █▓▒░

Selain berbicara dengan Bot, Pengguna juga memiliki pilihan untuk dapat langsung curhat ke Admin dengan mengetik "Mode Admin".

 ░▒▓█ Info Bot █▓▒░

Pengguna dapat mengetahui Info kesehatan mental terkini dan kata-kata motivasi dengan mengetik "Info".
        """
        sent_msg = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(event.reply_token, sent_msg)
    else:
        reply_msg = "Maaf, aku kurang paham nih sama apa yang kamu katakan. Mungkin bisa diperjelas. Kalau kamu ingin tahu info, boleh ketik 'Bot Help'. "
        sent_msg = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(event.reply_token, sent_msg)
    return


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
