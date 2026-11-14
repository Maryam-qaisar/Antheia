import h5py
import os

folders = {
    "Product 2": "data/raw/product_2",
    "Product 6": "data/raw/product_6"
}

paths = [
    "science/LSAR/identification/radarBand",
    "science/LSAR/identification/listOfFrequencies",
    "science/LSAR/GCOV/metadata/ceosAnalysisReadyData/outputBackscatterDecibelConversionFormula",
    "science/LSAR/GCOV/grids/frequencyA/listOfPolarizations",
    "science/LSAR/GCOV/grids/frequencyA/listOfCovarianceTerms"
]

for name, folder in folders.items():

    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("Missing file:", name)
        continue

    file_path = os.path.join(folder, files[0])

    print("\n", "=" * 50)
    print(name)
    print("=" * 50)

    with h5py.File(file_path, "r") as hdf:

        for path in paths:
            print("\n", path.split("/")[-1])

            if path in hdf:
                value = hdf[path][()]
                print(value)
            else:
                print("Not found at this path")