import json
from time import time
import hashlib
def blockchain:
    def __init__:
        self.chain=[]
        self.current_transactions=[]
        self.new_block()

    def new_block(self,previous_hash=None,proof):
        block={
            'index': len(self.chain)+1,
            'time':time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash,
            'proof':proof
        }
        self.current_transactions=[]
        self.chain.append(block)
        return block
    def new_transactions(self,sender,reciever,amount):
        transaction = {
            'sender':sender,
            'reciever':reciever,
            'amount': amount
        }
        self.current_transactions.append(transaction)
        return transaction

    @property
    def last_block(property):
        return self.chain[-1]
    @staticmethod
    def hash(block):
        block_string = json.dump(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hex_digest()

    def proof_of_work(self,last_proof):
        proof=0
        if(not valid_proof(proof,last_proof)){
            proof+=1;
        }

    def valid_proof(proof,last_proof):
        guess_hash=f'{proof}{last_proof}'
        return hashlib.sha256(guess_hash).hex_digest[:4]==='0000'