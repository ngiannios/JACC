from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
# wallet = Wallet()
# blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route('/', methods=['GET'])
def get_ui():
    return 'Python and flask is working..!!' 
    #send_from_directory('ui', 'node.html')

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    # parser.add_argument('-i', '--ip', type=str, default='0.0.0.0')
    args = parser.parse_args()
    port = args.port
    # ip = args.ip
    # app.run(host='0.0.0.0', port=port)
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
