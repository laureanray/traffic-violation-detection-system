import cv2 as cv
from flask_socketio import emit, join_room, leave_room
from app.main.utilities import emit_log


class CarDetector:
    car_cascade = cv.CascadeClassifier('/media/laureanray/ACADS/Software Dev/Python/traffic-violation-detection-system/app/main/cars.xml')

    frame = None
    def __init__(self):
        print("Contructor Called")
        self.face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

    def __del__(self):
        print("Car detector deleted")

    def getCar(self, frame):
        newframe = cv.resize(frame, (512,288))
        gray = cv.cvtColor(newframe, cv.COLOR_BGR2GRAY)

        cars = CarDetector.car_cascade.detectMultiScale(gray, 1.1, 1)

        for (x, y, w, h) in cars:
            cv.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # print('may car')

        return gray