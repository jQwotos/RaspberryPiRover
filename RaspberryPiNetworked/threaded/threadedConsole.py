import socket, pygame, security, threading

piIP = '192.168.1.101'
localIP = '192.168.0.111'
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9986

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind((localIP, port))

class Reciever(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pass

    def run(self):
        while True:
            data, addr = recieve_socket.recvfrom(1024)
            data = security.check_secure(data.decode())
            if data:
                print(data)


class ConnectionHandler:
    @staticmethod
    def takeInData():
        print("poop")
        data, addr = yield from recieve_socket.recvfrom(1024)
        print("Here I am!")
        print(data)
        return data

    @staticmethod
    def sendData(s):
        send_socket.sendto(security.make_secure(s).encode(),(piIP, port))

class PyGameWindow():
    def __init__(self):
        pygame.init()
        self.width = 100
        self.height = 100

        self.screen = pygame.display.set_mode((self.width, self.height))

    def send(self, s):
        ConnectionHandler.sendData(s)
        print('sending:%s' % s)

    def KeyStrokeHandler(self, key):
        if key == pygame.K_RIGHT:
            self.send("turn right")
        elif key == pygame.K_LEFT:
            self.send("turn left")
        elif key == pygame.K_UP:
            self.send("move forward")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    self.KeyStrokeHandler(event.key)

if __name__ == "__main__":
    pyGame = PyGameWindow()
    recieverThread = Reciever()

    try:
        recieverThread.start()
        pyGame.run()
        print("r started")
    except KeyboardInterrupt:
        print("interupted by keyboard")
        recieverThread.stop()
