import telebot
import websocket
import threading
import time
import os
import json
from API.egld import *
from API.btc import *

API_KEY = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')
BTC = os.environ.get("BTC")
ETH = os.environ.get("ETH")
ELROND = os.environ.get("ELROND")

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start', 'commands', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "<b>Commands:</b>\n\nBitcoin (₿)\n/btc_economics\n\nElrond (EGLD)\n/egld_economics\n/egld_delegation", parse_mode='html')
    # print(message.chat.id)

# BTC command
@bot.message_handler(commands=['btc_economics'])
def message_BTC(message):
    bot.send_message(message.chat.id, get_economics_btc(), parse_mode='html')

# EGLD commands
@bot.message_handler(commands=['egld_economics'])
def message_EGLD(message):
    bot.send_message(message.chat.id, get_economics_egld(), parse_mode='html')

@bot.message_handler(commands=['egld_delegation'])
def message_EGLD_Delegation(message):
    bot.send_message(message.chat.id, get_account_delegation_egld(ELROND), parse_mode='html')


# Track new events every minute
def track_wallet():
    while 1:
        check_new_elrond_transaction(ELROND, bot, CHAT_ID)
        time.sleep(60)

# Bitcoin tracker
def on_open_btc(wsapp):
    wsapp.send(json.dumps({"op": "addr_sub", "addr": BTC}))

def on_message_btc(wsapp, message):
    data = json.loads(message)
    bot.send_message(CHAT_ID, get_on_message_btc(data), parse_mode='html')

def init_websocket():
    # Bitcoin tracker
    ws_btc = websocket.WebSocketApp("wss://ws.blockchain.info/inv", on_message=on_message_btc, on_open=on_open_btc)
    ws_btc.run_forever()

track_wallet_thread = threading.Thread(target=track_wallet)
track_wallet_thread.start()

init_websocket_thread = threading.Thread(target=init_websocket)
init_websocket_thread.start()
bot.polling()