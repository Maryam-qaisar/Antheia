import json
import os

file_path = "data/reference/faisalabad_district.geojson"

if not os.path.exists(file_path):
    print("Boundary file not found!")
else:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("File loaded successfully!")
    print("Number of features:", len(data["features"]))

    for feature in data["features"]:
        print("\nDISTRICT INFORMATION")
        print("Properties:", feature["properties"])
        print("Geometry type:", feature["geometry"]["type"])

        coordinates = feature["geometry"]["coordinates"]

        all_points = []

        def collect_points(item):
            if isinstance(item[0], (int, float)):
                all_points.append(item)
            else:
                for child in item:
                    collect_points(child)

        collect_points(coordinates)

        longitudes = [point[0] for point in all_points]
        latitudes = [point[1] for point in all_points]

        print("\nGEOGRAPHIC EXTENT")
        print("West:", min(longitudes))
        print("East:", max(longitudes))
        print("South:", min(latitudes))
        print("North:", max(latitudes))

print("\nBoundary verification completed!")