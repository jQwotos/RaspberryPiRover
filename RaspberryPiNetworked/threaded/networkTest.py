import security, socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    s.sendto(security.make_secure(input(">")).encode(), ('192.168.0.111', 9986))
