import telebot
import websocket
import threading
import time, datetime
import os
import json

API_KEY = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['commands', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Commands:\n\n/commands\n/help")
    # print(message.chat.id)

def track_wallet():
    while 1:
        if (int(datetime.datetime.now().strftime("%S")) % 60 == 0):
            bot.send_message(CHAT_ID, datetime.datetime.now().strftime("%H:%M:%S"))
        time.sleep(1)

def on_open(wsapp):
    wsapp.send(json.dumps({"op": "unconfirmed_sub"}))

def on_message(wsapp, message):
    data = json.loads(message)
    text = "New Bitcoin transaction:\n\n" + data['x']['hash'] + "\n\n" + str(data['x']['out'][0]['value']) + " satoshis" + "\n\n" + data['x']['out'][0]['addr'] + "\n\n" + "https://blockchain.info/tx/" + data['x']['hash']
    bot.send_message(CHAT_ID, text)


def init_websocket():
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv", on_message=on_message, on_open=on_open)
    ws.run_forever()


track_wallet_thread = threading.Thread(target=track_wallet)
track_wallet_thread.start()

init_websocket_thread = threading.Thread(target=init_websocket)
init_websocket_thread.start()
bot.polling()