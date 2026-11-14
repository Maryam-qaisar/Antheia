import json
import h5py
import os
from pyproj import Transformer

boundary_path = "data/reference/faisalabad_district.geojson"

# Convert geographic coordinates to NISAR's projection
transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32643",
    always_xy=True
)

with open(boundary_path, "r", encoding="utf-8") as file:
    boundary = json.load(file)

all_points = []

def collect_points(item):
    if isinstance(item[0], (int, float)):
        all_points.append(item)
    else:
        for child in item:
            collect_points(child)

for feature in boundary["features"]:
    collect_points(feature["geometry"]["coordinates"])

projected_points = [
    transformer.transform(point[0], point[1])
    for point in all_points
]

district_min_x = min(p[0] for p in projected_points)
district_max_x = max(p[0] for p in projected_points)
district_min_y = min(p[1] for p in projected_points)
district_max_y = max(p[1] for p in projected_points)

print("FAISALABAD DISTRICT - PROJECTED EXTENT")
print("X:", district_min_x, "to", district_max_x)
print("Y:", district_min_y, "to", district_max_y)

folders = {
    "Product 2 - 11 November": "data/raw/product_2",
    "Product 6 - 30 October": "data/raw/product_6"
}

for name, folder in folders.items():

    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("\nMissing:", name)
        continue

    with h5py.File(os.path.join(folder, files[0]), "r") as hdf:

        base = "science/LSAR/GCOV/grids/frequencyA/"

        x = hdf[base + "xCoordinates"][:]
        y = hdf[base + "yCoordinates"][:]

        raster_min_x = min(x)
        raster_max_x = max(x)
        raster_min_y = min(y)
        raster_max_y = max(y)

        covered = (
            district_min_x >= raster_min_x and
            district_max_x <= raster_max_x and
            district_min_y >= raster_min_y and
            district_max_y <= raster_max_y
        )

        print("\n", name)
        print("Raster X:", raster_min_x, "to", raster_max_x)
        print("Raster Y:", raster_min_y, "to", raster_max_y)
        print("District bounding extent inside raster:", covered)

print("\nCoverage check completed!")