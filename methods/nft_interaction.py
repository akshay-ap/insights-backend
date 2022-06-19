from web3 import Web3, HTTPProvider
import json
from config import config


def update_to_claimable(nft_address: str, public_address: str, reward: int) -> (bool, str):
    try:
        with open("abi/erc721.json") as f:
            info_json = json.load(f)
            abi = info_json["abi"]

            network_address = config["NETWORK_ADDRESS"]
            web3 = Web3(HTTPProvider(network_address))
            nft_contract = web3.eth.contract(address=nft_address, abi=abi)
            oracle_address = config["ORACLE_PUBLIC_ADDRESS"]
            nonce = web3.eth.get_transaction_count(oracle_address)
            tx = nft_contract.functions.updateClaimable(public_address, reward).buildTransaction(
                {
                    'from': oracle_address,
                    "gasPrice": web3.eth.gas_price,
                    "chainId": int(config["CHAIN_ID"]),
                    # 'gas': 31000000000,
                    'nonce': nonce})
            signed = web3.eth.account.signTransaction(tx, config["ORACLE_PRIVATE_KEY"])  # Sign with private key
            web3.eth.sendRawTransaction(signed.rawTransaction)
            return True, signed.hash.hex()
    except Exception as e:
        print(e)
        return False, None
