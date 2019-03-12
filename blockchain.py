import functools
import hashlib as hl
import datetime 
import requests
from block import Block
from transaction import Transaction
from utility.hash_util import HashUtil
from  utility.file_util import FileUtil
from utility.verification import Verification
from wallet import Wallet
from utility.log import Log
from utility.misc import Misc


MINING_REWARD = 10
GUESS_HASS_PROOF_STRING = '00'


class Blockchain:

    def __init__(self, public_key, node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.load_data()
        self.resolve_conflicts = False

    @property
    def chain(self):
        return self.__chain[:]
    
    @chain.setter
    def chain(self, value):
        self.__chain = value

    @property
    def open_transactions(self):
        return self.__open_transactions[:]
    
    @open_transactions.setter
    def open_transactions(self, value):
        self.__open_transactions = value

    def get_guess_hass_proof_string(self):
        return GUESS_HASS_PROOF_STRING

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    # This function accepts two arguments.
    # One required one (transaction_amount) and one optional one 
    # The optional one is optional because it has a default value => [1]
    def load_data(self):
        file_content = FileUtil.load_data(self.node_id)
        if file_content is not None:
            self.__chain = file_content['chain']
            self.__open_transactions = file_content['ot']
            self.__peer_nodes = file_content['peer_nodes']

    def save_data(self): 
        FileUtil.save_data(self.chain, self.open_transactions, 
                            self.__peer_nodes, self.node_id)

    def get_balance(self, sender=None):
        """Calculate and return the balance for a participant.

        Arguments:
            :participant: The person for whom to calculate the balance.
        """
        if sender is None:
            if self.public_key is None:
                return None
            participant = self.public_key
        else:
            participant = sender
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of transactions that were already included in blocks of the blockchain
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of open transactions (to avoid double spending)
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        # Calculate the total amount of coins sent
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0, tx_sender, 0)
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum + 0, tx_recipient, 0)
        # Return the total balance
        return amount_received - amount_sent

    def add_transaction(self, recipient, sender, signature, amount=1.0, is_receiving=False):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = '{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender': sender, 'recipient': recipient, 'amount': amount, 'signature':signature})
                        if response.status_code == 400 or response.status_code == 500:
                            Log.log_error(response.status_code, 'broadcast-transaction error response from {}:{}'.format(url, response), self.node_id)
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        if self.public_key == None:
            return None        
        last_block = self.__chain[-1]
        hashed_block = HashUtil.hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = '{}/broadcast-block'.format(node)
            # Log.log_message(url, self.node_id)
            try:
                response = requests.post(url, json={'block':block.to_json()})
                Log.log_message(response, self.node_id)
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declinde, needs resolving!')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'], GUESS_HASS_PROOF_STRING)
        hashes_match = HashUtil.hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient']  and opentx.amount == itx['amount']  and opentx.signature == itx['signature'] :
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        Log.log_error('ValueError', 'Item was already removed', self.node_id)
        self.save_data()
        return True

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = HashUtil.hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof, GUESS_HASS_PROOF_STRING):
            proof += 1
        return proof

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = '{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'], block['previous_hash'], [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']], block['proof'], block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(self.chain)
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain, GUESS_HASS_PROOF_STRING):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, new_node):
        self.__peer_nodes.add(new_node)
        # get all the peer nodes of the added node
        url = '{}/node'.format(new_node)
        try:
            response = requests.get(url)
            peer_nodes = response.json()
            for peer_node in peer_nodes['all_nodes']:
                self.__peer_nodes.add(peer_node)
        except requests.exceptions.ConnectionError:
            Log.log_error(requests.exceptions.ConnectionError, 'ConnectionError', self.node_id)
            None
        Log.log_message(Misc.get_IP(self.node_id), self.node_id)
        try: 
            local_http_addr = 'http://{}:{}'.format(Misc.get_IP(self.node_id), self.node_id)
            response = requests.post(url, json={'node': local_http_addr})
            Log.log_error(response.status_code, response, self.node_id)
        except requests.exceptions.ConnectionError:
            None
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)
