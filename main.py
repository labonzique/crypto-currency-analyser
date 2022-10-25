import requests
from datetime import datetime
from auth import token, binance
import telebot
from telebot import types
import bot_manager as bm


def telegram_bot(token):
    bot = telebot.TeleBot(token)
    response_text = ["BTC", "ETH", "BNB", "LTC", "BSW", "SOL"]

    markup = types.ReplyKeyboardMarkup(True, True)
    for i in response_text:
        btn = types.KeyboardButton(i)
        markup.add(btn)
    markup.add(types.KeyboardButton(" Другое "))



    def get_price_currency(name_currency: str):
        req = requests.get(binance)
        response = req.json()
        for currency in response:
            if currency['symbol'] == name_currency:
                return currency['price']



    def send_text(message):
        i = message.text.lower()
        try:
            sell_price = get_price_currency(f'{i.upper()}USDT')
            bot.send_message(
                message.chat.id,
                f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nЦена {i.upper()}: {round(float(sell_price), 4)} USDT")

            markup1 = types.InlineKeyboardMarkup(row_width=2)
            rep1 = types.InlineKeyboardButton("Да", callback_data='yes')
            rep2 = types.InlineKeyboardButton("Нет", callback_data='no')
            markup1.add(rep1, rep2)
            bot.send_message(
                message.chat.id,
                "Еще надо че то?",
                reply_markup=markup1)

        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id,
                "Не могу такую найти..\nДавай по новой",
                reply_markup=markup)



    @bot.message_handler(commands=['start'])
    def start_message(message):

        bot.send_message(message.chat.id, "Здарова заебал, могу расценки показать что ли..", reply_markup=markup)

        if bm.check_user(message) == True:
            pass
        else:
            bm.add_new_user(message)



    @bot.message_handler(content_types=['text'])
    def chat_message(message):

        if message.text.lower() in list(map(lambda x: x.lower(), response_text)):
            send_text(message)

        elif message.text.lower() == "другое":
            bot.send_message(message.chat.id, "Напиши название валюты")
            bot.register_next_step_handler(message, send_text)

        else:
            bot.send_message(message.chat.id, "Ты че еблан? Нормально пиши..", reply_markup=markup)



    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            if call.message:
                if call.data == 'yes':
                    bot.send_message(call.message.chat.id, "Выбери, что нужно", reply_markup=markup)


                elif call.data == 'no':
                    bot.send_message(call.message.chat.id, "Пидора ответ))0) \nЯ выключаюсь тогда.")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Еще надо че то?", reply_markup=None)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Еще надо че то?", reply_markup=None)

                bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=True, text='GG')

        except Exception as e:
            pass


    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
