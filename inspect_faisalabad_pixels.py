import h5py
import os
import numpy as np
from pyproj import Transformer

# Known location inside Faisalabad
longitude = 73.0744
latitude = 31.419

# Convert to NISAR projected coordinates
transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32643",
    always_xy=True
)

target_x, target_y = transformer.transform(
    longitude, latitude
)

folders = {
    "Product 2 - 11 November": "data/raw/product_2",
    "Product 6 - 30 October": "data/raw/product_6"
}

base = "science/LSAR/GCOV/grids/frequencyA/"

for name, folder in folders.items():

    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("File missing:", name)
        continue

    path = os.path.join(folder, files[0])

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    with h5py.File(path, "r") as hdf:

        x = hdf[base + "xCoordinates"][:]
        y = hdf[base + "yCoordinates"][:]

        # Find nearest pixel to our known location
        col = int(np.argmin(np.abs(x - target_x)))
        row = int(np.argmin(np.abs(y - target_y)))

        print("Projected location:", target_x, target_y)
        print("Nearest pixel row:", row)
        print("Nearest pixel column:", col)

        # Read a small 9 x 9 area around the location
        r1 = max(0, row - 4)
        r2 = min(len(y), row + 5)
        c1 = max(0, col - 4)
        c2 = min(len(x), col + 5)

        for dataset_name in [
            "mask",
            "inputDataExceptionMask",
            "HHHH",
            "HVHV"
        ]:

            sample = hdf[base + dataset_name][r1:r2, c1:c2]

            print("\nDataset:", dataset_name)
            print("Unique values:",
                  np.unique(sample)[:20])

            if dataset_name in ["HHHH", "HVHV"]:
                valid = sample[np.isfinite(sample)]

                print("Valid pixel count:", len(valid))

                if len(valid) > 0:
                    print("Minimum:", valid.min())
                    print("Maximum:", valid.max())
                    print("Mean:", valid.mean())

print("\nFaisalabad pixel inspection completed!")