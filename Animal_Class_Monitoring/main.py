"""
Biodiversity Monitoring: Exploration Phase

Exploratory data analysis of the Snapshot Karoo camera-trap dataset.

The analysis:
1. Builds image metadata from folder structure and filenames.
2. Summarizes images by camera-trap location and animal class.
3. Visualizes class imbalance and class distribution by location.
4. Samples images from individual/all camera locations.
5. Inspects example image sequences and difficult-to-classify images.
"""

from pathlib import Path
import re
import random

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
}


def get_metadata(image_dir="data"):
    """
    Scan class folders and create one metadata row per image.

    Returns
    -------
    pandas.DataFrame
        Columns:
        - location: camera-trap location code
        - class: animal class
        - path: image path
    """

    image_dir = Path(image_dir)
    records = []

    for class_dir in sorted(image_dir.iterdir()):

        if not class_dir.is_dir():
            continue

        animal_class = class_dir.name

        for image_path in class_dir.iterdir():

            if image_path.suffix not in IMAGE_EXTENSIONS:
                continue

            # Example:
            # KAR_S1_B03_R1_IMAG0786.JPG
            match = re.search(
                r"KAR_S1_([A-Z]\d+)_R\d+_IMAG\d+",
                image_path.name
            )

            if match:
                location = match.group(1)
            else:
                location = "UNKNOWN"

            records.append({
                "location": location,
                "class": animal_class,
                "path": str(image_path)
            })

    return pd.DataFrame(
        records,
        columns=["location", "class", "path"]
    )


def plot_donut_chart(
    class_counts,
    title="Distribution of Images by Animal Class"
):
    """Plot the distribution of animal classes as a donut chart."""

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.pie(
        class_counts.values,
        labels=class_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.45}
    )

    ax.set_title(title)

    plt.tight_layout()
    plt.show()


def plot_bar_chart(
    meta_data,
    title="Animal Distribution by Camera Location"
):
    """
    Plot animal-class composition for each camera location.
    """

    distribution = pd.crosstab(
        meta_data["location"],
        meta_data["class"]
    )

    distribution = distribution.sort_index()

    ax = distribution.plot(
        kind="bar",
        stacked=True,
        figsize=(15, 8),
        width=0.85
    )

    ax.set_xlabel("Camera location")
    ax.set_ylabel("Number of images")
    ax.set_title(title)

    ax.legend(
        title="Animal class",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    plt.tight_layout()
    plt.show()


def _display_images(
    paths,
    titles=None,
    ncols=3,
    figsize=(15, 10)
):
    """Display image files in a grid."""

    paths = list(paths)

    if not paths:
        print("No images found.")
        return

    ncols = min(ncols, len(paths))
    nrows = (len(paths) + ncols - 1) // ncols

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=figsize,
        squeeze=False
    )

    axes = axes.ravel()

    for i, path in enumerate(paths):

        ax = axes[i]

        try:

            image = Image.open(path)

            ax.imshow(image)
            ax.axis("off")

            if titles:
                ax.set_title(titles[i])

        except Exception as exc:

            ax.text(
                0.5,
                0.5,
                f"Could not load\n{path}\n{exc}",
                ha="center",
                va="center"
            )

            ax.axis("off")

    for ax in axes[len(paths):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


def plot_random_images(
    meta_data,
    camera_location,
    n=6,
    seed=None
):
    """Display random images from one camera location."""

    subset = meta_data[
        meta_data["location"] == camera_location
    ]

    if subset.empty:
        raise ValueError(
            f"No images found for camera location: "
            f"{camera_location}"
        )

    sample = subset.sample(
        n=min(n, len(subset)),
        random_state=seed
    )

    titles = [
        f"{row['class']} | {row['location']}"
        for _, row in sample.iterrows()
    ]

    _display_images(
        sample["path"],
        titles=titles,
        ncols=3
    )


def plot_images_from_all_locations(
    meta_data,
    seed=None
):
    """Display one randomly selected image from each location."""

    rng = random.Random(seed)

    samples = []

    for location in sorted(
        meta_data["location"].unique()
    ):

        subset = meta_data[
            meta_data["location"] == location
        ]

        row = subset.iloc[
            rng.randrange(len(subset))
        ]

        samples.append(row)

    paths = [
        row["path"]
        for row in samples
    ]

    titles = [
        f"{row['location']} | {row['class']}"
        for row in samples
    ]

    _display_images(
        paths,
        titles=titles,
        ncols=4,
        figsize=(16, 12)
    )


def plot_examples(
    examples,
    titles=None
):
    """Display manually selected example images."""

    _display_images(
        examples,
        titles=titles,
        ncols=3,
        figsize=(15, 10)
    )


def summarize_by_location(meta_data):
    """Return image counts by camera location."""

    return (
        meta_data["location"]
        .value_counts()
        .rename_axis("location")
        .reset_index(
            name="number_of_images"
        )
    )


def summarize_by_class(meta_data):
    """Return image counts by animal class."""

    return (
        meta_data["class"]
        .value_counts()
        .rename_axis("animal")
        .reset_index(
            name="number_of_images"
        )
    )


def main():

    # ---------------------------------------------------------
    # 1. Load metadata
    # ---------------------------------------------------------

    IMAGE_DIR = "data/"

    meta_data = get_metadata(IMAGE_DIR)

    print(
        f"Shape of dataframe: "
        f"{meta_data.shape}"
    )

    print("\nFirst five rows:")
    print(meta_data.head())

    # ---------------------------------------------------------
    # 2. Unique classes and locations
    # ---------------------------------------------------------

    class_names = sorted(
        meta_data["class"].unique()
    )

    locations = sorted(
        meta_data["location"].unique()
    )

    print("\nClass names:")
    print(class_names)

    print("\nCamera locations:")
    print(locations)

    # ---------------------------------------------------------
    # 3. Images by location
    # ---------------------------------------------------------

    location_count = summarize_by_location(
        meta_data
    )

    print(
        "\nImages by camera location:"
    )

    print(location_count)

    # ---------------------------------------------------------
    # 4. Images by animal class
    # ---------------------------------------------------------

    animal_count = summarize_by_class(
        meta_data
    )

    print(
        "\nImages by animal class:"
    )

    print(animal_count)

    # ---------------------------------------------------------
    # 5. Visual exploration
    # ---------------------------------------------------------

    class_counts = (
        meta_data["class"]
        .value_counts()
    )

    plot_donut_chart(
        class_counts
    )

    plot_bar_chart(
        meta_data
    )

    # Example camera location
    plot_random_images(
        meta_data,
        camera_location="B02",
        n=6,
        seed=42
    )

    plot_images_from_all_locations(
        meta_data,
        seed=42
    )


if __name__ == "__main__":
    main()
