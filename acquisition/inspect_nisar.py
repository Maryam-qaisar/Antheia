import json
from pathlib import Path

file_path = Path("data/raw/nisar_validated_results.json")

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

products = data.get("features", [])

print("\nVALIDATED NISAR PRODUCTS")
print("=" * 60)
print("Total products:", len(products))

for number, product in enumerate(products, start=1):

    properties = product.get("properties", {})

    print(f"\nPRODUCT {number}")
    print("-" * 40)

    # Display metadata fields related to our analysis.
    keywords = [
        "fileName",
        "sceneName",
        "groupID",
        "startTime",
        "stopTime",
        "polarization",
        "beamMode",
        "processingLevel",
        "dataMaturity",
        "url"
    ]

    for key, value in properties.items():
        if any(word.lower() in key.lower() for word in keywords):
            print(f"{key}: {value}")

print("\nInspection completed.")