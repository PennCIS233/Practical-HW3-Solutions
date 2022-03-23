from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import PaymentTxn, AssetConfigTxn, AssetTransferTxn, LogicSigTransaction
from algosdk import mnemonic, encoding
from utils import wait_for_confirmation, get_default_params
from secrets import (
    ALGOD_ADDRESS,
    ALGOD_HEADERS,
    account_private_key,
    account_address,
)
from ipfs_info import (
    ASSET_NAME,
    IPFS_METADATA_ADDRESS,
    IPFS_METADATA_HASH
)


def create_ASA(client, address, private_key):
    params = get_default_params(client)
    txn = AssetConfigTxn(
        sender=address,
        sp=params,
        total=1,
        default_frozen=False,
        asset_name=ASSET_NAME,
        manager="",
        reserve="",
        freeze="",
        clawback="",
        url=IPFS_METADATA_ADDRESS + "#arc3",
        metadata_hash=IPFS_METADATA_HASH,
        decimals=0,
        strict_empty_address_check=False)

    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)

    wait_for_confirmation(client, tx_id, 5)

    pending_txn = client.pending_transaction_info(tx_id)
    asset_id = pending_txn['asset-index']

    print("Transaction ID: {}".format(tx_id))
    print("Asset ID: {}".format(asset_id))

def main():
    algod_client = algod.AlgodClient(
        algod_token="",
        algod_address=ALGOD_ADDRESS,
        headers=ALGOD_HEADERS,
    )
    create_ASA(algod_client, account_address, account_private_key)

if __name__ == '__main__':
    main()
