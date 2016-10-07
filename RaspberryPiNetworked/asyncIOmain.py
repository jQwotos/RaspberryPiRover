import socket, pygame, secrets, asyncio, security

piIP = '192.168.1.101'
localIP = '192.168.0.111'
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9986

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind((localIP, port))

def waitForData():
    data = asyncio.async(ConnectionHandler.takeInData())
    return data
'''
class Receiver:
    @staticmethod
    @asyncio.coroutine
    def start():
        print("y you no start!")
        while True:
            print("Waiting for data!")
            data = yield from ConnectionHandler.takeInData()
            print(data)
'''
class ConnectionHandler:
    @asyncio.coroutine
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

    @asyncio.coroutine
    def MainLoop(self):
        print("potatoes")
        while True:
            data = waitForData()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    self.KeyStrokeHandler(event.key)

def main():
    MainWindow = PyGameWindow()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(MainWindow.MainLoop())
    except KeyboardInterrupt:
        loop.close()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
