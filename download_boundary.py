import requests
import json
import os

url = (
    "https://github.com/wmgeolab/geoBoundaries/raw/"
    "9469f09/releaseData/gbOpen/PAK/ADM2/"
    "geoBoundaries-PAK-ADM2.geojson"
)

print("Downloading Pakistan district boundaries...")

response = requests.get(url, timeout=120)
response.raise_for_status()

data = response.json()

print("Download successful!")
print("Total district features:", len(data["features"]))

# Find Faisalabad by checking district properties
matches = []

for feature in data["features"]:
    properties = feature["properties"]

    for key, value in properties.items():
        if "faisalabad" in str(value).lower():
            matches.append(feature)
            print("\nMatching property:", key, "=", value)
            break

if not matches:
    print("Faisalabad was not found. Check the downloaded properties.")
else:
    os.makedirs("data/reference", exist_ok=True)

    output_path = "data/reference/faisalabad_district.geojson"

    result = {
        "type": "FeatureCollection",
        "features": matches
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file)

    print("\nBoundary saved successfully!")
    print("Location:", output_path)