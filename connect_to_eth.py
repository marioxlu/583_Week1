import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider

'''If you use one of the suggested infrastructure providers, the url will be of the form
now_url  = f"https://eth.nownodes.io/{now_token}"
alchemy_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_token}"
infura_url = f"https://mainnet.infura.io/v3/{infura_token}"
'''


def connect_to_eth():
	url = "https://eth-mainnet.g.alchemy.com/v2/af1I02w3ZtSVoGgFEG9UFCMBGCNVHasF"  # FILL THIS IN
	w3 = Web3(HTTPProvider(url))
	assert w3.is_connected(), f"Failed to connect to provider at {url}"
	return w3


def connect_with_middleware(contract_json):
    # Load the contract address and ABI from the contract JSON file
    with open(contract_json, "r") as f:
        d = json.load(f)
        address = d['address']  # Contract address
        abi = d['abi']  # Contract ABI

    # BNB Testnet URL
    bnb_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
    w3 = Web3(HTTPProvider(bnb_url))

    # Inject middleware for Proof of Authority
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    assert w3.isConnected(), "Failed to connect to BNB testnet"

    # Create the contract object using ABI and address
    contract = w3.eth.contract(address=address, abi=abi)

    return w3, contract

if __name__ == "__main__":
    # Test both connections
    print("Testing Ethereum Mainnet Connection:")
    connect_to_eth()
    
    print("\nTesting BNB Testnet Connection:")
    w3, contract = connect_with_middleware("contract_info.json")
    print("Connected to BNB Testnet and contract successfully")
