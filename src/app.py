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
    user_msg = event.message.text
    
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

    if 'image_carousel' in user_msg.lower():
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='datetime',
                                                            data='datetime_postback',
                                                            mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerAction(label='date',
                                                            data='date_postback',
                                                            mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    # Di bawah ini bagian logika percakapan pengguna
    # Sementara masih echo pesan pengguna, silakan ditambah, dan dihapus saja komentar ini jika sudah
    if user_msg == 'cat image':
        #url = 'https://bryanahusna-first-line-bot.herokuapp.com/statics/cat-cartoon.jpg' #url = request.url_root + 'statics/cat-cartoon.jpg'
        url = 'https://cdn.pixabay.com/photo/2021/06/27/14/32/raspberry-6368999_960_720.png'
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=url))
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(url, url))
    if user_msg == 'elephant image': 
        #url = 'https://bryanahusna-first-line-bot.herokuapp.com/statics/cat-cartoon.jpg' #url = request.url_root + 'statics/cat-cartoon.jpg'
        url = 'https://cdn.pixabay.com/photo/2018/11/22/18/17/elephant-3832516_1280.jpg'
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=url))
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(url, url))

    if 'hai' in user_msg.lower() or 'halo' in user_msg.lower() or 'hello' in user_msg.lower():
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Halo, '+ user_profile.display_name+ '! Di sini Kirana. Apa yang bisa aku bantu untukmu'))
    if 'stress' in user_msg.lower() or 'stres' in user_msg.lower():
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Gapapa kok, hampir semua orang pasti pernah merasakan hal sepertimu. Coba dimaknai saja keadaan yang sekarang, pastinya terjadi untuk membentuk dirimu menjadi lebih baik. Aku punya artikel menarik nih yang mungkin dapat bermanfaat untuk kondisimu sekarang, yuk dicek! \nhttp://grhasia.jogjaprov.go.id/berita/371/manajemen-stress.html   \nhttps://www.alodokter.com/ternyata-tidak-sulit-mengatasi-stres  \nhttps://hellosehat.com/mental/stres/cara-unik-menghilangkan-stres/'))
    if 'bosan' in user_msg.lower() or 'bosen' in user_msg.lower() or 'jenuh' in user_msg.lower():
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Haiiiii, lagi bosan yaa?? Kamu bisa isi waktu luangmu dengan kegiatan yang bermanfaat nih! Contohnya, belajar skill baru ataupun berolahraga. Kamu juga bisa menghibur dirimu sendiri menggunakan media hiburan. Kalau belum cukup, kamu bisa kontak admin kami, yuk! \nhttps://dosenpsikologi.com/cara-menghilangkan-rasa-bosan'))
    if 'bully' in user_msg.lower() or 'bullying' in user_msg.lower() or 'rundung' in user_msg.lower():
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Heii, kamu orang yang kuat. Hidup ini memang kejam, memaksamu untuk tumbuh lebih cepat karena keadaan. Its okay, aku percaya kamu bisa bangkit lagi dari semua ini. Semoga artikel ini bisa membantu yaa \nhttps://www.sehatq.com/artikel/trauma-psikologis-bisa-lumpuhkan-kehidupan-ini-cara-menyembuhkannya'))
    if 'anxiety' in user_msg.lower() or 'cemas' in user_msg.lower() or 'gelisah' in user_msg.lower(): 
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Terkadang apa yang kamu cemaskan tidak seburuk kenyataannya kok. Baca ini, yuk! \nhttp://www.p2ptm.kemkes.go.id/artikel-sehat/olah-raga-atasi-gangguan-kecemasan'))
    if 'trauma' in user_msg.lower(): 
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Heii, kamu orang yang kuat. Hidup ini memang kejam, memaksamu untuk tumbuh lebih cepat karena keadaan. Its okay, aku percaya kamu bisa bangkit lagi dari semua ini. Semoga artikel ini bisa membantu yaa \nhttps://www.sehatq.com/artikel/trauma-psikologis-bisa-lumpuhkan-kehidupan-ini-cara-menyembuhkannya'))
    if 'takut' in user_msg.lower() : 
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Iya gapapa kok, wajar muncul ketakutan di dalam dirimu. Sekarang tenangin diri kamu dulu ya, mungkin artikel ini bisa membantu \nhttps://www.sehatq.com/artikel/mengenal-alasan-di-balik-rasa-takut-pada-manusia'))
    if 'capek' in user_msg.lower() or 'lelah' in user_msg.lower() : 
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Rehat dulu yuk dari semuanya. Istirahatkan pikiran, mental, dan fisikmu supaya kamu bisa berenergi kembali. Ini ada artikel buat kamu, semoga membantu ya! \nhttps://www.hipwee.com/tag/capek/'))
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    return


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
