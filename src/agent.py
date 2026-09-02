import os
from pathlib import Path

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

from site_tools import (
    get_site_images as load_site_images,
    get_site_information as load_site_information,
)

from vision import (
    run_site_analysis as run_vision_site_analysis,
)

from earth_engine_tools import (
    initialize_earth_engine,
)

from orthophoto_vision import (
    analyse_latest_finland_orthophoto,
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


# ---------------------------------------------------------
# Tool 1: Site metadata
# ---------------------------------------------------------

@function_tool
def get_site_information(site_id: str) -> str:
    """
    Return basic information about one known wood site.

    Args:
        site_id: Site identifier, for example FIN001.
    """

    try:
        site = load_site_information(site_id)

        return (
            f"Site ID: {site['site_id']}\n"
            f"Site name: {site['site_name']}\n"
            f"Country: {site['country']}\n"
            f"Latitude: {site['latitude']}\n"
            f"Longitude: {site['longitude']}"
        )

    except (FileNotFoundError, ValueError) as error:
        return f"Error: {error}"


# ---------------------------------------------------------
# Tool 2: Local historical screenshots
# ---------------------------------------------------------

@function_tool
def get_site_images(site_id: str) -> str:
    """
    Return historical screenshot files available
    for one known site.

    Args:
        site_id: Site identifier, for example FIN001.
    """

    try:
        images = load_site_images(site_id)

        lines = [
            f"Historical images available for "
            f"{site_id.upper()}:"
        ]

        for image in images:
            image_path = Path(
                image["image_path"]
            )

            lines.append(
                f"- Date: {image['image_date']} "
                f"| File: {image_path.name}"
            )

        return "\n".join(lines)

    except (FileNotFoundError, ValueError) as error:
        return f"Error: {error}"


# ---------------------------------------------------------
# Tool 3: Analyse known site screenshots
# ---------------------------------------------------------

@function_tool
def analyse_site(site_id: str) -> str:
    """
    Analyse all locally available historical
    screenshots for one known wood site.

    Args:
        site_id: Site identifier, for example FIN001.
    """

    try:
        report = run_vision_site_analysis(
            site_id.strip().upper()
        )

        report_path = (
            BASE_DIR
            / "data"
            / "results"
            / f"{site_id.strip().upper()}_report.json"
        )

        return (
            f"Historical screenshot analysis completed "
            f"for {site_id.upper()}.\n\n"

            f"Historical comparison:\n"
            f"{report['historical_comparison']}\n\n"

            f"Report saved to:\n"
            f"{report_path}"
        )

    except Exception as error:
        return (
            f"Analysis failed for "
            f"{site_id.upper()}: {error}"
        )


# ---------------------------------------------------------
# Tool 4: Coordinate-based Earth Engine analysis
# ---------------------------------------------------------

@function_tool
def analyse_finland_location(
    latitude: float,
    longitude: float,
) -> str:
    """
    Analyse a location in Finland using automatically
    selected high-resolution orthophoto imagery from
    Google Earth Engine.

    The image is retrieved into memory and is not
    permanently stored locally.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
    """

    try:
        initialize_earth_engine()

        result = (
            analyse_latest_finland_orthophoto(
                latitude=latitude,
                longitude=longitude,
            )
        )

        metadata = result["metadata"]
        analysis = result["analysis"]

        return (
            "Earth Engine location analysis completed.\n\n"

            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}\n"

            f"Imagery source: "
            f"{metadata['source']}\n"

            f"Selected orthophoto year: "
            f"{metadata['orthophoto_year']}\n"

            f"Image ID: "
            f"{metadata['image_id']}\n\n"

            f"Visual assessment:\n"
            f"{analysis}"
        )

    except Exception as error:
        return (
            "Earth Engine location analysis failed.\n"
            f"Error: {error}"
        )


# ---------------------------------------------------------
# AI Agent
# ---------------------------------------------------------

wood_site_agent = Agent(
    name="Wood-Site Monitoring Agent",

    instructions=(
        "You are an AI agent developed for a bachelor "
        "thesis investigating the use of AI and openly "
        "available geospatial imagery for identifying "
        "and monitoring wood-storage and wood-processing "
        "sites.\n\n"

        "Choose tools according to the user's request.\n\n"

        "If the user provides a known site ID such as "
        "FIN001 and asks for metadata, use "
        "get_site_information.\n\n"

        "If the user asks which locally stored historical "
        "images exist for a known site, use "
        "get_site_images.\n\n"

        "If the user asks to analyse historical screenshots "
        "for a known site ID, use analyse_site.\n\n"

        "If the user provides latitude and longitude and "
        "asks you to identify, inspect, assess, or analyse "
        "the location in Finland, use "
        "analyse_finland_location.\n\n"

        "When using Earth Engine analysis, explain which "
        "imagery year was automatically selected.\n\n"

        "Base conclusions only on information returned "
        "by the tools.\n\n"

        "Do not invent timber volume, production levels, "
        "sales, revenue, market demand, purchasing intent, "
        "company identity, or business performance.\n\n"

        "Visual site characteristics may be treated as "
        "potential decision-support indicators, but they "
        "must not be presented as direct proof of market "
        "demand or purchasing intention.\n\n"

        "Clearly distinguish visible evidence from "
        "uncertainty.\n\n"

        "Keep answers concise, evidence-based, and "
        "appropriate for an academic research prototype."
    ),

    tools=[
        get_site_information,
        get_site_images,
        analyse_site,
        analyse_finland_location,
    ],
)


# ---------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------

def main() -> None:

    user_request = input(
        "What would you like the "
        "wood-site agent to do?\n> "
    )

    result = Runner.run_sync(
        wood_site_agent,
        user_request,
    )

    print("\nAgent response:\n")
    print(result.final_output)


if __name__ == "__main__":
    main()