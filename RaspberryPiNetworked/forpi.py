import socket, hashlib, datetime
from RPi import GPIO

uberSecretPassword = '>8Y\JNtK:,\</(#2sP"/UU)R3NRrKp~+j@Z.DVfF'
magicalNumber = 421948395773
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

def check_secure(s):
    date = datetime.datetime.now()
    try:
        command = s.split(":|:")[0]
        sentHash = s.split(":|:")[1]

        myHash = hashlib.sha256((str(date.year + date.month + date.day + date.hour + date.minute + magicalNumber) + uberSecretPassword).encode()).hexdigest()

        if sentHash == myHash:
            print("COMMAND:%s" % command)
            return command
        else:
            print('Unauthenticated user trying to send commands!')
    except:
        print("Who sent me a bad packet!")


class ConnectionHandler:
    @staticmethod
    def takeInData():
        data, addr = recieve_socket.recvfrom(1024)

        return check_secure(data.decode())

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
    try:
        MotorHandler()
    except:
        GPIO.cleanup()
