import telebot
import websocket
import threading
from pycoingecko import CoinGeckoAPI
import time, datetime
import os
import json

API_KEY = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')
BTC = os.environ.get("BTC")
ETH = os.environ.get("ETH")

bot = telebot.TeleBot(API_KEY)
cg = CoinGeckoAPI()

@bot.message_handler(commands=['start', 'commands', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Commands:\n\n/commands\n/help")
    # print(message.chat.id)

def track_wallet():
    while 1:
        if (int(datetime.datetime.now().strftime("%S")) % 60 == 0):
            # bot.send_message(CHAT_ID, datetime.datetime.now().strftime("%H:%M:%S"))
            pass
        time.sleep(1)

def on_open_btc(wsapp):
    wsapp.send(json.dumps({"op": "addr_sub", "addr": BTC}))

def on_message_btc(wsapp, message):
    data = json.loads(message)
    bitcoin_price = cg.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
    total_send = 0
    total_received = 0

    text = "<b>New ₿ transaction:</b>\n\n" + "From: \n"
    for address_from in data['x']['inputs']:
        text += "<a href='https://bitcoinexplorer.org/address/" + address_from['prev_out']['addr'] + "'>" + address_from['prev_out']['addr'][0:5] + ".." + address_from['prev_out']['addr'][-5:] + "</a> " + "%.6f" % (address_from['prev_out']['value'] / 10**8) + "₿ ≈ " + "%.2f" % (bitcoin_price * (address_from['prev_out']['value'] / 10**8)) + "$\n" 
        total_send += address_from['prev_out']['value'] / 10**8
    text += "\nTo: \n" 

    for address_to in data['x']['out']:
        text += "<a href='https://bitcoinexplorer.org/address/" + address_to['addr'] + "'>" + address_to['addr'][:5] + ".." + address_to['addr'][-5:] + "</a> " + "%.6f" % (address_to['value'] / 10**8) +  "₿ ≈ " + "%.2f" % (bitcoin_price * (address_to['value'] / 10**8)) + "$\n" 
        total_received += address_to['value'] / 10**8

    text += "\nValue received: " + "%0.6f" % total_received + "₿" + " ≈ " + "%.2f" % (bitcoin_price * total_received) + "$" \
    + "\nFees: " + "%0.6f" % (total_send - total_received) + "₿" + " ≈ " + "%.2f" % (bitcoin_price * (total_send - total_received)) + "$" + \
    "\n\n" + "<a href='https://bitcoinexplorer.org/tx/" + data['x']['hash'] + "'>Tx hash</a>"
    bot.send_message(CHAT_ID, text, parse_mode='html')

def init_websocket():
    # Bitcoin tracker
    ws_btc = websocket.WebSocketApp("wss://ws.blockchain.info/inv", on_message=on_message_btc, on_open=on_open_btc)
    ws_btc.run_forever()

    # Ethereum tracker
    

track_wallet_thread = threading.Thread(target=track_wallet)
track_wallet_thread.start()

init_websocket_thread = threading.Thread(target=init_websocket)
init_websocket_thread.start()
bot.polling()