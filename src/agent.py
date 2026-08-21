import os
from pathlib import Path

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

from site_tools import (
    get_site_images as load_site_images,
    get_site_information as load_site_information,
)

from vision import run_site_analysis as run_vision_site_analysis


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )


@function_tool
def get_site_information(site_id: str) -> str:
    """
    Return basic information about one wood site.

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


@function_tool
def get_site_images(site_id: str) -> str:
    """
    Return the historical screenshot files available for one site.

    Args:
        site_id: Site identifier, for example FIN001.
    """
    try:
        images = load_site_images(site_id)

        lines = [
            f"Historical images available for {site_id.upper()}:"
        ]

        for image in images:
            image_path = Path(image["image_path"])

            lines.append(
                f"- Date: {image['image_date']} "
                f"| File: {image_path.name}"
            )

        return "\n".join(lines)

    except (FileNotFoundError, ValueError) as error:
        return f"Error: {error}"


@function_tool
def analyse_site(site_id: str) -> str:
    """
    Analyse all available historical overhead images
    for one wood site and compare changes over time.

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
            f"Analysis completed for {site_id.upper()}.\n\n"
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


wood_site_agent = Agent(
    name="Wood-Site Monitoring Agent",

    instructions=(
        "You are an AI agent for a bachelor thesis project "
        "about identifying and monitoring wood-storage sites "
        "using historical overhead imagery.\n\n"

        "Use the available tools according to the user's request.\n\n"

        "Use get_site_information when the user asks about "
        "site metadata, coordinates, country, or site name.\n"

        "Use get_site_images when the user asks which historical "
        "images or dates are available.\n"

        "Use analyse_site when the user asks you to analyse, "
        "monitor, compare, or investigate a site's historical "
        "overhead imagery.\n\n"

        "Never invent site information, image findings, exact "
        "timber volume, production figures, sales, revenue, "
        "or market demand.\n"

        "Clearly distinguish visible evidence from uncertainty.\n"
        "Keep the final answer concise and evidence-based."
    ),

    tools=[
        get_site_information,
        get_site_images,
        analyse_site,
    ],
)


def main() -> None:
    user_request = input(
        "What would you like the wood-site agent to do?\n> "
    )

    result = Runner.run_sync(
        wood_site_agent,
        user_request,
    )

    print("\nAgent response:\n")
    print(result.final_output)


if __name__ == "__main__":
    main()