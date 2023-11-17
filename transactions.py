import requests
import pandas as pd
import datetime

class Transactions:

    required_headers = [
        "Txhash",
        "Blockno",
        "UnixTimestamp",
        "DateTime",
        "From",
        "To",
        "ContractAddress",
        "Value_IN(Canto)",
        "Value_OUT(Canto)",
        "CurrentValue @ $1/canto",
        "TxnFee(Canto)",
        "TxnFee(USD)",
        "Historical $Price/Canto",
        "Status",
        "ErrCode",
        "Method",
    ]

    def __init__(self, base_uri, wallet_address):
        self.wallet_address = wallet_address
        self.uri = base_uri + "/addresses/" + wallet_address + "/transactions"

    def get_txs_as_df(self):
        txs = requests.get(self.uri).json()['items']
        txs_flat = [pd.json_normalize(tx).to_dict(orient='records')[0] for tx in txs]
        out = []
        for tx in txs_flat:
            row = [
                tx['hash'],
                tx['block'],
                datetime.datetime.strptime(tx['timestamp'],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                tx["timestamp"],
                tx['from.hash'],
                tx['to.hash'],
                None,
                float(tx['value'])/1e18 if tx['to.hash'] == self.wallet_address else None,
                float(tx['value'])/1e18  if tx['from.hash'] == self.wallet_address else None,
                None,
                float(tx['fee.value'])/1e18,
                None,
                None,
                tx['status'],
                None,
                tx['method']
            ]
            out.append(row)
        return pd.DataFrame(out, columns = self.required_headers)




