import ee


PROJECT_ID = "wood-site-thesis"

ee.Initialize(project=PROJECT_ID)


# FIN001 coordinates
latitude = 60.868673
longitude = 26.7346685

point = ee.Geometry.Point(
    [longitude, latitude]
)

# Check approximately the same area
# we want to analyse later.
region = (
    point
    .buffer(500)
    .bounds()
)


print("\nChecking actual orthophoto coverage for FIN001...\n")


for year in range(2015, 2023):

    image_id = f"Finland/SMK/V/50cm/{year}"

    image = ee.Image(image_id)

    pixel_count = (
        image
        .select("R")
        .reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=region,
            scale=10,
            maxPixels=100000,
        )
        .getInfo()
        .get("R", 0)
    )

    if pixel_count > 0:
        status = "VALID IMAGERY"
    else:
        status = "NO DATA"

    print(
        f"{year}: {status} "
        f"| sampled valid pixels: {pixel_count}"
    )