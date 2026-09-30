import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf

from tensorflow.keras.metrics import (
    sparse_top_k_categorical_accuracy
)

from tensorflow.keras.applications import nasnet

import utils2

RANDOM_SEED = 42

tf.keras.utils.set_random_seed(
    RANDOM_SEED
)

IMAGE_DIR = "data_crops"

BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)

OUTPUT_DIR = "data_final"

train_ds_full, _, _ = utils2.load_data(
    IMAGE_DIR,
    BATCH_SIZE,
    IMAGE_SIZE,
    RANDOM_SEED
)

# Example image
images, labels = next(
    iter(train_ds_full)
)

selected_image = 3

image = (
    images[selected_image]
    .numpy()
    .astype("uint8")
)

label = label2cat_full[
    labels[selected_image].numpy()
]

utils2.plot_single_image(
    image,
    label
)

# Flip
utils2.data_aug_flip(image)

# Zoom
utils2.data_aug_zoom(image)

# Rotation
utils2.data_aug_rot(image)

# Contrast
utils2.data_aug_contrast(image)

# Random combination
utils2.data_aug_random(image)

utils2.resample_data(
    "data_crops",
    OUTPUT_DIR,
    train_ds_full,
    11,
    500
)

utils2.resample_data(
    "data_crops",
    OUTPUT_DIR,
    train_ds_full,
    11,
    500
)

train_ds, val_ds, test_ds = (
    utils2.load_data(
        OUTPUT_DIR,
        BATCH_SIZE,
        IMAGE_SIZE,
        RANDOM_SEED
    )
)

label2cat = {
    0: "baboon",
    1: "bustardkori",
    2: "duiker",
    3: "eland",
    4: "gemsbokoryx",
    5: "hartebeestred",
    6: "jackalblackbacked",
    7: "kudu",
    8: "springbok",
    9: "steenbok",
    10: "zebramountain"
}

cat2label = {
    v: k
    for k, v in label2cat.items()
}

#Load the fine-tuned model
MODEL_WEIGHT_PATH = (
    "models/"
    "model_cnn_finetuned_nasnet_150epocha_augmented.h5"
)

model.load_weights(
    MODEL_WEIGHT_PATH
)

EPOCHS = 1

history = model.fit(
    train_ds,
    epochs=EPOCHS
)

EPOCHS = 1

history = model.fit(
    train_ds,
    epochs=EPOCHS
)

#Evaluate on the test set
y_pred = []
y_true = []

for data, label in test_ds:

    predictions = model.predict(
        data,
        verbose=0
    )

    predicted_classes = tf.argmax(
        predictions,
        axis=1
    ).numpy()

    y_pred.extend(
        predicted_classes
    )

    y_true.extend(
        label.numpy()
    )

#calculate the accuracy
y_true = np.array(y_true)
y_pred = np.array(y_pred)

accuracy = np.mean(
    y_true == y_pred
)

print(
    f"Test accuracy: {accuracy:.4f}"
)

#confusion matrix
utils2.plot_cm(
    y_true,
    y_pred,
    label2cat
)

utils2.pick_img_and_plot_predictions(
    test_imgs,
    model,
    label2cat,
    cat2label,
    IMAGE_SIZE
)
