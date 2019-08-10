from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.datasets import mnist
from keras.utils import to_categorical
import cv2 as cv
import numpy
import os
import numpy as np
import tensorflow as tf
import glob


filelist = glob.glob('dataset/*.jpg')
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = tf.keras.models.model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data

loaded_model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

image = cv.imread('cat.2000.jpg')
image2 = cv.imread('dog.2249.jpg')

image_resized = cv.resize(image, (160, 160), cv.INTER_AREA)
image_resized2 = cv.resize(image2, (160 ,160), cv.INTER_AREA)

x = np.array([cv.imread(fname) for fname in filelist])

for item in x:
    resized = cv.resize(item, (160, 160), cv.INTER_AREA)
    arr = np.array([resized])
    pred = loaded_model.predict(arr)
    cv.imshow('iamge', resized)
    print(pred)
    if(pred[0] < 0.5):
        print("DOG")
    else:
        print("CAT")
    cv.waitKey(0)
    cv.destroyAllWindows()



# print(pred)

