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
    markup.add(types.KeyboardButton(" Other "))



    def get_price_currency(name_currency: str):
        req = requests.get(binance)
        response = req.json()
        for currency in response:
            if currency['symbol'] == name_currency:
                return currency['price']



    def send_text(message):
        bm.logg_message(message)
        i = message.text.lower()
        try:
            sell_price = get_price_currency(f'{i.upper()}USDT')
            bot.send_message(
                message.chat.id,
                f"{datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M')}\nPrice {i.upper()}: {round(float(sell_price), 4)} USDT")

            markup1 = types.InlineKeyboardMarkup(row_width=2)
            rep1 = types.InlineKeyboardButton("Yes", callback_data='yes')
            rep2 = types.InlineKeyboardButton("No", callback_data='no')
            markup1.add(rep1, rep2)
            bot.send_message(
                message.chat.id,
                "Do you need something else?",
                reply_markup=markup1)

        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id,
                "Can't find anything..\nTry again",
                reply_markup=markup)



    @bot.message_handler(commands=['start'])
    def start_message(message):
        bm.logg_message(message)

        bot.send_message(message.chat.id, "Hi! I'm Crypto bot, I can show you price for currency. "
                                          "\nOr give you a forecast", reply_markup=markup)

        if bm.check_user(message) == True:
            pass
        else:
            bm.add_new_user(message)



    @bot.message_handler(content_types=['text'])
    def chat_message(message):
        bm.logg_message(message)
        if message.text.lower() in list(map(lambda x: x.lower(), response_text)):
            send_text(message)

        elif message.text.lower() == "other":
            bot.send_message(message.chat.id, "Write down the name of currency you want me to find.")
            bot.register_next_step_handler(message, send_text)

        else:
            bot.send_message(message.chat.id, "Can't understand you..\nPlease choose one of the options", reply_markup=markup)



    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        bm.logg_message(call.message)
        try:
            if call.message:

                if call.data == 'yes':
                    bot.send_message(call.message.chat.id, "Choose the option", reply_markup=markup)


                elif call.data == 'no':
                    bot.send_message(call.message.chat.id, "Okay, see you later!")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Do you need something else?", reply_markup=None)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Do you need something else?", reply_markup=None)

        except Exception as e:
            pass


    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
