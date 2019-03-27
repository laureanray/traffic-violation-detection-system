import cv2
import cv2 as cv
from app.main.base_camera import BaseCamera
from app.main.cardetector import CarDetector
from app import socketio
from app.main.utilities import emit_log
import tensorflow as tf
import os
import numpy as np
import sys

# BEGIN


# Import utilites
from app.utils import label_map_util
from app.utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,'app','main',MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'app','main','data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 90

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')



# END

fgbg = cv.createBackgroundSubtractorMOG2()
cardetetor = CarDetector()

isOriginal = False
isBdm = False

videoSource = 0

@socketio.on('source')
def onChange(source):
    if source['source'] == 'webcam':
        videoSource = 0
    else:
        videoSource = source['source']


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
    frame_counter = 0
    # Initialize frame rate calculation

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(videoSource)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        
        freq = cv2.getTickFrequency()
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame_rate_calc = 1

        while True:
            toReturn = None

            t1 = cv2.getTickCount()

            # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
            # i.e. a single-column array, where each item in the column has the pixel RGB value
            ret, frame = camera.read()
            frame = cv2.resize(frame, (512, 288))
            frame_original = frame
            fgmask = fgbg.apply(frame)
            frame_expanded = np.expand_dims(frame, axis=0)



            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})

            # Draw the results of the detection (aka 'visulaize the results')
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.85)

            cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

            # All the results have been drawn on the frame, so it's time to display it.

            t2 = cv2.getTickCount()
            time1 = (t2-t1)/freq
            frame_rate_calc = 1/time1

            if isOriginal == True:
                toReturn = frame_original
            elif isBdm == True:
                toReturn = fgmask
            else:
                toReturn = frame

            yield cv2.imencode('.jpg', toReturn)[1].tobytes()
