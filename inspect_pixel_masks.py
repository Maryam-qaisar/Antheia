import h5py
import os
import numpy as np

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

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    with h5py.File(path, "r") as hdf:

        for dataset_name in [
            "mask",
            "inputDataExceptionMask",
            "HHHH",
            "HVHV"
        ]:

            dataset = hdf[base + dataset_name]

            print("\nDataset:", dataset_name)
            print("Shape:", dataset.shape)
            print("Data type:", dataset.dtype)
            print("Attributes:", dict(dataset.attrs))

            # Read only a small 512 x 512 sample
            sample = dataset[5508:6020, 5619:6131]

            print("Sample minimum:", np.nanmin(sample))
            print("Sample maximum:", np.nanmax(sample))

            if dataset_name in ["mask", "inputDataExceptionMask"]:
                values, counts = np.unique(
                    sample, return_counts=True
                )

                print("Unique values:", values[:30])
                print("Value counts:", counts[:30])

print("\nMask inspection completed!")