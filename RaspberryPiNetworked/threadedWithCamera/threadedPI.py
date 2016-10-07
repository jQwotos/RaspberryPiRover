import socket, asyncio, security, cv2, numpy, convertIP
from RPi import GPIO

# [left, right]
computerIP = '192.168.0.111'
motorsPins = [3, 5]
localIP = 'auto'
port = 9986

localIP = convertIP.checkIP(localIP)

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.bind((localIP, port))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorsPins, GPIO.OUT)

class ConnectionHandler:
    @staticmethod
    def takeInData():
        data, addr = recieve_socket.recvfrom(1024)
        return security.check_secure(data.decode())

    @staticmethod
    def sendData(s):
        send_socket.sendto(security.make_secure(s).encode(), (computerIP, port))

class OpenCV(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, img = self.cap.read()

            r = 100.0 / img.shape[1]
            dim = (100, int(img.shape[0] * r))

            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = gray.flatten().tostring()

            frame = gray.flatten().tostring()
            ConnectionHandler.sendData(frame)

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

def main():
    cvThread = OpenCV()
    try:
        MotorHandler.start()
        cvThread.start()
    except KeyboardInterrupt:
        cvThread.stop()
        cvThread.cap.release()
        cv2.destroyAllWindows()
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
