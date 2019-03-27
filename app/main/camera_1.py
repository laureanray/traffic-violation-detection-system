import cv2
import cv2 as cv
from app.main.base_camera import BaseCamera
from app.main.cardetector import CarDetector
from app import socketio
from app.main.utilities import emit_log
fgbg = cv.createBackgroundSubtractorMOG2()
cardetetor = CarDetector()

isOriginal = False
isBdm = False

@socketio.on('button')
def onButton(data):
    global isOriginal
    global isBdm
    print('*' + data['toggle'] + '*') 
    if data['toggle'] == 'original':
        isOriginal = not isOriginal
        if isOriginal == True:
            emit_log('Original Frame')
        else:
            emit_log('Default Frame')

    elif data['toggle'] == 'bdm':
        isBdm = not isBdm
        if isBdm == True:
            emit_log('Background Difference Mask')
        else:
            emit_log('Default Frame')

class Camera(BaseCamera):
    video_source = '/media/laureanray/ACADS/Software Dev/Python/traffic-violation-detection-system/app/main/footage.mp4'
    frame_counter = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            car = cardetetor.getCar(img)
            Camera.frame_counter += 1
            fgmask = fgbg.apply(img)

            toReturn = None
            if Camera.frame_counter == camera.get(cv2.CAP_PROP_FRAME_COUNT):
                frame_counter = 0
                camera = cv2.VideoCapture(Camera.video_source)
            
            if isOriginal == True:
                toReturn = img
            elif isBdm == True:
                toReturn = fgmask
            else:
                toReturn = car

            yield cv2.imencode('.jpg', toReturn)[1].tobytes()
