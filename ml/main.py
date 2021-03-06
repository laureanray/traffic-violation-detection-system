# Imports 
import os

from keras import backend as K

import tensorflow as tf
from tensorflow import keras
print("TensorFlow version is ", tf.__version__)

import numpy as np
# This will be used fror plotting the resutl of training
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tensorflow.python.tools import freeze_graph


zip_file = tf.keras.utils.get_file(origin="https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip",
                                   fname="cats_and_dogs_filtered.zip", extract=True)
base_dir, _ = os.path.splitext(zip_file)

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')


# Save checkpoints during training 
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback 
tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True,
                                    verbose=1)



# Directory with our training cat pictures
train_cats_dir = os.path.join(train_dir, 'cats')
print ('Total training cat images:', len(os.listdir(train_cats_dir)))

# Directory with our training dog pictures
train_dogs_dir = os.path.join(train_dir, 'dogs')
print ('Total training dog images:', len(os.listdir(train_dogs_dir)))

# Directory with our validation cat pictures
validation_cats_dir = os.path.join(validation_dir, 'cats')
print ('Total validation cat images:', len(os.listdir(validation_cats_dir)))

# Directory with our validation dog pictures
validation_dogs_dir = os.path.join(validation_dir, 'dogs')
print ('Total validation dog images:', len(os.listdir(validation_dogs_dir)))

image_size = 160 # All images will be resized to 160x160
batch_size = 32

# Rescale all images by 1./255 and apply image augmentation
train_datagen = keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255)

validation_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
                train_dir,  # Source directory for the training images
                target_size=(image_size, image_size),
                batch_size=batch_size,
                # Since we use binary_crossentropy loss, we need binary labels
                class_mode='binary')

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = validation_datagen.flow_from_directory(
                validation_dir, # Source directory for the validation images
                target_size=(image_size, image_size),
                batch_size=batch_size,
                class_mode='binary')

IMG_SHAPE = (image_size, image_size, 3)


with tf.Graph().as_default():
    with tf.Session() as sess:
        K.set_session(sess)
                

        # Create the base model from the pre-trained model MobileNet V2
        base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                    include_top=False,
                                                    weights='imagenet')

        base_model.trainable = False

        base_model.summary()

        model = tf.keras.Sequential([
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

        model.summary()

        len(model.trainable_variables)


        epochs = 10
        
        steps_per_epoch = train_generator.n // batch_size
        validation_steps = validation_generator.n // batch_size

        history = model.fit_generator(train_generator,
                                    steps_per_epoch = steps_per_epoch,
                                    epochs=epochs,
                                    workers=4,
                                    validation_data=validation_generator,
                                    validation_steps=validation_steps)

        saver = tf.train.Saver()
        saver.save(sess, './model.ckpt')
        tf.train.write_graph(sess.graph.as_graph_def(), '.', 'model.pbtxt', as_text=True)





