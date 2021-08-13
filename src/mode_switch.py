
id_admins = ["U2cc53b28669cf7c907d47e8653c08c6a"]
admin_count = len(id_admins)
timeout_menit = 60  # Timeout pengguna menghubungi admin sejak terakhir chat

"""def example_save_database():
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
    psql_conn.commit()"""