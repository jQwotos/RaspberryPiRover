import socket, security, cv2
from RPi import GPIO

# [left, right]
motorsPins = [3, 5]
localIP = 'auto'
port = 9986

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind((localIP, port))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorsPins, GPIO.OUT)

def setIP:
    if localIP == "auto":
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempSocket.connect(("gmail.com", 80))
        localIP = tempSocket.getsockname()[0]

class ConnectionHandler:
    @staticmethod
    def takeInData():
        data, addr = recieve_socket.recvfrom(1024)
        return security.check_secure(data.decode())

    @staticmethod
    def sendData(s):
        # send info data
        pass

class MotorHandler:
    @staticmethod
    def start():
        while True:
            data = ConnectionHandler.takeInData()
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

    def start():
        while True:
            ConnectionHandler.sendData(data)

def main():
    try:
        MotorHandler.start()
        setIP()
    except KeyboardInterrupt:

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
