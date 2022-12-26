import requests

def get_economics_egld():
    url = "https://api.elrond.com/economics"
    response = requests.request("GET", url)
    response = response.json()
    message = "<b>Elrond Economics:</b>\n\n" + \
              "Price: <code>$" + "%.2f" % response['price'] + "</code>\n" + \
              "Staked: <code>" + "%.2f" % (response['staked']/response['circulatingSupply'] * 100) + "%</code>\n" + \
              "APR: <code>" + "%.2f" % (response['apr'] * 100) + "%</code>\n"
    return message

def get_account_delegation_egld(address):
    url = "https://api.elrond.com/accounts/" + address + "/delegation"
    response = requests.request("GET", url)
    response = response.json()
    message = "<b>Elrond Delegation Wallet:</b>\n\n"
    for delegation in response:
        url = "https://api.elrond.com/providers/" + delegation['contract']
        validator = requests.request("GET", url)
        validator = validator.json()
        message += "Validator: <b>" + validator['identity'] + "</b>\n" + \
                   "APR: <code>" + "%.2f" % validator['apr'] + "% -> " + "%.2f" % (validator['apr'] - (validator['apr'] * validator['serviceFee'])) + "%</code>\n" + \
                   "Fee: <code>" + "%.2f" % (validator['serviceFee'] * 100) + "%</code>\n" + \
                   "Staked: <code>" + "%.2f" % (float(delegation['userActiveStake'])/10**18) + " EGLD</code>\n" + \
                   "claimable rewards: <code>" + "%.2f" % (float(delegation['claimableRewards'])/10**18) + " EGLD</code>\n\n"
    return message
