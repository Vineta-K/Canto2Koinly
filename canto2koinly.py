import requests
import pandas as pd
import datetime

from transactions import Transactions
from token_transfers import TokenTransfers
from internal_transactions import InternalTransactions

WALLET_ADDRESS = ""
BASE_URI = "https://explorer.plexnode.wtf/api/v2/"

#Transactions
txs_df = Transactions(BASE_URI, WALLET_ADDRESS).get_txs_as_df()
print(txs_df.head())
txs_df.to_csv(f"transactions_{WALLET_ADDRESS}.csv", index=False)

#Tokens - use generic koinly format as I couldn't get the etherscan one to work
txs_df = TokenTransfers(BASE_URI,WALLET_ADDRESS).get_txs_as_df()
print(txs_df.head())
txs_df.to_csv(f"token_transfers_{WALLET_ADDRESS}.csv", index=False)

txs_df = InternalTransactions(BASE_URI,WALLET_ADDRESS).get_txs_as_df()
print(txs_df.head())
txs_df.to_csv(f"internal_transactions_{WALLET_ADDRESS}.csv", index=False)

