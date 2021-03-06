import socket, pygame, hashlib, datetime, secrets

piIP = '192.168.1.101'
localIP = '127.0.0.1'
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9986

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind((localIP, port))

def make_secure(s):
    date = datetime.datetime.now()
    return s + ":|:" + hashlib.sha256((str(date.year + date.month + date.day + date.hour + date.minute + secrets.magicalNumber) + secrets.uberSecretPassword).encode()).hexdigest()

class ConnectionHandler:
    @staticmethod
    def takeInData(piIP):
        data, addr = recieve_socket.recvfrom(1024)
        if piIP == addr:
            # do something with data
            pass

    @staticmethod
    def sendData(s):
        send_socket.sendto(make_secure(s).encode(),(piIP, port))

class PyGameWindow:
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

    def MainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    self.KeyStrokeHandler(event.key)


if __name__ == "__main__":
    MainWindow = PyGameWindow()
    MainWindow.MainLoop()
