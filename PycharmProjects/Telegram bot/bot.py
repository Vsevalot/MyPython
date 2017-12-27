# -*- coding: utf-8 -*-
import config # pip install pytelegrambotapi
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def sendEchoMsg(message):
    if message.chat.first_name=="Vitaly":
        bot.send_message(message.chat.id, "{} says: {}".format("The king of microcontroll", message.text))
    else:
        bot.send_message(message.chat.id, "{} says: {}".format(message.chat.first_name, message.text))

if __name__ == '__main__':
    bot.polling(none_stop=True)