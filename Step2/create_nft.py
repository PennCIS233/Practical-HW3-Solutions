from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import PaymentTxn, AssetConfigTxn, AssetTransferTxn, LogicSigTransaction
from algosdk import mnemonic, encoding
import json
import base64

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "3oFTnjf15h9rHdK3QnCcO18tCSIyL1PIa4JvGCTU"}
)

def wait_for_confirmation(client, transaction_id, timeout):
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return

        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception('pool error: {}'.format(pending_txn["pool-error"]))

        client.status_after_block(current_round)
        current_round += 1

    raise Exception('pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

def get_default_params(client):
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000
    return params

address = "ATPUKE6I3PMJBBEG4CAORCMCV2BMZHFY6ICAWK2UNL4OG2IGPFBN5JPY3E"
private_key = mnemonic.to_private_key("observe cry rose display remain poem junk march grace hen quit blue strategy shrimp nasty peasant brother cheese enrich series foam spread note abandon fury")

# Create NFT ASA

params = get_default_params(algod_client)

txn = AssetConfigTxn(sender=address,
                     sp=params,
                     total=1,           # NFTs have totalIssuance of exactly 1
                     default_frozen=False,
                     unit_name="NFWatts",
                     asset_name="Alan Watts Pic",
                     manager="",
                     reserve="",
                     freeze="",
                     clawback="",
                     url="https://i.imgur.com/MhOb19A.png",
                     metadata_hash="",
                     decimals=0,
                     strict_empty_address_check=False)        # NFTs have decimals of exactly 0

signed_txn = txn.sign(private_key)
txid = algod_client.send_transaction(signed_txn)
print(txid)

wait_for_confirmation(algod_client, txid, 5)

pending_txn = algod_client.pending_transaction_info(txid)
asset_id = pending_txn["asset-index"]
print("asset id is :")
print(asset_id)
