import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_FILE = BASE_DIR / "data" / "site_metadata.csv"


def get_site_information(site_id: str) -> dict:
    """
    Return metadata for one site.
    """
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_FILE}"
        )

    clean_site_id = site_id.strip().upper()

    if not clean_site_id:
        raise ValueError("site_id cannot be empty.")

    sites = pd.read_csv(METADATA_FILE)

    required_columns = {
        "site_id",
        "site_name",
        "country",
        "latitude",
        "longitude",
    }

    missing_columns = required_columns - set(sites.columns)

    if missing_columns:
        raise ValueError(
            "Missing required CSV columns: "
            + ", ".join(sorted(missing_columns))
        )

    matching_rows = sites[
        sites["site_id"].astype(str).str.upper() == clean_site_id
    ]

    if matching_rows.empty:
        raise ValueError(
            f"Site '{clean_site_id}' was not found."
        )

    site = matching_rows.iloc[0]

    return {
        "site_id": str(site["site_id"]),
        "site_name": str(site["site_name"]),
        "country": str(site["country"]),
        "latitude": float(site["latitude"]),
        "longitude": float(site["longitude"]),
    }


def get_site_images(site_id: str) -> list[dict]:
    """
    Return all screenshot files for one site.
    """
    clean_site_id = site_id.strip().upper()

    screenshots_folder = (
        BASE_DIR
        / "data"
        / "screenshots"
        / clean_site_id
    )

    if not screenshots_folder.exists():
        raise FileNotFoundError(
            f"Screenshot folder not found: {screenshots_folder}"
        )

    supported_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    image_files = sorted(
        file_path
        for file_path in screenshots_folder.iterdir()
        if (
            file_path.is_file()
            and file_path.suffix.lower() in supported_extensions
        )
    )

    if not image_files:
        raise ValueError(
            f"No screenshots were found for site '{clean_site_id}'."
        )

    images = []

    for image_path in image_files:
        date_part = image_path.stem.replace(
            f"{clean_site_id}_",
            "",
        )

        images.append(
            {
                "site_id": clean_site_id,
                "image_date": date_part,
                "image_path": str(image_path),
            }
        )

    return images


def save_site_report(site_id: str, report: dict) -> str:
    """
    Save one site's analysis report as a JSON file.
    """
    clean_site_id = site_id.strip().upper()

    results_folder = BASE_DIR / "data" / "results"
    results_folder.mkdir(parents=True, exist_ok=True)

    output_file = results_folder / f"{clean_site_id}_report.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return str(output_file)


if __name__ == "__main__":
    try:
        # Test Tool 1: Site information
        site_result = get_site_information("FIN001")

        print("Site information loaded successfully:")
        print(site_result)

        # Test Tool 2: Find screenshots
        image_results = get_site_images("FIN001")

        print("\nSite screenshots found:")

        for image in image_results:
            print(image)

        # Test Tool 3: Save a report
        test_report = {
            "site_id": "FIN001",
            "status": "test successful",
        }

        saved_path = save_site_report(
            "FIN001",
            test_report,
        )

        print("\nTest report saved:")
        print(saved_path)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")