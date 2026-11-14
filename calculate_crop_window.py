import h5py
import os
import json
import numpy as np
from pyproj import Transformer

# Load district boundary
boundary_path = "data/reference/faisalabad_district.geojson"

with open(boundary_path, "r", encoding="utf-8") as file:
    boundary = json.load(file)

# Convert longitude/latitude to NISAR coordinates
transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32643",
    always_xy=True
)

all_points = []

def collect_points(item):
    if isinstance(item[0], (int, float)):
        all_points.append(item)
    else:
        for child in item:
            collect_points(child)

for feature in boundary["features"]:
    collect_points(feature["geometry"]["coordinates"])

projected = [
    transformer.transform(point[0], point[1])
    for point in all_points
]

min_x = min(p[0] for p in projected)
max_x = max(p[0] for p in projected)
min_y = min(p[1] for p in projected)
max_y = max(p[1] for p in projected)

folders = {
    "Product 2 - 11 November": "data/raw/product_2",
    "Product 6 - 30 October": "data/raw/product_6"
}

for name, folder in folders.items():

    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("Missing file:", name)
        continue

    file_path = os.path.join(folder, files[0])

    with h5py.File(file_path, "r") as hdf:

        base = "science/LSAR/GCOV/grids/frequencyA/"

        x = hdf[base + "xCoordinates"][:]
        y = hdf[base + "yCoordinates"][:]

        # Find columns and rows inside the district extent
        columns = np.where((x >= min_x) & (x <= max_x))[0]
        rows = np.where((y >= min_y) & (y <= max_y))[0]

        if len(columns) == 0 or len(rows) == 0:
            print("No matching pixels:", name)
            continue

        col_start = columns.min()
        col_end = columns.max() + 1

        row_start = rows.min()
        row_end = rows.max() + 1

        crop_width = col_end - col_start
        crop_height = row_end - row_start

        print("\n", name)
        print("Column range:", col_start, "to", col_end)
        print("Row range:", row_start, "to", row_end)
        print("Crop dimensions:", crop_height, "x", crop_width)
        print("Number of pixels:", crop_height * crop_width)

print("\nCrop window calculation completed!")