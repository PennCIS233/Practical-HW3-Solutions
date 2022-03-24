from django.http import HttpResponse
import requests

from algosdk.v2client import algod

from secrets import (
    ALGOD_ADDRESS,
    ALGOD_HEADERS
)

PINATA_GATEWAY = "https://gateway.pinata.cloud/ipfs/"

# TODO fill me out
ASSET_ID = 79849243

def serve_image(request):
    def ipfs_address_to_cid(address):
        return address.replace("ipfs://", "").replace("#arc3", "")

    algod_client = algod.AlgodClient(
        algod_token="",
        algod_address=ALGOD_ADDRESS,
        headers=ALGOD_HEADERS
    )

    asset = algod_client.asset_info(ASSET_ID)
    ipfs_metadata_address = asset['params']['url']
    ipfs_metadata_cid = ipfs_address_to_cid(ipfs_metadata_address)
    response = requests.get(PINATA_GATEWAY + ipfs_metadata_cid)
    if response.status_code != requests.codes.ok:
        return "Could not find IPFS metadata" 

    content_type = response.json()["image_mimetype"]
    ipfs_image_address = response.json()["image"]
    ipfs_image_cid = ipfs_address_to_cid(ipfs_image_address)
    img_response = requests.get(PINATA_GATEWAY + ipfs_image_cid)
    return HttpResponse(img_response.content, content_type=content_type)

def home_page(request):
    return HttpResponse("<h1>Visit localhost:8000/nft to view your NFT!</h1>")