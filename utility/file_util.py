from collections import OrderedDict
import json
import pickle
from block import Block
from transaction import Transaction


FILE_ACCESS_METHOD='JSON'
FILENAME_JSON = 'blockchain{}.txt'
FILENAME_PICKLE = 'blockchain{}.p'


class FileUtil:
    @staticmethod
    def __load_data_JSON(filename):
        try:
            with open(filename, mode='r') as f:
                file_content = f.readlines()
                
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                                block['index'],
                                block['previous_hash'],
                                converted_tx,
                                block['proof'],
                                block['timestamp']
                                )
                    
                    updated_blockchain.append(updated_block)
                # blockchain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                # open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                set_peer_nodes = set(peer_nodes)
                return {
                    'chain': updated_blockchain,
                    'ot': updated_transactions,
                    'peer_nodes': set_peer_nodes
                }
        except (IOError, IndexError):
            print('File not found!')
    
    @staticmethod
    def __load_data_PICKLE(filename):
        try:
            with open(filename, mode='rb') as f:
                file_content = pickle.loads(f.read())
                return file_content
        except (IOError, IndexError):
            print('File not found!')

    @classmethod
    def load_data(cls, node_id):
        if FILE_ACCESS_METHOD=='JSON':
            return cls.__load_data_JSON(FILENAME_JSON.format(node_id))
        else:
            return cls.__load_data_PICKLE(FILENAME_PICKLE.format(node_id))

    @staticmethod
    def __save_data_JSON(filename, blockchain, open_transactions, peered_nodes):
        try: 
            with open(filename, mode='w') as f:
                # f.write(json.dumps(blockchain))
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
                json.dump(saveable_chain, f)
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in open_transactions]
                json.dump(saveable_tx, f)
                f.write('\n')
                json.dump(list(peered_nodes), f)
                # f.write(str(open_transactions))
        except (IOError, IndexError):
            print('Saving failed!')

    @staticmethod    
    def __save_data_PICKLE(filename, blockchain, open_transactions, peered_nodes):
        try:
            with open(filename, mode='wb') as f:
                saved_data = {
                    'chain': blockchain,
                    'ot': open_transactions
                }
                pickle.dump(saved_data, f)
                pickle.dump(peered_nodes, f)
        except (IOError, IndexError):
            print('Saving failed!')

    @classmethod
    def save_data(cls, blockchain, open_transactions, peered_nodes, node_id):
        if FILE_ACCESS_METHOD=='JSON':
            cls.__save_data_JSON(FILENAME_JSON.format(node_id), blockchain, open_transactions, peered_nodes)
        else:
            cls.__save_data_PICKLE(FILENAME_PICKLE.format(node_id), blockchain, open_transactions, peered_nodes)        

