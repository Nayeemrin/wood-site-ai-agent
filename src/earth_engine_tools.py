from datetime import datetime, timezone
from urllib.request import urlopen

import ee


PROJECT_ID = "wood-site-thesis"


# ---------------------------------------------------------
# Earth Engine initialization
# ---------------------------------------------------------

def initialize_earth_engine() -> None:
    """
    Initialize Google Earth Engine.
    """
    ee.Initialize(project=PROJECT_ID)


# ---------------------------------------------------------
# Sentinel-2 tools
# ---------------------------------------------------------

def get_sentinel2_collection(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    max_cloud: float = 30,
):
    """
    Return a filtered Sentinel-2 collection
    for one coordinate and date range.
    """

    point = ee.Geometry.Point(
        [longitude, latitude]
    )

    collection = (
        ee.ImageCollection(
            "COPERNICUS/S2_SR_HARMONIZED"
        )
        .filterBounds(point)
        .filterDate(start_date, end_date)
        .filter(
            ee.Filter.lt(
                "CLOUDY_PIXEL_PERCENTAGE",
                max_cloud,
            )
        )
    )

    return collection


def get_best_sentinel2_image_bytes(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    max_cloud: float = 30,
    buffer_meters: int = 500,
) -> tuple[bytes, dict]:
    """
    Retrieve the clearest Sentinel-2 RGB image
    around one coordinate.

    The image is kept in memory only.
    """

    point = ee.Geometry.Point(
        [longitude, latitude]
    )

    collection = get_sentinel2_collection(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        max_cloud=max_cloud,
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        raise ValueError(
            "No Sentinel-2 images were found "
            "for this location and date range."
        )

    image = ee.Image(
        collection
        .sort("CLOUDY_PIXEL_PERCENTAGE")
        .first()
    )

    timestamp = image.get(
        "system:time_start"
    ).getInfo()

    image_date = datetime.fromtimestamp(
        timestamp / 1000,
        tz=timezone.utc,
    ).strftime("%Y-%m-%d")

    cloud_percentage = image.get(
        "CLOUDY_PIXEL_PERCENTAGE"
    ).getInfo()

    image_id = image.id().getInfo()

    region = (
        point
        .buffer(buffer_meters)
        .bounds()
    )

    rgb_image = image.select(
        ["B4", "B3", "B2"]
    )

    thumbnail_url = rgb_image.getThumbURL(
        {
            "region": region,
            "dimensions": 512,
            "min": 0,
            "max": 3000,
            "format": "png",
        }
    )

    with urlopen(
        thumbnail_url,
        timeout=120,
    ) as response:
        image_bytes = response.read()

    metadata = {
        "source": "Sentinel-2",
        "image_id": image_id,
        "date": image_date,
        "cloud_percentage": cloud_percentage,
        "latitude": latitude,
        "longitude": longitude,
        "buffer_meters": buffer_meters,
    }

    return image_bytes, metadata


# ---------------------------------------------------------
# Finland orthophoto tools
# ---------------------------------------------------------

def get_valid_finland_orthophoto_years(
    latitude: float,
    longitude: float,
    buffer_meters: int = 500,
) -> list[int]:
    """
    Find Finland orthophoto years that contain
    actual valid pixels around the requested location.
    """

    point = ee.Geometry.Point(
        [longitude, latitude]
    )

    region = (
        point
        .buffer(buffer_meters)
        .bounds()
    )

    collection = (
        ee.ImageCollection(
            "Finland/SMK/V/50cm"
        )
        .filterBounds(point)
    )

    image_info = collection.getInfo()

    valid_years = []

    for feature in image_info.get(
        "features",
        []
    ):
        image_id = feature["id"]

        try:
            year = int(
                image_id.split("/")[-1]
            )
        except ValueError:
            continue

        image = ee.Image(image_id)

        pixel_result = (
            image
            .select("R")
            .reduceRegion(
                reducer=ee.Reducer.count(),
                geometry=region,
                scale=10,
                maxPixels=100000,
            )
            .getInfo()
        )

        pixel_count = pixel_result.get(
            "R",
            0,
        )

        if pixel_count > 0:
            valid_years.append(year)

    valid_years.sort(
        reverse=True
    )

    return valid_years


def find_latest_finland_orthophoto_year(
    latitude: float,
    longitude: float,
    buffer_meters: int = 500,
) -> int:
    """
    Return the latest Finland orthophoto year
    containing valid imagery at the location.
    """

    valid_years = (
        get_valid_finland_orthophoto_years(
            latitude=latitude,
            longitude=longitude,
            buffer_meters=buffer_meters,
        )
    )

    if not valid_years:
        raise ValueError(
            "No valid Finland 0.5 m orthophoto "
            "was found for this location."
        )

    return valid_years[0]


def get_finland_orthophoto_bytes(
    latitude: float,
    longitude: float,
    year: int,
    buffer_meters: int = 500,
    dimensions: int = 1200,
) -> tuple[bytes, dict]:
    """
    Retrieve one Finland 0.5 m orthophoto.

    Image data is returned directly in memory.
    No permanent image file is created.
    """

    image_id = (
        f"Finland/SMK/V/50cm/{year}"
    )

    image = ee.Image(image_id)

    point = ee.Geometry.Point(
        [longitude, latitude]
    )

    region = (
        point
        .buffer(buffer_meters)
        .bounds()
    )

    rgb_image = image.select(
        ["R", "G", "B"]
    )

    thumbnail_url = rgb_image.getThumbURL(
        {
            "region": region,
            "dimensions": dimensions,
            "min": 0,
            "max": 255,
            "format": "png",
        }
    )

    with urlopen(
        thumbnail_url,
        timeout=120,
    ) as response:
        image_bytes = response.read()

    if not image_bytes:
        raise ValueError(
            "Earth Engine returned an empty orthophoto."
        )

    metadata = {
        "source": "Finland NLS 0.5 m orthophoto",
        "image_id": image_id,
        "orthophoto_year": year,
        "latitude": latitude,
        "longitude": longitude,
        "buffer_meters": buffer_meters,
    }

    return image_bytes, metadata


def get_latest_finland_orthophoto_bytes(
    latitude: float,
    longitude: float,
    buffer_meters: int = 500,
    dimensions: int = 1200,
) -> tuple[bytes, dict]:
    """
    Automatically find the latest valid Finland
    orthophoto for a location and retrieve it
    directly into memory.
    """

    latest_year = (
        find_latest_finland_orthophoto_year(
            latitude=latitude,
            longitude=longitude,
            buffer_meters=buffer_meters,
        )
    )

    image_bytes, metadata = (
        get_finland_orthophoto_bytes(
            latitude=latitude,
            longitude=longitude,
            year=latest_year,
            buffer_meters=buffer_meters,
            dimensions=dimensions,
        )
    )

    return image_bytes, metadata


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    initialize_earth_engine()

    # FIN001 coordinates
    latitude = 60.868673
    longitude = 26.7346685

    print(
        "\nSearching for valid Finland orthophotos..."
    )

    valid_years = (
        get_valid_finland_orthophoto_years(
            latitude=latitude,
            longitude=longitude,
        )
    )

    print(
        f"Valid years: {valid_years}"
    )

    image_bytes, metadata = (
        get_latest_finland_orthophoto_bytes(
            latitude=latitude,
            longitude=longitude,
        )
    )

    print()
    print(
        "Latest valid orthophoto retrieved successfully."
    )
    print(
        f"Selected year: "
        f"{metadata['orthophoto_year']}"
    )
    print(
        f"Image ID: "
        f"{metadata['image_id']}"
    )
    print(
        f"Image size in memory: "
        f"{len(image_bytes):,} bytes"
    )
    print(
        "No local image file was created."
    )