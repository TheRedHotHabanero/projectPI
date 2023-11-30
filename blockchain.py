from web3 import Web3
import json

ganache_url = "http://127.0.0.1:8545"
registeredInstitutes = {"MIPT": 1, "MIFI": 2, "SPBGU": 3}

class Blockchain:
    def __init__(self, institute):
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        self.institute = institute

        with open('contractDetails.json') as f:
            contractDetails = json.load(f)
            contractAddress = self.web3.to_checksum_address(contractDetails["address"])
            abi = contractDetails["abi"]
        
        self.contract = self.web3.eth.contract(address=contractAddress, abi=abi)

        if institute in registeredInstitutes.keys():
            self.web3.eth.default_account = self.web3.eth.accounts[registeredInstitutes[institute]]
            print("Connected to blockchain with account: ", institute)
        else:
            self.web3.eth.default_account = self.web3.eth.accounts[0]
            print("Connected to blockchain with default account")
    
    def addBatchMerkleRoot(self, batch, batchMerkleRoot):
        self.contract.functions.addBatchMerkleRoot(self.institute, batch, batchMerkleRoot).transact()
    
    def verifyBatchMerkleRoot(self, institute, batch, batchMerkleRoot):
        return self.contract.functions.verifyBatchMerkleRoot(institute, batch, batchMerkleRoot).call()
    
    def registerInstitute(self, institute):
        self.contract.functions.registerInstitute(institute).transact()
        
