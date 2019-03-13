from utility.log import Log
from wallet import Wallet
from blockchain import Blockchain

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    parser.add_argument('-n', '--nodeUrl', type=str, default='')
    args = parser.parse_args()
    port = args.port
    node_Url = args.nodeUrl
    Log.log_message('A new node URL"{}" will be added at port:{}'.format(node_Url, port), port)
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    blockchain.add_peer_node(node_Url)
