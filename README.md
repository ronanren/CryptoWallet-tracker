# CryptoWallet-tracker

Crypto wallet tracker for telegram to track new transactions, stacking rewards and others activities on your wallets.

## Usage commands

- /help or /commands or /start - show available commands

<img src="https://raw.githubusercontent.com/ronanren/CryptoWallet-tracker/main/images/commands.jpg" width="150px">

- /btc_economics - show BTC economics

<img src="https://raw.githubusercontent.com/ronanren/CryptoWallet-tracker/main/images/btc_economics.jpg" width="250px">

- /egld_economics - show EGLD economics

<img src="https://raw.githubusercontent.com/ronanren/CryptoWallet-tracker/main/images/egld_economics.jpg" width="250px">

- /egld_delegation - show EGLD delegation

<img src="https://raw.githubusercontent.com/ronanren/CryptoWallet-tracker/main/images/egld_delegation.jpg" width="250px">

## Development 

```bash
pip install -r requirements.txt
python walletTracker.py
```

## Deploy

You can use flyctl or ~/.fly/bin/flyctl depending on your installation
```bash
flyctl auth login
flyctl apps create <your-app-name>
flyctl secrets set API_KEY=<your telegram bot token>
flyctl secrets set CHAT_ID=<your chat id>
flyctl secrets set BTC=<your BTC address>
flyctl secrets set ELROND=<your ELROND address>
flyctl deploy

# stop app
flyctl scale count 0
# resume app
flyctl scale count 1
```
