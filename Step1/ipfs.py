# Doc: https://docs.pinata.cloud/api-pinning/pin-file
import os
import requests
import json
import hashlib
import base64
import mimetypes
from ipfs2bytes32 import ipfscidv0_to_byte32

from secrets import (
    PINATA_API_KEY, 
    PINATA_API_SECRET
)
from art.art_info import (
    FILE_NAME,
    ASSET_NAME,
    ASSET_DESCRIPTION
)


PINATA_IMAGE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
PINATA_JSON_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
PINATA_HEADERS = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_API_SECRET,
}

def pin_image_to_ipfs(file_path):
    nft_file = open(file_path, 'rb')
    files = {
        'file': nft_file,
    }

    response = requests.post(PINATA_IMAGE_URL, files=files, headers=PINATA_HEADERS)
    if response.status_code == requests.codes.ok:
        return response.json()["IpfsHash"]
    else:
        return response.raise_for_status()


def pin_metadata_to_ipfs(metadata):
    response = requests.post(PINATA_JSON_URL, json=metadata, headers=PINATA_HEADERS)

    if response.status_code == requests.codes.ok:
        return response.json()["IpfsHash"]
    else:
        return response.raise_for_status()


def compute_integrity(ipfs_image_cid):
    integrity = ipfscidv0_to_byte32(ipfs_image_cid)
    integrity = base64.b64encode(bytes.fromhex(integrity))
    integrity = "sha256-{}".format(integrity.decode('utf-8'))
    return integrity


def compute_metadata_hash(metadata):
    metadata_json_string = json.dumps(metadata)

    hash = hashlib.sha256()
    hash.update(metadata_json_string.encode("utf-8"))
    ipfs_metadata_hash = hash.digest()
    return ipfs_metadata_hash


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'art', FILE_NAME)

    ipfs_image_cid = pin_image_to_ipfs(path)
    ipfs_image_address = "ipfs://{}".format(ipfs_image_cid)

    integrity = compute_integrity(ipfs_image_cid)

    file_mimetype, _ = mimetypes.guess_type(path)

    metadata = {
        'name': ASSET_NAME,
        'description': ASSET_DESCRIPTION,
        'image': ipfs_image_address,
        'image_integrity': integrity,
        'image_mimetype': file_mimetype,
    }

    ipfs_metadata_cid = pin_metadata_to_ipfs(metadata)
    ipfs_metadata_address = "ipfs://{}".format(ipfs_metadata_cid)

    ipfs_metadata_hash = compute_metadata_hash(metadata) 

    print("IPFS metadata CID: {}".format(ipfs_metadata_cid))
    print("IPFS metadata address: {}".format(ipfs_metadata_address))
    print("IPFS metadata hash: {}".format(ipfs_metadata_hash))

if __name__ == '__main__':
    main()
