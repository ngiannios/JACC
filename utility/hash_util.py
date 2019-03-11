import hashlib as hl
import json

class HashUtil:
    @staticmethod
    def hash_string_256(string):
        return hl.sha256(string).hexdigest()
    @classmethod
    def hash_block(cls, block):
        hashable_block = block.__dict__.copy()
        hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
        return cls.hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
    
