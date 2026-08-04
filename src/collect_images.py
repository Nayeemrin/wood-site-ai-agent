import ee
import requests
import os
import pandas as pd
from pathlib import Path

# -----------------------------------
# Initialize Google Earth Engine
# -----------------------------------
ee.Initialize(project="wood-site-thesis")

# -----------------------------------
# Set project paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = (
    BASE_DIR
    / "data"
    / "wood_sites_finland_sweden.csv"
)

images_folder = (
    BASE_DIR
    / "data"
    / "images"
)

# Create image folder if missing
os.makedirs(images_folder, exist_ok=True)

# -----------------------------------
# Read CSV
# -----------------------------------
sites = pd.read_csv(csv_path)

# Remove "Unknown" sites
sites = sites[
    sites["name"]
    .astype(str)
    .str.lower() != "unknown"
]

print("CSV loaded successfully!")

# -----------------------------------
# Select 5 Finland + 5 Sweden sites
# -----------------------------------
finland_sites = sites[
    sites["country"].str.contains(
        "Finland",
        case=False,
        na=False
    )
].head(5)

sweden_sites = sites[
    sites["country"].str.contains(
        "Sweden",
        case=False,
        na=False
    )
].head(5)

# Combine selected sites
selected_sites = pd.concat(
    [finland_sites, sweden_sites]
)

print(
    f"Selected {len(selected_sites)} sites"
)

# -----------------------------------
# Download satellite images
# -----------------------------------
for _, row in selected_sites.iterrows():

    site_name = str(row["name"])
    country = str(row["country"])

    # Clean filename
    safe_name = (
        site_name
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    lat = row["lat"]
    lon = row["lon"]

    print(
        f"\nProcessing {country}: "
        f"{site_name}"
    )

    point = ee.Geometry.Point(
        [lon, lat]
    )

    # Sentinel-2 collection
    collection = (
        ee.ImageCollection(
            "COPERNICUS/S2_SR_HARMONIZED"
        )
        .filterBounds(point)
        .filterDate(
            "2025-01-01",
            "2025-12-31"
        )
        .sort(
            "CLOUDY_PIXEL_PERCENTAGE"
        )
    )

    # Get first 3 frames
    images = collection.toList(3)

    for i in range(3):

        image = ee.Image(
            images.get(i)
        )

        url = image.getThumbURL({

            # Zoom level
            "region":
                point.buffer(300)
                .bounds()
                .getInfo(),

            # Resolution
            "dimensions": 1200,

            # RGB bands
            "bands":
                ["B4", "B3", "B2"],

            # Brightness
            "min": 0,
            "max": 3000
        })

        response = requests.get(url)

        filename = (
            images_folder
            / f"{country}"
            f"_{safe_name}"
            f"_frame_{i+1}.jpg"
        )

        with open(
            filename,
            "wb"
        ) as file:

            file.write(
                response.content
            )

        print(
            f"Saved: "
            f"{filename.name}"
        )

print(
    "\nFinished downloading "
    "satellite images!"
)