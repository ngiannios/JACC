# Importing socket library 
import socket 
from utility.log import Log

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
  
