from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import PaymentTxn, AssetConfigTxn, AssetTransferTxn, LogicSigTransaction
from algosdk import mnemonic, encoding
import json
import base64
from utils import wait_for_confirmation, get_default_params
from secrets import (
    ALGOD_ADDRESS,
    ALGOD_HEADERS,
    account_private_key,
    account_address,
)
from pinata import save_art_to_ipfs


def create_nft(client, address, private_key, nft_info):
    ipfs_cid, ipfs_address, ipfs_metadata = save_art_to_ipfs(
        nft_info['asset-name'],
        nft_info['asset-description'],
        nft_info['file-name'])

    params = get_default_params(client)
    txn = AssetConfigTxn(
        sender=address,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name=nft_info['unit-name'],
        asset_name=nft_info['asset-name'],
        manager="",
        reserve="",
        freeze="",
        clawback="",
        url=ipfs_address,
        metadata_hash=ipfs_metadata,
        decimals=0,
        strict_empty_address_check=False)

    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)

    wait_for_confirmation(client, tx_id, 5)

    pending_txn = client.pending_transaction_info(tx_id)
    asset_id = pending_txn['asset-index']

    print("NFT CID: {}".format(ipfs_cid))
    print("Transaction ID: {}".format(tx_id))
    print("Asset ID: {}".format(asset_id))



def main():
    algod_client = algod.AlgodClient(
        algod_token="",
        algod_address=ALGOD_ADDRESS,
        headers=ALGOD_HEADERS,
    )
    create_nft(algod_client, account_address, account_private_key, get_nft_info())

if __name__ == '__main__':
    main()
