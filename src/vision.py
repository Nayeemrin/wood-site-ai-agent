import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from site_tools import (
    get_site_images,
    get_site_information,
    save_site_report,
)


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )

client = OpenAI(api_key=api_key)


def encode_image(image_path: Path) -> str:
    """
    Convert a local image into a base64 string.
    """
    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    with image_path.open("rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def analyse_single_image(image_path: Path) -> str:
    """
    Analyse one wood-site screenshot.
    """
    encoded_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Analyse this overhead image carefully. "
                            "Describe only what is visually observable. "
                            "State whether the location appears consistent "
                            "with a wood-storage or wood-processing site. "
                            "Mention visible storage rows, open yards, "
                            "buildings, roads, vegetation, and uncertainty. "
                            "Do not estimate exact timber volume."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            "data:image/jpeg;base64,"
                            + encoded_image
                        ),
                        "detail": "high",
                    },
                ],
            }
        ],
    )

    return response.output_text


def analyse_site_images(site_id: str) -> list[dict]:
    """
    Analyse every screenshot belonging to one site.
    """
    site_images = get_site_images(site_id)

    analyses = []

    for image_info in site_images:
        image_path = Path(image_info["image_path"])

        print(
            f"\nAnalysing "
            f"{image_info['image_date']} "
            f"({image_path.name})..."
        )

        analysis_text = analyse_single_image(
            image_path
        )

        analyses.append(
            {
                "site_id": site_id.upper(),
                "image_date": image_info["image_date"],
                "image_path": str(image_path),
                "analysis": analysis_text,
            }
        )

    return analyses


def compare_historical_images(
    analyses: list[dict],
) -> str:
    """
    Compare multiple historical analyses
    from the same site.
    """
    if len(analyses) < 2:
        raise ValueError(
            "At least two image analyses are "
            "required for comparison."
        )

    comparison_input = []

    for result in analyses:
        comparison_input.append(
            f"Date: {result['image_date']}\n"
            f"Analysis:\n{result['analysis']}"
        )

    combined_text = "\n\n".join(
        comparison_input
    )

    response = client.responses.create(
        model="gpt-5",
        input=(
            "Compare the following historical "
            "overhead-image analyses of the same "
            "wood-storage or wood-processing site.\n\n"

            "Identify only changes supported by "
            "the observations.\n\n"

            "Focus on:\n"
            "- visible wood-storage extent\n"
            "- apparent use of open yard space\n"
            "- changes in storage rows or material piles\n"
            "- visible infrastructure changes\n"
            "- possible increase, decrease, or stability "
            "in visible activity\n"
            "- uncertainty\n\n"

            "Do not claim changes in sales, production "
            "volume, revenue, market demand, or exact "
            "timber volume.\n\n"

            "Finish with these two lines:\n"
            "Overall visible trend: ...\n"
            "Confidence: low, medium, or high\n\n"

            f"{combined_text}"
        ),
    )

    return response.output_text


def run_site_analysis(site_id: str) -> dict:
    """
    Run the complete analysis workflow
    for one wood site.
    """

    print(
        f"\nStarting analysis for {site_id}..."
    )

    # 1. Get site metadata
    site_information = get_site_information(
        site_id
    )

    # 2. Analyse all historical screenshots
    image_analyses = analyse_site_images(
        site_id
    )

    # 3. Compare the historical analyses
    historical_comparison = (
        compare_historical_images(
            image_analyses
        )
    )

    # 4. Build the final report
    report = {
        "site": site_information,
        "image_analyses": image_analyses,
        "historical_comparison": (
            historical_comparison
        ),
    }

    # 5. Save the final report
    saved_path = save_site_report(
        site_id,
        report,
    )

    print(
        f"\nReport saved successfully:"
        f"\n{saved_path}"
    )

    return report


if __name__ == "__main__":
    try:
        report = run_site_analysis(
            "FIN001"
        )

        print("\n")
        print("=" * 60)
        print("HISTORICAL COMPARISON")
        print("=" * 60)
        print()

        print(
            report["historical_comparison"]
        )

    except Exception as error:
        print(f"Error: {error}")