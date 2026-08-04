import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = (
    BASE_DIR
    / "data"
    / "wood_sites_finland_sweden.csv"
)

sites = pd.read_csv(csv_path)

print("\nFINLAND SITES")
print("-" * 40)

finland = sites[
    sites["country"].str.contains(
        "Finland",
        case=False,
        na=False
    )
]

print(finland[
    ["name", "lat", "lon"]
].head(20))

print("\nSWEDEN SITES")
print("-" * 40)

sweden = sites[
    sites["country"].str.contains(
        "Sweden",
        case=False,
        na=False
    )
]

print(sweden[
    ["name", "lat", "lon"]
].head(20))