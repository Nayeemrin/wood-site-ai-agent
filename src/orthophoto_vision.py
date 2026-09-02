import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from earth_engine_tools import (
    get_latest_finland_orthophoto_bytes,
    initialize_earth_engine,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )

client = OpenAI(api_key=api_key)


# ---------------------------------------------------------
# OpenAI vision analysis
# ---------------------------------------------------------

def analyse_latest_finland_orthophoto(
    latitude: float,
    longitude: float,
) -> dict:
    """
    Automatically find the latest valid Finland
    orthophoto for a coordinate, retrieve it from
    Earth Engine into memory, and analyse it with
    OpenAI vision.

    No permanent image file is created.
    """

    print(
        "\nSearching Earth Engine for the "
        "latest valid Finland orthophoto..."
    )

    image_bytes, metadata = (
        get_latest_finland_orthophoto_bytes(
            latitude=latitude,
            longitude=longitude,
            buffer_meters=500,
            dimensions=1200,
        )
    )

    selected_year = metadata[
        "orthophoto_year"
    ]

    print("\nOrthophoto retrieved successfully.")
    print(
        f"Selected year: {selected_year}"
    )
    print(
        f"Image ID: {metadata['image_id']}"
    )
    print(
        f"Image size in memory: "
        f"{len(image_bytes):,} bytes"
    )
    print(
        "No local image file was created."
    )

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    print(
        "\nSending orthophoto to "
        "OpenAI vision..."
    )

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Analyse this high-resolution aerial "
                            "orthophoto of the location below.\n\n"

                            f"Latitude: {latitude}\n"
                            f"Longitude: {longitude}\n"
                            f"Orthophoto dataset year: "
                            f"{selected_year}\n\n"

                            "The purpose is to assess whether this "
                            "location appears consistent with a "
                            "wood-storage, timber-handling, sawmill, "
                            "or wood-processing site.\n\n"

                            "Describe only features that are visually "
                            "supported by the image.\n\n"

                            "Examine specifically:\n"
                            "- visible timber or log storage rows\n"
                            "- long repeated or parallel material stacks\n"
                            "- packaged or processed wood stacks\n"
                            "- woodchip or sawdust-like piles\n"
                            "- open storage or maneuvering yards\n"
                            "- industrial buildings\n"
                            "- road access\n"
                            "- rail access\n"
                            "- material-handling areas\n"
                            "- surrounding vegetation or forest\n"
                            "- other visible evidence relevant to "
                            "wood-industry activity\n\n"

                            "Clearly distinguish visible evidence "
                            "from uncertainty.\n\n"

                            "Do not estimate exact timber volume, "
                            "production, sales, revenue, market demand, "
                            "or purchasing intent.\n\n"

                            "At the end provide:\n"
                            "Wood-site likelihood: low, medium, or high\n"
                            "Visible activity indication: "
                            "low, medium, or high\n"
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


# ---------------------------------------------------------
# Test with FIN001
# ---------------------------------------------------------

if __name__ == "__main__":

    initialize_earth_engine()

    # FIN001 coordinates
    latitude = 60.868673
    longitude = 26.7346685

    result = (
        analyse_latest_finland_orthophoto(
            latitude=latitude,
            longitude=longitude,
        )
    )

    print()
    print("=" * 60)
    print(
        "AUTOMATIC ORTHOPHOTO + "
        "OPENAI ANALYSIS"
    )
    print("=" * 60)
    print()

    print(result["analysis"])