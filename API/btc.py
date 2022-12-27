from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def get_economics_btc():
    bitcoin_info = cg.get_coin_by_id(id='bitcoin', localization=False, tickers=False, market_data=True, community_data=False, developer_data=False, sparkline=False)
    message = "<b>Bitcoin Economics:</b>\n\n" + \
              "Price: <code>$" + "%.2f" % bitcoin_info['market_data']['current_price']['usd']  + \
              "</code>\nMarket Cap change 24h: <code>" + "%.2f" % bitcoin_info['market_data']['market_cap_change_percentage_24h'] + "%</code>\n\n" + \
              "24h High: <code>$" + "%.2f" % bitcoin_info['market_data']['high_24h']['usd'] + \
              "</code>\n24h Low: <code>$" + "%.2f" % bitcoin_info['market_data']['low_24h']['usd'] + \
              "</code>\n24h Change: <code>" + "%.2f" % bitcoin_info['market_data']['price_change_percentage_24h'] + "%</code>\n\n" + \
              "7d Change: <code>" + "%.2f" % bitcoin_info['market_data']['price_change_percentage_7d'] + "%</code>\n" + \
              "30d Change: <code>" + "%.2f" % bitcoin_info['market_data']['price_change_percentage_30d'] + "%</code>\n" + \
              "1y Change: <code>" + "%.2f" % bitcoin_info['market_data']['price_change_percentage_1y'] + "%</code>\n\n" + \
              "All Time High: <code>$" + "%.2f" % bitcoin_info['market_data']['ath']['usd'] + \
              "</code>\nAll Time High Percentage: <code>" + "%.2f" % bitcoin_info['market_data']['ath_change_percentage']['usd'] + "%</code>\n\n" 
    return message

def get_on_message_btc(data):
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
    return text