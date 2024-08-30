import socket
from common_ports import ports_and_services # <<< ADDED BY ME

def get_open_ports(target, port_range, verbose = False):

    # === CHECK IF target HAS ANY LETTERS ===
    if any((char.isalpha() for char in target)):
        # target IS A URL
        print("1) There are letters. target must be a URL.")
        url_address = target
        link = "hostname"
        try:
            print(f"2) Trying to connect to URL: {url_address}")
            ip_address = socket.gethostbyname(target)
        except:
            print("2) Couldn't .gethostbyname(). IP: ''")
            ip_address = ""
        
    else: #target IS AN IP
        print("1) There are no letters. target must be an IP.")
        ip_address = target
        link = "IP address"
        try:
            print(f"2) Trying to connect to IP: {ip_address}")
            url_address = socket.gethostbyaddr(target)[0] #.gethostbyaddr() RETURNS A TUPLE. THE FIRST ITEM IS THE DOMAIN.
        except:
            print(f"2) No hostname/url found for IP {ip_address}. hostname: ''")
            url_address = ""
    
    resp_string = f"Open ports for {url_address} ({ip_address})\nPORT     SERVICE"
    if not url_address: # PROVIDE DIFFERENT STRING IF THERE'S NO HOSTNAME
        resp_string = f"Open ports for {ip_address}\nPORT     SERVICE"
    open_ports = []
    
    # === SCAN PORT RANGE ====
    for port in range( port_range[0], port_range[1]+1 ):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(0.5)
        print(f"3) trying to reach port #{port}")
        # target CAN EITHER BE AN IP OR URL; BOTH WORK.
        try:
            if client_socket.connect_ex( (target, port) ) != 0:
                print(f"4) Port {port} is closed")
                print(f"5) Closing socket")
                client_socket.close()
            else:
                if not verbose:
                    open_ports.append(port)
                print(f"4) Port {port} is open and appended")
                if verbose:
                    resp_string += f"\n{port:<9}{ports_and_services[port]}"
                    print(f"4) Port {port} is open and string is modified")
                    # service = client_socket.getservbyport(port) #ALTERNATIVE
                client_socket.close()
                print(f"5) Socket for port #{port} closed")
        except: # IF CONNECTION UNSUCCESSFUL, target IS INVALID
            print(f"Error: Invalid {link}")
            client_socket.close()
            return f"Error: Invalid {link}"

    if verbose:
        print(resp_string)
        return resp_string
    
    elif not verbose:
        print(open_ports)
        return open_ports    
