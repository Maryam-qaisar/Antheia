import h5py
import os
import numpy as np

folders = {
    "Product 2": "data/raw/product_2",
    "Product 6": "data/raw/product_6"
}

coordinates = {}

for name, folder in folders.items():

    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("File missing:", name)
        continue

    file_path = os.path.join(folder, files[0])

    with h5py.File(file_path, "r") as hdf:

        base = "science/LSAR/GCOV/grids/frequencyA/"

        x = hdf[base + "xCoordinates"][:]
        y = hdf[base + "yCoordinates"][:]

        coordinates[name] = (x, y)

x2, y2 = coordinates["Product 2"]
x6, y6 = coordinates["Product 6"]

print("X coordinate comparison")
print("Same length:", len(x2) == len(x6))
print("Maximum difference:", np.max(np.abs(x2 - x6)))

print("\nY coordinate comparison")
print("Same length:", len(y2) == len(y6))
print("Maximum difference:", np.max(np.abs(y2 - y6)))

print("\nGrid alignment check completed.")