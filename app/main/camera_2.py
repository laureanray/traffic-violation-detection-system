import cv2
from app.main.base_camera import BaseCamera


class Camera(BaseCamera):

    video_source = 0

    @staticmethod
    def set_source(source):
        Camera.video_source = source


    @staticmethod
    def frames():
        # cardetector = CarDetector()
        camera = Camera.video_source
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            # car = cardetector.getCar(img)


            yield cv2.imencode('.jpg', img)[1].tobytes()
