from algosdk import mnemonic

# TODO
#PINATA_API_KEY = "your-key-here"
PINATA_API_KEY = "16ca536bfba2e30bbf79"
#PINATA_API_SECRET = "your-secret-here"
PINATA_API_SECRET = "7c517c8261cda4ead0a43c5b9be30186d8e28770f6a147393acf0cbf65e7073e"

# TODO
#PURESTAKE_API_KEY = "your-purestake-key-here"
PURESTAKE_API_KEY = "1iMSUP8Kz94umVOCuQHxC3NnMEHgVjOH12cliIto"

#account_mnemonic = "mnemonic here" # TODO
account_mnemonic = "odor office connect cargo isolate soul field absent neither mammal crunch mercy produce alpha common another flash bottom then crime cereal green broken able knee" # TODO
account_private_key = mnemonic.to_private_key(account_mnemonic)
account_address = mnemonic.to_public_key(account_mnemonic)

ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_HEADERS = {"X-API-Key": PURESTAKE_API_KEY}
