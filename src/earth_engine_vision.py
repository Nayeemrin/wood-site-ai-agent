import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from earth_engine_tools import (
    get_best_sentinel2_image_bytes,
    initialize_earth_engine,
)


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )

client = OpenAI(api_key=api_key)


def analyse_earth_engine_image(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Retrieve one Sentinel-2 image from Earth Engine
    directly into memory and analyse it with OpenAI vision.

    No image is permanently saved locally.
    """

    image_bytes, metadata = (
        get_best_sentinel2_image_bytes(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            max_cloud=30,
            buffer_meters=500,
        )
    )

    print("\nEarth Engine image retrieved.")
    print(f"Date: {metadata['date']}")
    print(
        f"Cloud cover: "
        f"{metadata['cloud_percentage']}%"
    )
    print(
        f"Image size: "
        f"{len(image_bytes):,} bytes"
    )

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    print("\nSending image to OpenAI vision...")

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Analyse this satellite image of the "
                            "location given below.\n\n"
                            f"Latitude: {latitude}\n"
                            f"Longitude: {longitude}\n"
                            f"Image date: {metadata['date']}\n\n"
                            "The purpose is to assess whether the "
                            "location appears consistent with a "
                            "wood-storage or wood-processing site.\n\n"
                            "Describe only what is visually supported "
                            "by the image. Consider:\n"
                            "- open industrial yard areas\n"
                            "- elongated or repeated storage patterns\n"
                            "- possible timber or material storage\n"
                            "- buildings\n"
                            "- roads or rail access\n"
                            "- vegetation\n"
                            "- signs of industrial activity\n"
                            "- limitations caused by satellite "
                            "resolution\n\n"
                            "Do not estimate exact timber volume, "
                            "production, sales, revenue, or market "
                            "demand.\n\n"
                            "Finish with:\n"
                            "Wood-site likelihood: low, medium, or high\n"
                            "Confidence: low, medium, or high"
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            "data:image/png;base64,"
                            + encoded_image
                        ),
                        "detail": "high",
                    },
                ],
            }
        ],
    )

    return {
        "metadata": metadata,
        "analysis": response.output_text,
    }


if __name__ == "__main__":

    initialize_earth_engine()

    # FIN001 coordinates
    latitude = 60.868673
    longitude = 26.7346685

    result = analyse_earth_engine_image(
        latitude=latitude,
        longitude=longitude,
        start_date="2025-06-01",
        end_date="2025-07-01",
    )

    print()
    print("=" * 60)
    print("EARTH ENGINE + OPENAI ANALYSIS")
    print("=" * 60)
    print()
    print(result["analysis"])