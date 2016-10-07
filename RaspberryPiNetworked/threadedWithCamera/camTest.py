import cv2, socket
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class OpenCV:
    @staticmethod
    def run():
        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()

            r = 100.0 / img.shape[1]
            dim = (100, int(img.shape[0] * r))

            img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = gray.flatten().tostring()
            print(len(gray))

            #img = img
            #img = img.flatten().tostring()
            #print(len(img))
            #s.sendto(img, ('192.168.0.111', 9986))
            cv2.imshow('img', img)


OpenCV.run()

cap.release()
cv2.destroyAllWindows()
