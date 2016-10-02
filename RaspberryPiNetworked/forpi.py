import socket, hashlib
from RPi import GPIO

uberSecretPassword = '>8Y\JNtK:,\</(#2sP"/UU)R3NRrKp~+j@Z.DVfF'
# [left, right]
motorsPins = [1, 2]
computerIP = ''
port = 9986

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind(computerIP, port)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorsPins, GPIO.OUT)

class ConnectionHandler:
    @staticmethod
    def takeInData():
        data, addr = recieve_socket.recvfrom(1024)
        return data.decode()

    @staticmethod
    def sendData(s):
        # send info data
        pass

class MotorHandler:
    def __init__(self):
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

        GPIO.cleanup()

    def allStop(self):
        GPIO.write(motorsPins, GPIO.LOW)

if __name__ == "__main__":
    MotorHandler()
