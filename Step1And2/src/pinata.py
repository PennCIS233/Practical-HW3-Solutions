# Doc: https://docs.pinata.cloud/api-pinning/pin-file
import os
import requests
import json
import hashlib
import base64
import mimetypes
from secrets import PINATA_API_KEY, PINATA_API_SECRET
from ipfs2bytes32 import ipfscidv0_to_byte32


PINATA_URL = "https://api.pinata.cloud"
PINATA_HEADERS = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_API_SECRET,
}



def save_arc3_json(json_string):
    with open('nft.json', 'w') as f:
        json.dump(json_string, f)

def pin_to_ipfs(file_path):
    pinning_url = "/pinning/pinFileToIPFS"
    final_url = PINATA_URL + pinning_url

    nft_file = open(file_path, 'rb')

    files = {
        'file': nft_file,
    }
    r = requests.post(final_url, files=files, headers=PINATA_HEADERS)

    if r.status_code == requests.codes.ok:
        r = r.json()
        return r["IpfsHash"]

    return r.raise_for_status()


def save_art_to_ipfs(asset_name, asset_description, nft_file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'art', nft_file_name)

    ipfs_cid = pin_to_ipfs(path)
    ipfs_address = "ipfs://{}".format(ipfs_cid)

    integrity = ipfscidv0_to_byte32(ipfs_cid)
    integrity = base64.b64encode(bytes.fromhex(integrity))
    integrity = "sha256-{}".format(integrity.decode('utf-8'))

    file_mimetype, _ = mimetypes.guess_type(path)

    metadata = {
        'name': asset_name,
        'description': asset_description,
        'image': ipfs_address,
        'image_integrity': integrity,
        'ipfs_mimetype': file_mimetype,
        'properties': {
            'file_url': nft_file_name,
            'file_url_integrity': integrity,
            'file_url_mimetype': file_mimetype,
        }
    }

    metadata_json_string = json.dumps(metadata)

    hash = hashlib.new("sha512_256")
    hash.update(b"arc0003/amj")
    hash.update(metadata_json_string.encode("utf-8"))
    ipfs_metadata = hash.digest()

    save_arc3_json(metadata_json_string)

    return ipfs_cid, ipfs_address, ipfs_metadata
