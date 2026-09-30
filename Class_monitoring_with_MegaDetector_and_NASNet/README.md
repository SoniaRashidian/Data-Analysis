# Project Overview

This project develops a computer-vision pipeline for automated biodiversity monitoring using camera-trap images from the **Snapshot Karoo** dataset.

The project combines:

1. **Exploratory image analysis**
2. **MegaDetector object detection**
3. **Region-of-interest extraction**
4. **Image preprocessing and resizing**
5. **Data augmentation**
6. **Class balancing**
7. **Transfer learning with NASNet-Mobile**
8. **Model fine-tuning**
9. **Confusion-matrix evaluation**
10. **Visual inspection of model predictions**

The overall objective is to transform raw camera-trap photographs into a machine-learning-ready dataset and develop an animal-classification model.

---

# Project Pipeline

The complete workflow is:

```text
Raw camera-trap images
        │
        ▼
   Dataset exploration
        │
        ▼
    MegaDetector
        │
        ▼
Animal detection + bounding boxes
        │
        ▼
     ROI cropping
        │
        ▼
Square and resize images
        │
        ▼
Data augmentation
        │
        ▼
Class balancing
        │
        ▼
NASNet-Mobile
   Transfer Learning
        │
        ▼
     Fine-tuning
        │
        ▼
 Model predictions
        │
        ├───────────────┐
        ▼               ▼
 Confusion Matrix   Visual Inspection
```

---

# Part 1 — MegaDetector Object Detection

## Objective

The first stage uses **MegaDetector** to automatically identify where animals occur in the camera-trap images.

MegaDetector is an object-detection model that identifies:

* animals
* people
* vehicles

and returns bounding-box coordinates around detected objects.

The purpose in this project is specifically to identify animals and isolate their regions of interest before classification.

---

## 1. Loading MegaDetector

The pretrained MegaDetector model is loaded using its PyTorch detector:

```python
from detection.pytorch_detector import PTDetector

model_file = "md_v5a.0.0.pt"

megadetector = PTDetector(model_file)
```

The original implementation used MegaDetector version `md_v5a.0.0.pt`.

---

## 2. Running Detection on an Image

An individual image can be loaded and passed through MegaDetector:

```python
sample_image = viz_utils.load_image(
    sample_im_file
)

megadetector_result = (
    megadetector.generate_detections_one_image(
        sample_image,
        sample_im_file,
        detection_threshold=0.6
    )
)
```

The detector returns information including:

* image path
* maximum detection confidence
* detected object categories
* confidence scores
* normalized bounding-box coordinates

Example output:

```python
{
    "file": ".../KAR_S1_E03_R1_IMAG0052.JPG",
    "max_detection_conf": 0.856,
    "detections": [
        {
            "category": "1",
            "conf": 0.856,
            "bbox": [
                0.07499,
                0,
                0.6156,
                0.9696
            ]
        }
    ]
}
```

The original analysis also tested images containing multiple animals.

---

## 3. Detection Threshold

The detection threshold used in the project was:

```python
detection_threshold = 0.6
```

Only detections meeting this confidence threshold are considered during the subsequent processing pipeline.

---

# 4. Bounding-Box Visualization

The detected regions can be visualized on the original image:

```python
utils2.draw_bounding_box(
    sample_image,
    megadetector_result
)
```

This provides a visual check of whether the detector correctly identifies the animal region.

---

# 5. Cropping the Region of Interest

The bounding boxes produced by MegaDetector are used to extract animal regions.

The original workflow is:

```text
MegaDetector detection
        ↓
Bounding box
        ↓
Square bounding region
        ↓
Crop image
        ↓
Resize
        ↓
Save cropped image
```

The source project explicitly describes this as detecting the region of interest, squaring the region, cropping it, resizing it to **244 × 244 pixels**, and saving the result.

Example:

```python
res = megadetector.generate_detections_one_image(
    random_image,
    random_im_file,
    detection_threshold=0.6
)

animals = utils2.crop_image(
    random_image,
    res,
    "./data",
    "/tmp"
)
```

The resulting detections and crops can then be visualized:

```python
utils2.plot_detections(
    random_image,
    animals,
    res
)
```

---

# 6. Processing the Full Dataset

The complete image collection can be processed using:

```python
root_dir = "./data"

utils2.preprocess_dataset(
    root_dir,
    megadetector,
    utils2.crop_image,
    0.6,
    0
)
```

This applies the detection-and-cropping pipeline to the dataset and generates the cropped image dataset for the classification stage.

---

# Part 2 — NASNet Animal Classification

## Objective

After extracting animal regions from the original camera-trap photographs, the second stage develops an animal-classification model.

The project uses **NASNet-Mobile**, a convolutional neural network originally pretrained on ImageNet.

NASNet-Mobile accepts images of:

```text
224 × 224 × 3
```

and was originally trained to classify ImageNet categories.

The project adapts this pretrained network to the Snapshot Karoo animal classes using **transfer learning**.

---

# 1. Reproducibility

A fixed random seed is used:

```python
RANDOM_SEED = 42

tf.keras.utils.set_random_seed(
    RANDOM_SEED
)
```

This improves reproducibility of the data-processing and model-training workflow.

---

# 2. Loading the Original NASNet Model

The original ImageNet-trained NASNet-Mobile model can first be loaded:

```python
original_nasnet_model = (
    nasnet.NASNetMobile(
        include_top=True
    )
)
```

The purpose of this stage is to investigate how a model trained on ImageNet performs on the biodiversity dataset before adapting it to the specific animal classes.

---

# 3. Image Preprocessing

The classification pipeline uses:

```python
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
```

The cropped images are loaded as TensorFlow datasets:

```python
train_ds_full, _, _ = utils2.load_data(
    IMAGE_DIR,
    BATCH_SIZE,
    IMAGE_SIZE,
    RANDOM_SEED
)
```

The original dataset was divided into training, validation, and test subsets.

---

# 4. Data Augmentation

Because camera-trap images can vary substantially in viewpoint, position, lighting, and scale, several augmentation techniques were investigated.

The project explored:

### Horizontal/vertical flipping

```python
utils2.data_aug_flip(image)
```

### Zooming

```python
utils2.data_aug_zoom(image)
```

### Rotation

```python
utils2.data_aug_rot(image)
```

### Contrast modification

```python
utils2.data_aug_contrast(image)
```

### Random combination of augmentations

```python
utils2.data_aug_random(image)
```

These transformations increase variation in the training data and can help reduce overfitting.

---

# 5. Class Imbalance

The initial exploratory analysis showed substantial imbalance between animal classes.

Therefore, the classification dataset was balanced using a combination of:

* **oversampling** minority classes
* **undersampling** majority classes

The project retained 11 classes with sufficient numbers of observations.

The selected classes were:

```text
baboon
bustardkori
duiker
eland
gemsbokoryx
hartebeestred
jackalblackbacked
kudu
springbok
steenbok
zebramountain
```

The balanced dataset contained:

```text
5,500 training images
477 validation images
1,194 test images
```

across 11 classes.

---

# 6. Transfer Learning

Instead of training a convolutional neural network from scratch, the project uses the pretrained NASNet-Mobile architecture as a feature extractor.

The base model is loaded without its original ImageNet classification layer:

```python
base_model = nasnet.NASNetMobile(
    include_top=False
)
```

The original NASNet core is then frozen:

```python
base_model.trainable = False
```

A new classification head is constructed for the 11 Karoo animal classes.

This is a **transfer-learning approach**: the pretrained network provides general visual features while the new classification layers learn the animal categories specific to the Karoo dataset.

---

# 7. Model Configuration

The adapted classifier uses:

```python
NUM_CLASSES = 11

model = utils2.get_transfer_model(
    model_to_transfer=base_model,
    num_classes=NUM_CLASSES,
    img_height=IMAGE_SIZE[0],
    img_width=IMAGE_SIZE[1]
)
```

The model was designed so that the pretrained NASNet core remains frozen while the newly added classification layers are trained.

---

# 8. Loading Fine-Tuned Weights

A model that had already been fine-tuned for 150 epochs was supplied in the original project:

```python
model_weight_path = (
    "models/"
    "model_cnn_finetuned_nasnet_150epocha_augmented.h5"
)

model.load_weights(
    model_weight_path
)
```

The project then allows additional fine-tuning.

---

# 9. Additional Fine-Tuning

Additional training can be performed using:

```python
epochs = 1

history_finetune = model.fit(
    train_ds,
    epochs=epochs
)
```

The supplied run produced:

```text
loss: 0.4765
accuracy: 0.8340
sparse_top_k_categorical_accuracy: 0.9907
```

for the additional training epoch.

Training history can then be visualized:

```python
utils2.plot_training_history(
    "history_training"
)
```

---

# 10. Model Evaluation

The final model is evaluated on the held-out test dataset.

Predictions are generated:

```python
y_pred = []
y_true = []

for data, label in test_ds:

    predictions = model.predict(data)

    y_pred.extend(
        tf.argmax(
            predictions,
            axis=1
        ).numpy()
    )

    y_true.extend(
        label.numpy()
    )
```

Overall accuracy is calculated as:

```python
accuracy = (
    np.sum(
        np.array(y_true) == y_pred
    )
    / len(y_pred)
)

print(
    "Overall model accuracy:",
    accuracy
)
```

The supplied experiment reported:

```text
Overall model accuracy:
0.8015075376884422
```

or approximately **80.15%** on the reported test set.

---

# 11. Confusion Matrix

A confusion matrix is used to investigate class-specific performance:

```python
utils2.plot_cm(
    y_true,
    y_pred,
    label2cat
)
```

The confusion matrix provides more information than overall accuracy because it shows which animal classes are confused with one another.

This is particularly important for biodiversity classification where visually similar species may be difficult to distinguish.

---

# 12. Visual Prediction Analysis

The model predictions are also inspected visually.

The project uses:

```python
utils2.pick_img_and_plot_predictions(
    test_imgs,
    model,
    label2cat,
    cat2label,
    IMAGE_SIZE
)
```

This allows individual test images to be examined together with the model's top predictions and confidence values.

---

# Results

The reported experiment produced the following main result:

| Metric                           |     Result |
| -------------------------------- | ---------: |
| Number of classification classes |         11 |
| Training images                  |      5,500 |
| Validation images                |        477 |
| Test images                      |      1,194 |
| Additional fine-tuning accuracy  |     83.40% |
| Reported test accuracy           | **80.15%** |
| Top-k training accuracy          |     99.07% |


# Key Technical Skills

### Python

* Python scripting
* File and directory management
* Random sampling
* Data processing
* Reproducible workflows

### Data Analysis

* Dataset exploration
* Class-frequency analysis
* Class-imbalance analysis
* Data resampling
* Training/validation/test splitting
* Visualization
* Confusion-matrix analysis

### Computer Vision

* Object detection
* Bounding-box processing
* Region-of-interest extraction
* Image cropping
* Image resizing
* Image augmentation
* Image classification

### Machine Learning

* Transfer learning
* Convolutional neural networks
* NASNet-Mobile
* Fine-tuning
* Model evaluation
* Prediction-confidence analysis

### Deep Learning Frameworks

* TensorFlow
* Keras
* PyTorch

---

# Reproducibility

The project uses a fixed random seed:

```python
RANDOM_SEED = 42
```

and separates the data into training, validation, and test sets.

For reproducibility, the repository should document:

* Python version
* TensorFlow version
* PyTorch version
* MegaDetector version
* NASNet architecture
* random seed
* image dimensions
* batch size
* detection threshold
* selected classes
* resampling strategy

---

# Important Note


The project does not claim to have developed MegaDetector or NASNet. Instead, it demonstrates the application of these models to a real-world biodiversity dataset.

---

**[project source]:** https://www.coursera.org/specializations/ai-for-good
