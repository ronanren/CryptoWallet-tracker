# CryptoWallet-tracker

Crypto wallet tracker for telegram to track new transactions, stacking rewards and others activities on your wallets.
## Development 

```bash
pip install -r requirements.txt
python walletTracker.py
```

## Deploy

```bash
flyctl auth login
flyctl apps create <your-app-name>
flyctl secrets set API_KEY=<your telegram bot token>
flyctl secrets set CHAT_ID=<your chat id>
flyctl secrets set BTC=<your BTC address>
flyctl secrets set ETH=<your ETH address>
flyctl secrets set ELROND=<your ELROND address>
flyctl deploy

# stop app
flyctl scale count 0
# resume app
flyctl scale count 1
```
