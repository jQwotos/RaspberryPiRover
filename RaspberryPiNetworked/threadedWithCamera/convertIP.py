import socket
def checkIP(ip):
    if ip == "auto":
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempSocket.connect(("gmail.com", 80))
        ip = tempSocket.getsockname()[0]
    return ip
