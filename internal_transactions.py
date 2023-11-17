import requests
import pandas as pd
import datetime

class InternalTransactions:

    required_headers = [
        "Txhash",
        "Blockno",
        "UnixTimestamp",
        "DateTime",
        "ParentTxFrom",
        "ParentTxTo",
        "ParentTxCanto_Value",
        "From",
        "TxTo",
        "ContractAddress",
        "Value_IN(Canto)",
        "Value_OUT(Canto)",
        "CurrentValue @ $1/canto",
        "TxnFee(Canto)",
        "TxnFee(USD)",
        "Historical $Price/Canto",
        "Status",
        "ErrCode",
        "Type",
    ]

    def __init__(self, base_uri, wallet_address):
        self.wallet_address = wallet_address
        self.uri = base_uri + "/addresses/" + wallet_address + "/internal-transactions"

    def get_txs_as_df(self):
        txs = requests.get(self.uri).json()['items']
        txs_flat = [pd.json_normalize(tx).to_dict(orient='records')[0] for tx in txs]
        out = []
        for tx in txs_flat:
            row = [
                tx['transaction_hash'],
                tx['block'],
                datetime.datetime.strptime(tx['timestamp'],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
                tx["timestamp"],
                None,
                None,
                None,
                tx['from.hash'],
                tx['to.hash'],
                None,
                float(tx['value'])/1e18 if tx['to.hash'] == self.wallet_address else None,
                float(tx['value'])/1e18  if tx['from.hash'] == self.wallet_address else None,
                None,
                None,
                None,
                None,
                None,
                None,
                tx['type']
            ]
            out.append(row)
        return pd.DataFrame(out, columns = self.required_headers)




