import socket, asyncio, security
from RPi import GPIO

# [left, right]
motorsPins = [3, 5]
computerIP = ''
localIP = '127.0.0.1'
port = 9986

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind((localIP, port))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorsPins, GPIO.OUT)

class ConnectionHandler:
    @asyncio.coroutine
    @staticmethod
    def takeInData():
        data, addr = yield from recieve_socket.recvfrom(1024)
        return security.check_secure(data.decode())

    @staticmethod
    def sendData(s):
        # send info data
        pass

class MotorHandler:
    def __init__(self):
        pass

    @asyncio.coroutine
    def start():
        while True:
            data = yield from ConnectionHandler.takeInData()
            if data:
                if data == "turn right":
                    GPIO.write(motorsPins[1], GPIO.LOW)
                    GPIO.write(motorsPins[0], GPIO.HIGH)
                elif data == "turn left":
                    GPIO.write(motorsPins[0], GPIO.LOW)
                    GPIO.write(motorsPins[1], GPIO.HIGH)
                elif data == "move forward":
                    GPIO.write(motorsPins, GPIO.HIGH)
                else:
                    self.allStop()
                if data == "KILL":
                    self.allStop()
                    break

    def allStop(self):
        GPIO.write(motorsPins, GPIO.LOW)

class DataSender:
    def __init__(self):
        pass

    @asyncio.coroutine
    def start():
        while True:
            ConnectionHandler.sendData(data)



def main():
    loop = asyncio.get_event_loop()
    motorHandler = MotorHandler()
    dataSender = DataSender()
    try:
        loop.run_until_complete(motorHandler.start())
        loop.async()
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop
    finally:
        loop.close()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
