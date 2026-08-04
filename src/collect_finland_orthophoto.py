import ee
import requests
import os
import pandas as pd
from pathlib import Path

# -----------------------------------
# Initialize Earth Engine
# -----------------------------------
ee.Initialize(project="wood-site-thesis")

# -----------------------------------
# Paths
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
    / "finland_orthophoto"
)

os.makedirs(images_folder, exist_ok=True)

# -----------------------------------
# Read CSV
# -----------------------------------
sites = pd.read_csv(csv_path)

# Remove Unknown sites
sites = sites[
    sites["name"]
    .astype(str)
    .str.lower() != "unknown"
]

# -----------------------------------
# Take first 5 Finland sites
# -----------------------------------
finland_sites = sites[
    sites["country"].str.contains(
        "Finland",
        case=False,
        na=False
    )
].head(10)

print(
    f"Found {len(finland_sites)} "
    f"Finland sites"
)

# -----------------------------------
# Finland 50 cm Orthophoto dataset
# -----------------------------------
orthophotos = ee.ImageCollection(
    "Finland/SMK/VV/50cm"
)

# -----------------------------------
# Download images
# -----------------------------------
for _, row in finland_sites.iterrows():

    site_name = str(row["name"])

    safe_name = (
        site_name
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    lat = row["lat"]
    lon = row["lon"]

    print(
        f"\nProcessing: "
        f"{site_name}"
    )

    point = ee.Geometry.Point(
        [lon, lat]
    )

    # Mosaic orthophotos
    image = orthophotos.mosaic()

    url = image.getThumbURL({

        # Zoom area
        "region":
            point.buffer(200)
            .bounds()
            .getInfo(),

        # Higher resolution
        "dimensions": 1800,

        # Bands
        "bands":
            ["R", "G", "N"],

        "min": 0,
        "max": 255
    })

    response = requests.get(url)

    filename = (
        images_folder
        / f"Finland_"
        f"{safe_name}"
        f"_orthophoto.jpg"
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
    "5 Finland orthophotos!"
)