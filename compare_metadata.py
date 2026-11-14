import h5py
import os
import numpy as np

folders = {
    "Product 2 - 11 November": "data/raw/product_2",
    "Product 6 - 30 October": "data/raw/product_6"
}

def read_value(hdf, path):
    value = hdf[path][()]

    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")

    if isinstance(value, np.ndarray):
        return [
            x.decode("utf-8", errors="replace")
            if isinstance(x, bytes) else x
            for x in value
        ]

    return value

for product_name, folder in folders.items():

    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("HDF5 file missing:", folder)
        continue

    file_path = os.path.join(folder, files[0])

    print("\n" + "=" * 55)
    print(product_name)
    print("=" * 55)

    with h5py.File(file_path, "r") as hdf:

        metadata = [
            "science/LSAR/identification/orbitPassDirection",
            "science/LSAR/identification/absoluteOrbitNumber",
            "science/LSAR/identification/trackNumber",
            "science/LSAR/identification/frameNumber",
            "science/LSAR/identification/productVersion",
            "science/LSAR/identification/compositeReleaseId",
            "science/LSAR/identification/zeroDopplerStartTime",
            "science/LSAR/identification/zeroDopplerEndTime",
            "science/LSAR/identification/boundingPolygon",
            "science/LSAR/identification/listOfFrequencies"
        ]

        print("\nACQUISITION METADATA")

        for path in metadata:
            print(path.split("/")[-1], ":", read_value(hdf, path))

        print("\nGRID INFORMATION")

        for frequency in ["frequencyA", "frequencyB"]:

            base = (
                "science/LSAR/GCOV/grids/" + frequency
            )

            print("\n", frequency)

            for item in [
                "HHHH",
                "HVHV",
                "projection",
                "xCoordinateSpacing",
                "yCoordinateSpacing",
                "xCoordinates",
                "yCoordinates"
            ]:

                path = base + "/" + item
                dataset = hdf[path]

                if item in ["xCoordinates", "yCoordinates"]:
                    values = dataset[()]
                    print(
                        item,
                        "minimum:", values.min(),
                        "maximum:", values.max()
                    )
                elif dataset.shape == ():
                    print(item, ":", dataset[()])
                else:
                    print(item, "shape:", dataset.shape)

print("\nMetadata comparison completed!")