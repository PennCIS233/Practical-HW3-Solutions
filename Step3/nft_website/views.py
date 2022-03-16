from django.http import HttpResponse
import requests

from algosdk.v2client import algod


def serve_image(request):
    algod_client = algod.AlgodClient(
        algod_token="",
        algod_address="https://testnet-algorand.api.purestake.io/ps2",
        headers={"X-API-Key": "3oFTnjf15h9rHdK3QnCcO18tCSIyL1PIa4JvGCTU"}
    )
    asset_id = 75519703 
    asset = algod_client.asset_info(asset_id)
    url = asset['params']['url']
    print(url)
    img_response = requests.get(url)
    return HttpResponse(img_response.content, content_type="image/jpeg")

def home_page(request):
    return HttpResponse("<h1>Visit localhost:8000/nft to view your NFT!</h1>")