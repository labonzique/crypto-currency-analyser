from bot_loger import PgDriver
from datetime import datetime


def check_user(message):
    with PgDriver() as curr:
        curr.execute(f""" select tg_id from users where tg_id = %s """, [message.from_user.id])
        return bool(len(curr.fetchall()))


def add_new_user(message):
    with PgDriver() as curr:
        try:
            curr.execute(f""" insert into users (created, username, user_first_name, user_last_name, tg_id, is_bot, is_premium) 
            values (%s, %s, %s, %s, %s, %s, %s )""",
                         [datetime.utcfromtimestamp(message.date), message.from_user.username,
                          message.from_user.first_name, message.from_user.last_name,
                          message.from_user.id, message.from_user.is_bot,
                          bool(message.from_user.is_premium)])
        except Exception as ex:
            pass


def logg_message(message):
    with PgDriver() as curr:
        try:
            curr.execute(f""" insert into message_loggs(created, message, id_dialog, id_user) 
            values (%s, %s, %s, %s )""",
                         [datetime.utcfromtimestamp(message.date), message.text,
                          message.chat.id, message.from_user.id])
        except Exception as ex:
            pass
