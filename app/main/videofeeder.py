import cv2 as cv


class VideoFeeder:
    video = cv.VideoCapture(0)
    frame = None

    def __del__(self):
        self.video.release()

    @staticmethod
    def get_frame():
        success, image = VideoFeeder.video.read()
        VideoFeeder.frame = image
        return VideoFeeder.frame




 