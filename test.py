from app.main.videofeeder import VideoFeeder
import cv2 as cv


vf = VideoFeeder()
v2 = VideoFeeder()
while True:


    cv.imshow('test', vf.get_frame())


    if cv.waitKey(1) == 27:
        break

