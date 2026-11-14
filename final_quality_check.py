import os
import h5py
import numpy as np

# ---------------------------------------
# 1. ROBUST STATISTICS FROM EXISTING MAPS
# ---------------------------------------

file_path = "outputs/data/agri_pulse_data.npz"

print("=" * 55)
print("AGRIPULSE - ROBUST STATISTICS")
print("=" * 55)

data = np.load(file_path)

variables = {
    "HH - 30 October": "hh_30_oct",
    "HH - 11 November": "hh_11_nov",
    "HH - Change": "hh_change",
    "HV - 30 October": "hv_30_oct",
    "HV - 11 November": "hv_11_nov",
    "HV - Change": "hv_change"
}

for label, key in variables.items():

    values = data[key]
    values = values[np.isfinite(values)]

    print("\n", label)

    if len(values) == 0:
        print("No valid values")
        continue

    print("Valid cells:", len(values))
    print("Median:", round(float(np.median(values)), 3))
    print("5th percentile:", round(float(np.percentile(values, 5)), 3))
    print("95th percentile:", round(float(np.percentile(values, 95)), 3))


# ---------------------------------------
# 2. FIND INCIDENCE ANGLE METADATA
# ---------------------------------------

folders = {
    "30 October": "data/raw/product_6",
    "11 November": "data/raw/product_2"
}

print("\n" + "=" * 55)
print("RADAR INCIDENCE ANGLE METADATA")
print("=" * 55)

for date, folder in folders.items():

    files = [
        f for f in os.listdir(folder)
        if f.endswith(".h5")
    ]

    if not files:
        print("File missing:", date)
        continue

    path = os.path.join(folder, files[0])

    print("\nDATE:", date)

    with h5py.File(path, "r") as hdf:

        found = []

        def find_incidence(name, item):

            if isinstance(item, h5py.Dataset):
                if "incidenceangle" in name.lower():
                    found.append(name)

        hdf.visititems(find_incidence)

        if not found:
            print("No incidence angle dataset found.")
            continue

        for dataset_path in found:

            dataset = hdf[dataset_path]

            print("\nDataset:", dataset_path)
            print("Shape:", dataset.shape)
            print("Units:", dataset.attrs.get("units", "Not specified"))

            if dataset.size == 0:
                continue

            if dataset.shape == ():
                sample = np.asarray([dataset[()]])
            else:
                step = max(1, dataset.size // 100000)
                sample = dataset[()].reshape(-1)[::step]

            sample = sample.astype(float)
            sample = sample[np.isfinite(sample)]

            if len(sample):
                print("Minimum:", float(np.min(sample)))
                print("Maximum:", float(np.max(sample)))
                print("Mean:", float(np.mean(sample)))

print("\nQuality checks completed.")