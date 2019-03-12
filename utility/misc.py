# Importing socket library 
import socket 
from utility.log import Log
import requests

class Misc:  
    # Function to display hostname and 
    # IP address 
    @staticmethod
    def get_IP(port): 
        try: 
            host_name = socket.gethostname() 
            host_ip = socket.gethostbyname(host_name) 
            return(host_ip)
            
        except: 
            Log.log_error('IPE',"Unable to get Hostname and IP", port) 
  
    @staticmethod
    def get_Public_IP(port): 
        return requests.get('http://ip.42.pl/raw').text
