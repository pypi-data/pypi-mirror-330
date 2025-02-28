import socket

def get_ip():
    """Get the primary IP address of the machine"""
    try:
        # Create a temporary socket to determine the outgoing IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        # Fallback to hostname lookup
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"