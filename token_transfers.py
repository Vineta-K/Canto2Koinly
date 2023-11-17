import requests
import pandas as pd
import datetime

class TokenTransfers:

    required_headers = [
        "Date",
        "Sent Amount",
        "Sent Currency",
        "Received Amount",
        "Received Currency",
        "Fee Amount",
        "Fee Currency",
        "Net Worth Amount",
        "Net Worth Currency",
        "Label",
        "Description",
        "TxHash",
    ]

    def __init__(self, base_uri, wallet_address):
        self.wallet_address = wallet_address
        self.uri = base_uri + "/addresses/" + wallet_address + "/token-transfers"

    def get_txs_as_df(self):
        txs = requests.get(self.uri).json()['items']
        txs_flat = [pd.json_normalize(tx).to_dict(orient='records')[0] for tx in txs]
        out = []

        for tx in txs_flat:
            match tx['token.type']:
                case "ERC-20":
                    value = float(tx['total.value']) / 10**float(tx['total.decimals'])
                case "ERC-721":
                    value = 1
                case _:
                    raise Exception("Unsupported token transfer type")    
                #gonna have to write erc1155 here if u done it
            row = [
                tx["timestamp"],
                value               if tx['from.hash'] == self.wallet_address else None,
                tx['token.symbol']  if tx['from.hash'] == self.wallet_address else None,
                value               if tx['to.hash'] == self.wallet_address else None,
                tx['token.symbol']  if tx['to.hash'] == self.wallet_address else None,
                None,
                None,
                None,
                None,
                None,
                tx['token.name'],
                tx['tx_hash'],                
            ]
            out.append(row)
        return pd.DataFrame(out, columns = self.required_headers)




