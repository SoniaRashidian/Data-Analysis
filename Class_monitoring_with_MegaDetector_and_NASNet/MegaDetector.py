import os
import sys
import glob

from random import choice

import matplotlib.pyplot as plt

# MegaDetector dependencies
os.environ["PYTHONPATH"] += ":./ai4eutils"
os.environ["PYTHONPATH"] += ":./CameraTraps"
os.environ["PYTHONPATH"] += ":./yolov5"

sys.path.insert(0, "./ai4eutils")
sys.path.insert(0, "./CameraTraps")
sys.path.insert(0, "./yolov5")

from detection.pytorch_detector import PTDetector
import visualization.visualization_utils as viz_utils

import utils2

# LOAD MEGADETECTOR

MODEL_FILE = "md_v5a.0.0.pt"

megadetector = PTDetector(
    MODEL_FILE
)

# 3. FIND IMAGES

examples = list(
    glob.iglob(
        "./data/**/*.JPG",
        recursive=True
    )
)

print(
    f"Number of images: {len(examples)}"
)

# 4. OBJECT DETECTION

random_im_file = choice(
    examples
)

random_image = viz_utils.load_image(
    random_im_file
)

result = megadetector.generate_detections_one_image(
    random_image,
    random_im_file,
    detection_threshold=0.6
)

print(result)

utils2.draw_bounding_box(
    random_image,
    result
)

# 5. PROCESS DATASET

ROOT_DIR = "./data"

utils2.preprocess_dataset(
    ROOT_DIR,
    megadetector,
    utils2.crop_image,
    0.6,
    0
)

print(
    "Dataset processed successfully."
)
