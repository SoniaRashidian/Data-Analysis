# Exploratory Data Analysis of Snapshot Karoo

## Overview

This project performs exploratory data analysis (EDA) on the **Snapshot Karoo** camera-trap image dataset. The objective is to understand the structure, distribution, and visual characteristics of biodiversity observations before applying automated image-classification methods.

The analysis focuses on three main dimensions:

* **Animal class**
* **Camera-trap location** 
* **Image characteristics** 

The Snapshot Karoo dataset is part of the **Lila BC project** and contains camera-trap images collected for biodiversity monitoring. The original project describes 14,889 image sequences containing 38,074 images. A reduced mini-dataset was used for the analysis.

The supplied mini-dataset contains **6,200 images**, organized into **36 animal classes** and collected from **15 camera locations**.

---

## Project Objectives

The analysis follows these steps:

1. Import Python packages.
2. Inspect the dataset structure.
3. Load and construct image metadata.
4. Identify animal classes and camera locations.
5. Analyze the number of images per camera location.
6. Analyze the number of images per animal class.
7. Visualize the distribution of images across animal classes.
8. Visualize animal-class distributions across camera locations.
9. Inspect images from a selected camera location.
10. Inspect images from different camera locations.
11. Examine images that may present challenges for classification.

This follows the exploratory workflow used in the original project.

---

# Methodology

## 1. Metadata extraction

Instead of loading all images into memory simultaneously, the analysis first creates a metadata dataframe.

For each image, the following information is recorded:

| Variable   | Description                                      |
| ---------- | ------------------------------------------------ |
| `location` | Camera-trap location extracted from the filename |
| `class`    | Animal class obtained from the folder name       |
| `path`     | Path to the image file                           |

The resulting dataframe has the structure:

```text
location    class          path
B03         wildebeestblue data/wildebeestblue/...
B02         kudu           data/kudu/...
E01         eland          data/eland/...
```

The original analysis produced a dataframe with:

```text
6,200 rows × 3 columns
```

representing the images in the mini-dataset.

---

## 2. Identification of animal classes and camera locations

The unique animal classes are extracted from the metadata:

```python
class_names = sorted(meta_data["class"].unique())
```

Camera locations are extracted using:

```python
locations = sorted(meta_data["location"].unique())
```

The supplied analysis identified:

* **36 animal classes**
* **15 camera locations**

The classes include species/categories such as:

```text
baboon
birdother
birdsofprey
bustardkori
caracal
eland
gemsbokoryx
hare
kudu
lionmale
ostrich
rhinocerosblack
springbok
steenbok
wildebeestblue
zebraburchells
zebramountain
...
```

---

## 3. Image distribution by camera location

The number of images recorded at each camera location is calculated using:

```python
meta_data["location"].value_counts()
```

The supplied analysis found substantial differences in the number of images collected from different locations.

For example:

| Camera location | Images |
| --------------- | -----: |
| B03             |  1,445 |
| B02             |  1,186 |
| E01             |    505 |
| D04             |    440 |
| A02             |    434 |
| E03             |    417 |
| D01             |    366 |
| E02             |    291 |
| D03             |    263 |
| C02             |    258 |
| A01             |    235 |
| B01             |    158 |
| C03             |    117 |
| F02             |     47 |
| C04             |     38 |

Total:

```text
6,200 images
```

This indicates that the dataset is not evenly distributed across camera locations.

---

## 4. Image distribution by animal class

The number of images belonging to each animal class is calculated using:

```python
meta_data["class"].value_counts()
```

The supplied analysis identified substantial class imbalance.

The most frequent classes included:

| Animal class      | Images |
| ----------------- | -----: |
| gemsbokoryx       |  1,689 |
| hartebeestred     |    999 |
| kudu              |    849 |
| eland             |    726 |
| baboon            |    515 |
| springbok         |    332 |
| jackalblackbacked |    209 |
| zebramountain     |    202 |
| steenbok          |    133 |
| birdother         |    118 |

Some classes had only one or a few images.

For example:

```text
foxcape                  1
rabbitriverine           1
klipspringer             1
hyenabrown               1
meerkatsuricate          3
birdsofprey              3
mongooseyellow           3
```

The complete class-frequency analysis is contained in the original exploratory work.

---

# Exploratory Visualizations

## 5. Overall class distribution

A donut chart is used to visualize the distribution of images across animal classes.

```python
class_counts = meta_data["class"].value_counts()

plot_donut_chart(class_counts)
```

The purpose of this visualization is to make the class imbalance easier to identify.

A highly imbalanced dataset is important to recognize before developing an image-classification model because some animal classes contain substantially more observations than others.

---

## 6. Animal distribution by camera location

A stacked bar chart is used to visualize the distribution of animal classes at each camera location.

Conceptually:

```text
Camera location
       ↓
Animal-class composition
       ↓
Comparison across locations
```

This allows the analysis to examine whether different camera locations contain different distributions of animals.

The original project specifically used a bar chart to visualize the changing animal distribution across camera locations.

---

# Image-Level Exploration

## 7. Images from a single camera location

A random sample of images can be displayed from one camera location.

For example:

```python
plot_random_images(
    meta_data,
    camera_location="B02"
)
```

This makes it possible to visually inspect the type of scenes captured by a particular camera.

The original project used `B02` as an example camera location.

---

## 8. Images from different camera locations

The project also selects images from different camera locations.

```python
plot_images_from_all_locations(meta_data)
```

This provides a visual comparison of the environments and observations associated with different camera locations.

---

# Difficult-to-Classify Images

An important part of the analysis is inspecting images that may be challenging for automated classification.

The original project explains that images were presented to volunteers in sequences of three images corresponding to a single capture. These images were expected to have the same label.

However, an individual image may not clearly show the animal.

For example, an animal may be:

* outside the camera's field of view,
* partially hidden,
* obscured by vegetation,
* difficult to identify from the individual frame.

Therefore, the assigned class label does not necessarily mean that the animal is clearly visible in every image.

This is an important consideration when preparing the data for machine learning.

---

# Key Findings

The exploratory analysis identified several important characteristics of the dataset.

### 1. Dataset size

The analyzed mini-dataset contains:

```text
6,200 images
```

### 2. Multiple animal classes

The dataset contains:

```text
36 animal classes
```

### 3. Multiple camera locations

The images originate from:

```text
15 camera-trap locations
```

### 4. Class imbalance

The number of images varies considerably between animal classes.

For example:

```text
gemsbokoryx       1,689
hartebeestred       999
kudu                849
eland               726
...
hyenabrown            1
klipspringer          1
```

### 5. Location imbalance

The number of observations also differs substantially between camera locations.

For example:

```text
B03    1,445
B02    1,186
...
C04       38
F02       47
```

### 6. Image-quality/classification challenges

Some images contain animals that are partially visible or difficult to identify.

These characteristics should be considered before developing a classification model.

---

## Project Type

**Data Analysis / Exploratory Data Analysis / Computer Vision Data Exploration**

**Primary skills demonstrated:**

* Data preprocessing
* Metadata extraction
* Pandas
* Exploratory data analysis
* Data visualization
* Class-imbalance analysis
* Image-data exploration
* Feature/metadata engineering
* Python programming
* Critical assessment of machine-learning data quality

**[Project Source]:**:https://www.coursera.org/specializations/ai-for-good
