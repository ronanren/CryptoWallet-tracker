import time
import requests
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def get_economics_egld():
    url = "https://api.elrond.com/economics"
    response = requests.request("GET", url)
    response = response.json()
    egld_info = cg.get_coin_by_id(id='elrond-erd-2', localization=False, tickers=False, market_data=True, community_data=False, developer_data=False, sparkline=False)
    message = "<b>Elrond Economics:</b>\n\n" + \
              "Price: <code>$" + "%.2f" % egld_info['market_data']['current_price']['usd']  + \
              "</code>\nMarket Cap change 24h: <code>" + "%.2f" % egld_info['market_data']['market_cap_change_percentage_24h'] + "%</code>\n" + \
              "Staked: <code>" + "%.2f" % (response['staked']/response['circulatingSupply'] * 100) + "%</code>\n" + \
              "APR: <code>" + "%.2f" % (response['apr'] * 100) + "%</code>\n\n" + \
              "24h High: <code>$" + "%.2f" % egld_info['market_data']['high_24h']['usd'] + \
              "</code>\n24h Low: <code>$" + "%.2f" % egld_info['market_data']['low_24h']['usd'] + \
              "</code>\n24h Change: <code>" + "%.2f" % egld_info['market_data']['price_change_percentage_24h'] + "%</code>\n\n" + \
              "7d Change: <code>" + "%.2f" % egld_info['market_data']['price_change_percentage_7d'] + "%</code>\n" + \
              "30d Change: <code>" + "%.2f" % egld_info['market_data']['price_change_percentage_30d'] + "%</code>\n" + \
              "1y Change: <code>" + "%.2f" % egld_info['market_data']['price_change_percentage_1y'] + "%</code>\n\n" + \
              "All Time High: <code>$" + "%.2f" % egld_info['market_data']['ath']['usd'] + \
              "</code>\nAll Time High Percentage: <code>" + "%.2f" % egld_info['market_data']['ath_change_percentage']['usd'] + "%</code>\n\n" 
    return message

def get_account_delegation_egld(address):
    url = "https://api.elrond.com/accounts/" + address + "/delegation"
    response = requests.request("GET", url)
    response = response.json()
    egld_price = cg.get_price(ids='elrond-erd-2', vs_currencies='usd')['elrond-erd-2']['usd']
    total_staked = 0
    total_rewards = 0
    rewards_by_year = 0
    message = "<b>Elrond Delegation Wallet:</b>\n\n"
    for delegation in response:
        url = "https://api.elrond.com/providers/" + delegation['contract']
        validator = requests.request("GET", url)
        validator = validator.json()
        total_staked += float(delegation['userActiveStake'])/10**18
        total_rewards += float(delegation['claimableRewards'])/10**18
        rewards_by_year += float(delegation['userActiveStake'])/10**18 * ((validator['apr'] - (validator['apr'] * validator['serviceFee']))/100)
        message += "Validator: <b>" + validator['identity'] + "</b>\n" + \
                   "APR: <code>" + "%.2f" % validator['apr'] + "% -> " + "%.2f" % (validator['apr'] - (validator['apr'] * validator['serviceFee'])) + "%</code>\n" + \
                   "Fee: <code>" + "%.2f" % (validator['serviceFee'] * 100) + "%</code>\n" + \
                   "Staked: <code>" + "%.2f" % (float(delegation['userActiveStake'])/10**18) + " EGLD ≈ $" + "%.2f" % (float(delegation['userActiveStake'])/10**18 * egld_price) + "</code>\n" + \
                   "claimable rewards: <code>" + "%.2f" % (float(delegation['claimableRewards'])/10**18) + " EGLD ≈ $" + "%.2f" % (float(delegation['claimableRewards'])/10**18 * egld_price) + "</code>\n\n"
    message += "Total Staked: <code>" + "%.2f" % total_staked + " EGLD ≈ $" + "%.2f" % (total_staked * egld_price) + "</code>\n" + \
                "Total Claimable Rewards: <code>" + "%.2f" % total_rewards + " EGLD ≈ $" + "%.2f" % (total_rewards * egld_price) + "</code>\n\n" + \
                "Rewards by Day: <code>" + "%.3f" % (rewards_by_year/365) + " EGLD ≈ $" + "%.2f" % ((rewards_by_year/365) * egld_price) + "</code>\n" + \
                "Rewards by Month: <code>" + "%.2f" % (rewards_by_year/12) + " EGLD ≈ $" + "%.2f" % ((rewards_by_year/12) * egld_price) + "</code>\n" + \
                "Rewards by Year: <code>" + "%.2f" % rewards_by_year + " EGLD ≈ $" + "%.2f" % (rewards_by_year * egld_price) + "</code>\n\n"
    return message

def check_new_elrond_transaction(address, bot, chat_id):
    url = "https://api.elrond.com/accounts/" + address + "/transactions"
    response = requests.request("GET", url)
    response = response.json()
    egld_price = cg.get_price(ids='elrond-erd-2', vs_currencies='usd')['elrond-erd-2']['usd']
    message = "<b>New Elrond Transactions:</b>\n\n"
    for transaction in response:
        if (transaction['timestamp'] >= int(time.time()) - 60):
            message += "From: <a href='https://explorer.elrond.com/accounts/" + transaction['sender'] +"'>" + transaction['sender'][0:5] + ".." + transaction['sender'][-5:] + "</a>\n" + \
                       "To: <a href='https://explorer.elrond.com/accounts/"+ transaction['receiver'] + "'>" + transaction['receiver'][0:5] + ".." + transaction['receiver'][-5:] + "</a>\n\n" 
            if ("function" in transaction): 
                message += "Function: <code>" + transaction['function'] + "</code>\n"
            message += "Amount: <code>" + "%.3f" % (float(transaction['value'])/10**18) + " EGLD ≈ $" + "%.2f" % (float(transaction['value'])/10**18 * egld_price) + "</code>\n" + \
                       "Fee: <code>" + "%.5f" % (float(transaction['fee'])/10**18) + " EGLD ≈ $" + "%.4f" % (float(transaction['fee'])/10**18 * egld_price) + "</code>\n\n" + \
                        "<a href='https://explorer.elrond.com/transactions/" + transaction['txHash'] + "'>Tx hash</a>"
            bot.send_message(chat_id, message, parse_mode='html')
            message = "<b>New Elrond Transactions:</b>\n\n"
        else:
            break