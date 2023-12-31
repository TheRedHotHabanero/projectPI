from web3 import Web3
from solcx import compile_standard, install_solc

import json

with open("./Credentials.sol", "r") as file:
    smart_contract_demo = file.read()

install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Credentials.sol" : { "content" : smart_contract_demo }},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi","metadata","evm.bytecode","evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0",
)

with open("compiled_code.json","w+") as file:
    json.dump(compiled_sol, file)

# get abi
abi = compiled_sol["contracts"]["Credentials.sol"]["Credentials"]["abi"]

# bytecode
bytecode = compiled_sol["contracts"]["Credentials.sol"]["Credentials"]["evm"]["bytecode"]["object"]


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address= "0xC36Eb120426B0A6A85a8b9e400dFb7cF74B7290D"
private_key = "0xf86a2c27cd353e75b3da95a65aeb517331466fac6c1df8228f72d8c154ff3ca4"

SmartContractDemo = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
transaction = SmartContractDemo.constructor().build_transaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": w3.eth.get_transaction_count("0xC36Eb120426B0A6A85a8b9e400dFb7cF74B7290D")
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract!")
# Sent it
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for Transaction to finish...")

tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract Deployed to {tx_receipt.contractAddress}")