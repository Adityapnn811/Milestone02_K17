import psycopg2     # PostgreSQL
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

# Heroku PostgreSQL Setups
psql_riwayatcakap = 'riwayatcakap'
psql_host = 'ec2-54-196-65-186.compute-1.amazonaws.com'
psql_database = 'd12jneq73g7u2'
psql_user = 'aaqgmutpyfxgmx'
psql_port = 5432
psql_password = '614e04f0ec7d6a687c0b4e8c6a9941391d70349037ac3b1384149752bd7eeacd'
psql_uri = 'postgres://aaqgmutpyfxgmx:614e04f0ec7d6a687c0b4e8c6a9941391d70349037ac3b1384149752bd7eeacd@ec2-54-196-65-186.compute-1.amazonaws.com:5432/d12jneq73g7u2'
psql_herokucli = 'heroku pg:psql postgresql-trapezoidal-98002 --app kirana-bot'

# Channel Access Token
line_bot_api = LineBotApi('KBYcJt1ZmbmMnkQM0ZW6uREsAtE7QSARwDrVprACm91i3/zpvlJZVHXVVFnVDuRorEceLSqwx8qV/fIDE/qpJF1wdNMykK0kgHIxEeeNywBXIKvcWp+q9Rxw1a3C661yzKWgR/8AYzMt3eLgHAj3MwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('38cb174b5ffbf238b2b7048c47676654')

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

# Take user's sent text
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_profile = line_bot_api.get_profile(user_id=user_id)

    time_now = datetime.now()
    pesan_sql = '({}, {}, {}, {}-{}-{} {}:{}, {})'.format(
                user_profile.display_name, user_id, int(datetime.now().timestamp()),
                time_now.day, time_now.month, time_now.year, time_now.hour, time_now.minute,
                event.message.text)

    #psql_cur.execute("INSERT INTO riwayatcakap VALUES " + pesan_sql + ';')
    sent_msg = TextSendMessage(text=pesan_sql)
    line_bot_api.reply_message(event.reply_token, sent_msg)


import os
if __name__ == "__main__":
    psql_conn = psycopg2.connect(host=psql_host,
                                 database=psql_database, 
                                 user=psql_user,
                                 password=psql_password,
                                 port=psql_port)
    psql_cur = psql_conn.cursor()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)