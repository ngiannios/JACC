from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from utility.log import Log
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
# wallet = Wallet()
# blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET'])
def get_network():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else: 
        response = {
            'message': 'Saving the keys failed.'
        }
        return jsonify(response), 500

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys(): 
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading the keys failed.'
        }
        return jsonify(response), 500



@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    Log.log_message('broadcast-transaction started with values{}'.format(values), port)
    if not values:
        response = {'message': 'No data found.'}
        Log.log_error('400', response, port)
        return jsonify(response), 400
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required):
        response = {'message': 'Some data are missing.'}
        Log.log_error('400', response, port)
        return jsonify(response), 400
    Log.log_message('Broadcast-transaction', port)
    success = blockchain.add_transaction(values['recipient'], values['sender'], values['signature'], values['amount'], True)
    Log.log_message('Broadcast-transaction Ended', port)
    if success: 
        response= {
            'message': 'Succesfully added transaction',
            'transaction': {
                'sender': values['sender'], 
                'recipient':values['recipient'],
                'amount':values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed..!'
        }
        return jsonify(response), 500

@app.route('/broadcast-block', methods=['POST'])
def broadcast_blocks():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    
    if 'block' not in values:
        response = {'message': 'Some data is missing.'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': ' Block added'}
            return jsonify(response), 200
        else:
            response = {'message': 'Block seems invalid.'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {'message': 'Block seems to defer from local blockchain.'}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {'message': 'Blockchain seems to be shorter, block not added'}
        return jsonify(response), 409

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.open_transactions
    js_transactions = [tx.to_json() for tx in transactions]
    return jsonify(js_transactions), 200


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup.'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        response= {
            'message': 'Succesfully added transaction',
            'transaction': {
                'sender': wallet.public_key, 
                'recipient':recipient,
                'amount':amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed..!'
        }
        return jsonify(response), 500

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Fetched balance succesfully',
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 202
    else:
        response = {
            'message': 'Loading balance failed!',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.resolve_conflicts:
        response = {'message': 'Resolve conflicts first, block not added!'}
        Log.log_error(409, response, port)
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block != None :
        dict_block = block.to_json()
        response = {
            'message': 'Block added succesfully',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        Log.log_status(201, response, port) 
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_set_up': wallet.public_key != None
        }
        Log.log_error(500, response, port)
        return jsonify(response), 500


@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {
            'message': 'Chain was replaced..'
        }
    else:
        response = {
            'message': 'Local chain kept..'
        }
    Log.log_status(200, response, port)
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.to_json() for block in chain_snapshot]
    return jsonify(dict_chain), 200

@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached.'
        }
        return jsonify(response), 400
    
    if 'node' not in values: 
        response = {
            'message': 'No node data attached.'
        }
        return jsonify(response), 400
    node = values.get('node')
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added succesfully.',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None: 
        response = {
            'message': 'No node attached.'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed succesfully.',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

@app.route('/node', methods=['GET'])
def get_node():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 201



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=3200)
    args = parser.parse_args()
    port = args.port
    Log.log_message('Server started at port:{}'.format(port), port)
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='127.0.0.1', port=port)