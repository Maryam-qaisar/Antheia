import json
from pathlib import Path

import asf_search as asf


# Approximate rectangular search area around Faisalabad District.
# This is a search boundary, not an official district boundary.
FAISALABAD_AOI = (
    "POLYGON(("
    "72.85 31.05, "
    "73.55 31.05, "
    "73.55 31.75, "
    "72.85 31.75, "
    "72.85 31.05"
    "))"
)

OUTPUT_FOLDER = Path("data/raw")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def search_nisar_products(maturity):
    print(f"\nSearching for {maturity} NISAR GCOV products...")

    results = asf.search(
        dataset="NISAR",
        processingLevel="GCOV",
        intersectsWith=FAISALABAD_AOI,
        dataMaturity=maturity,
        maxResults=100
    )

    print(f"Products found: {len(results)}")

    # Save the complete search results and their metadata.
    output_file = OUTPUT_FOLDER / f"nisar_{maturity.lower()}_results.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(results.geojson(), file, indent=4, default=str)

    # Display the metadata of each matching product.
    for number, product in enumerate(results, start=1):
        print(f"\nProduct {number}")
        print("-" * 40)

        for key, value in product.properties.items():
            print(f"{key}: {value}")

    return len(results)


def main():
    validated_count = search_nisar_products("VALIDATED")
    provisional_count = search_nisar_products("PROVISIONAL")

    print("\nSEARCH SUMMARY")
    print("-------------------------")
    print("Validated products:", validated_count)
    print("Provisional products:", provisional_count)
    print("\nSearch results have been saved in data/raw/")


if __name__ == "__main__":
    main()