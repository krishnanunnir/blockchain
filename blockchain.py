import json
from time import time
import hashlib
from uuid import uuid4
from flask import Flask, jsonify, request
import sys



app=Flask(__name__)
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.current_transactions=[]
        self.new_block(previous_hash=1,proof=100)

    def new_block(self,proof,previous_hash=None):
        block={
            'index': len(self.chain) + 1,
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
        return self.last_block['index']+1

    @property
    def last_block(self):
        return self.chain[-1]


    @staticmethod
    def hash(block):
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self,last_proof):
        proof=0
        print("proof of work function called",file=sys.stderr)
        while(not self.valid_proof(proof,last_proof)):
            proof+=1;
        return proof


    @staticmethod
    def valid_proof(proof,last_proof):
        guess_hash=f'{proof}{last_proof}'.encode()
        return hashlib.sha256(guess_hash).hexdigest()[:4]=='0000'

node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()



@app.route('/transaction/new',methods=['POST'])
def transaction():
    unit = request.get_json()
    req_values=['sender','reciever','data']
    index=blockchain.new_transactions(unit['sender'],unit['reciever'],unit['amount'])
    response={'message':f'Transaction will be added to the block {index}'}
    return jsonify(response),200




@app.route('/mine/',methods=['GET'])
def mine():
    print('This error output', file=sys.stderr)
    last_blockchain = blockchain.last_block
    last_proof = last_blockchain['proof']
    blockchain.new_transactions(sender="0",reciever=node_identifier,amount=1)
    proof = blockchain.proof_of_work(last_proof)
    previous_hash=blockchain.hash(last_blockchain)
    block = blockchain.new_block(proof,previous_hash)

    response = {
        'index':block['index'],
        'time':time(),
        'transactions':block['transactions'],
        'previous_hash':block['previous_hash'],
        'proof':proof,
    }
    return jsonify(response),200;

@app.route('/chain',methods=['GET'])
def chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response),200

if __name__=="__main__":
    app.run('0.0.0.0',port=5000)
