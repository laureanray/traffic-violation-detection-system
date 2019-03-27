# import cv2 as cv
# import numpy as np
# from app.cardetector import CarDetector
#
# video = cv.VideoCapture('app/footage.mp4')
# face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
# car_cascade = cv.CascadeClassifier('cars.xml')
#
# while True:
#     ret, img = video.read()
#     if (type(img) == type(None)):
#         break
#
#     img = cv.resize(img, (512,288))
#
#     gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#
#     cars = car_cascade.detectMultiScale(gray, 1.1, 1)
#
#     for (x, y, w, h) in cars:
#         cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
#     cv.imshow('video', img)
#
#     if cv.waitKey(33) == 27:
#         break
#
# cv.destroyAllWindows()
# video.release()

from PyQt5.QtWidgets import  QApplication, QMainWindow

app = QApplication([])
win = QMainWindow()
win.show()

app.exit(app.exec_())