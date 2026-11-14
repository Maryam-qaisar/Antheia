import h5py
import os

# Location of our downloaded NISAR files
folders = [
    "data/raw/product_2",
    "data/raw/product_6"
]

for folder in folders:

    print("\n" + "=" * 60)
    print("INSPECTING:", folder)
    print("=" * 60)

    # Find the HDF5 file
    files = [f for f in os.listdir(folder) if f.endswith(".h5")]

    if not files:
        print("No HDF5 file found!")
        continue

    file_path = os.path.join(folder, files[0])

    # Open the HDF5 file in read-only mode
    with h5py.File(file_path, "r") as hdf:

        print("\nFile opened successfully!")

        def display_structure(name, item):

            if isinstance(item, h5py.Dataset):
                print(f"DATASET: {name}")
                print("Shape:", item.shape)
                print("Data type:", item.dtype)

            else:
                print(f"GROUP: {name}")

        # Display internal groups and datasets
        hdf.visititems(display_structure)

print("\nInspection completed!")