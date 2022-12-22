import os
import telebot

API_KEY = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['commands', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Howdy, how are you doing?")
    # print(message.chat.id)

bot.polling(none_stop=True)