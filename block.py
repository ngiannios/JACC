from time import time
from utility.printable import Printable

class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time() if timestamp is None else timestamp
        self.proof = proof

    def __repr__(self):
        return 'Index {}, Previous Hash: {}, Proof: {}, Transactions: {}'.format(self.index, self.previous_hash, self.proof, self.transactions)

    def to_json(self):
        copy_to_json = super().to_json()
        copy_to_json['transactions'] = [tx.to_json() for tx in copy_to_json['transactions']]  
        return copy_to_json
