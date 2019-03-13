from utility.log import Log
from utility.misc import Misc
from wallet import Wallet
from blockchain import Blockchain
import requests

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    parser.add_argument('-n', '--nodeUrl', type=str, default='')
    parser.add_argument('-np', '--nodePort', type=str, default='')
    
    args = parser.parse_args()
    port = args.port
    IP_Address = Misc.get_IP(port)
    
    if args.nodeUrl is not '':    
        node_Url = args.nodeUrl
        Log.log_message('A new node URL"{}" will be added at port:{}'.format(node_Url, port), port)
    elif args.nodePort is not '':
        print('step 1')
        node_Url = 'http://{}:{}'.format(IP_Address, args.nodePort)
        print(node_Url)
    else:
        print('No parameters were passed!')
        exit()


    url = 'http://{}:{}/node'.format(IP_Address, port)
    print('url:{}'.format(url))
    try:
        response = requests.post(url, json={'node':node_Url})
        print(response)
        if response.status_code == 400 or response.status_code == 500:
            print(response)
        if response.status_code == 409:
            print(response)
    except requests.exceptions.ConnectionError:
        print(response)
    

