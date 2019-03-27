from app.main.videofeeder import VideoFeeder
import cv2 as cv


v2 = VideoFeeder()

while True:


    cv.imshow('test2', v2.get_frame())

    if cv.waitKey(1) == 27:
        break

