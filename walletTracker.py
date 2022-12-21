from dotenv import load_dotenv
import os
import telebot, time
load_dotenv()

API_KEY = os.getenv('API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['commands', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Howdy, how are you doing?")
    # print(message.chat.id)

bot.polling(none_stop=True)