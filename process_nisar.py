import os
import json
import csv
import glob
import h5py
import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import shape
from shapely.ops import transform as transform_geometry
from shapely import contains_xy
from pyproj import Transformer


# =========================================================
# 1. PROJECT SETTINGS
# =========================================================

BASE_PATH = "data/raw"
BOUNDARY_PATH = "data/reference/faisalabad_district.geojson"
OUTPUT_PATH = "outputs"

PRODUCTS = {
    "30_Oct_2026": os.path.join(BASE_PATH, "product_6"),
    "11_Nov_2026": os.path.join(BASE_PATH, "product_2")
}

HDF_BASE = "science/LSAR/GCOV/grids/frequencyA/"

# Process ten source rows at a time.
# Output maps will have approximately 100 m pixels.
BLOCK_SIZE = 10

# Exception-mask validity bits from the product metadata.
HH_VALID_BIT = 256
HV_VALID_BIT = 512

# Other exception bits are treated conservatively as quality flags.
OTHER_BITS_MASK = 65535 ^ (HH_VALID_BIT | HV_VALID_BIT)


# =========================================================
# 2. CREATE OUTPUT FOLDERS
# =========================================================

os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_PATH, "maps"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_PATH, "data"), exist_ok=True)


# =========================================================
# 3. FIND THE DOWNLOADED HDF5 FILES
# =========================================================

def find_hdf5(folder):

    files = glob.glob(os.path.join(folder, "*.h5"))

    if not files:
        raise FileNotFoundError(
            "No HDF5 file found in: " + folder
        )

    if len(files) > 1:
        print("Multiple HDF5 files found in", folder)
        print("Using:", os.path.basename(sorted(files)[0]))

    return sorted(files)[0]


product_files = {
    date: find_hdf5(folder)
    for date, folder in PRODUCTS.items()
}

print("\nNISAR files found successfully.")


# =========================================================
# 4. LOAD AND PROJECT THE DISTRICT POLYGON
# =========================================================

print("\nLoading Faisalabad District boundary...")

with open(BOUNDARY_PATH, "r", encoding="utf-8") as file:
    boundary_data = json.load(file)

if len(boundary_data["features"]) != 1:
    raise ValueError(
        "Expected exactly one Faisalabad district feature."
    )

district = shape(boundary_data["features"][0]["geometry"])

if district.is_empty or not district.is_valid:
    raise ValueError("District geometry is empty or invalid.")

transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32643",
    always_xy=True
)

district = transform_geometry(
    transformer.transform,
    district
)

print("District boundary loaded and projected.")


# =========================================================
# 5. CHECK GRID ALIGNMENT AND FIND CROP WINDOW
# =========================================================

print("\nChecking NISAR grids...")

handles = {
    date: h5py.File(path, "r")
    for date, path in product_files.items()
}

try:
    first = handles["30_Oct_2026"]
    second = handles["11_Nov_2026"]

    for hdf in handles.values():
        if HDF_BASE not in hdf:
            raise ValueError("Frequency A group not found.")

    first_grid = first[HDF_BASE]
    second_grid = second[HDF_BASE]

    x = first_grid["xCoordinates"][:]
    y = first_grid["yCoordinates"][:]

    x2 = second_grid["xCoordinates"][:]
    y2 = second_grid["yCoordinates"][:]

    if not np.array_equal(x, x2) or not np.array_equal(y, y2):
        raise ValueError(
            "The two NISAR grids are not identical."
        )

    if first_grid["HHHH"].shape != second_grid["HHHH"].shape:
        raise ValueError("Raster dimensions do not match.")

    print("Grid alignment confirmed.")

    # Find the district's bounding rectangle.
    min_x, min_y, max_x, max_y = district.bounds

    columns = np.where((x >= min_x) & (x <= max_x))[0]
    rows = np.where((y >= min_y) & (y <= max_y))[0]

    if len(columns) == 0 or len(rows) == 0:
        raise ValueError("District does not overlap the NISAR grid.")

    col_start = int(columns.min())
    col_end = int(columns.max()) + 1

    row_start = int(rows.min())
    row_end = int(rows.max()) + 1

    crop_width = col_end - col_start
    crop_height = row_end - row_start

    print("District crop:", crop_height, "x", crop_width)

    # Check that required datasets exist.
    required = [
        "mask",
        "inputDataExceptionMask",
        "HHHH",
        "HVHV"
    ]

    for date, hdf in handles.items():
        for dataset in required:
            if HDF_BASE + dataset not in hdf:
                raise ValueError(
                    f"{dataset} missing in {date}"
                )

    # Verify the mask fill value and conversion formula.
    mask_fill = first_grid["mask"].attrs.get("_FillValue", 255)

    if int(mask_fill) != 255:
        raise ValueError("Unexpected subswath-mask fill value.")

    # Output dimensions after aggregation.
    coarse_rows = (crop_height + BLOCK_SIZE - 1) // BLOCK_SIZE
    coarse_cols = (crop_width + BLOCK_SIZE - 1) // BLOCK_SIZE

    # Store accumulated block sums and counts.
    accumulators = {}

    for polarization in ["HH", "HV"]:
        for date in PRODUCTS:
            accumulators[(polarization, date)] = {
                "sum": np.zeros((coarse_rows, coarse_cols)),
                "count": np.zeros((coarse_rows, coarse_cols))
            }

        accumulators[(polarization, "change")] = {
            "sum": np.zeros((coarse_rows, coarse_cols)),
            "count": np.zeros((coarse_rows, coarse_cols))
        }

    district_pixel_count = 0

    statistics = {}

    for polarization in ["HH", "HV"]:
        for date in list(PRODUCTS) + ["change"]:
            statistics[(polarization, date)] = {
                "sum": 0.0,
                "count": 0,
                "minimum": np.inf,
                "maximum": -np.inf
            }

    # =====================================================
    # 6. PROCESS THE DISTRICT IN SMALL BLOCKS
    # =====================================================

    print("\nStarting district processing...")

    padded_width = coarse_cols * BLOCK_SIZE

    x_crop = x[col_start:col_end]
    x_padded = np.pad(
        x_crop,
        (0, padded_width - crop_width),
        mode="edge"
    )

    for local_start in range(0, crop_height, BLOCK_SIZE):

        local_end = min(
            local_start + BLOCK_SIZE,
            crop_height
        )

        actual_rows = local_end - local_start

        source_start = row_start + local_start
        source_end = row_start + local_end

        y_chunk = y[source_start:source_end]

        # Create projected pixel-centre coordinates.
        xx = np.broadcast_to(
            x_crop[None, :],
            (actual_rows, crop_width)
        )

        yy = np.broadcast_to(
            y_chunk[:, None],
            (actual_rows, crop_width)
        )

        inside = contains_xy(district, xx, yy)

        district_pixel_count += int(np.count_nonzero(inside))

        # Read masks for both dates.
        date_data = {}

        for date, hdf in handles.items():

            group = hdf[HDF_BASE]

            subswath = group["mask"][
                source_start:source_end,
                col_start:col_end
            ]

            exception = group["inputDataExceptionMask"][
                source_start:source_end,
                col_start:col_end
            ]
            
            # Valid subswath values are 1 through 254.
            valid_subswath = (
                (subswath >= 1) & (subswath <= 254)
            )

            # Ignore unrelated exception flags conservatively.
            no_other_exceptions = (
                (exception & OTHER_BITS_MASK) == 0
            )

            date_data[date] = {
                "group": group,
                "subswath": valid_subswath,
                "exception": exception,
                "quality": no_other_exceptions
            }

        # Read and process HH and HV separately.
        for polarization in ["HH", "HV"]:

            dataset_name = "HHHH" if polarization == "HH" else "HVHV"

            valid_bit = (
                HH_VALID_BIT
                if polarization == "HH"
                else HV_VALID_BIT
            )

            values = {}

            for date in PRODUCTS:

                item = date_data[date]

                raw = item["group"][dataset_name][
                    source_start:source_end,
                    col_start:col_end
                ]

                valid_channel = (
                    (item["exception"] & valid_bit) != 0
                )

                valid = (
                    inside
                    & item["subswath"]
                    & item["quality"]
                    & valid_channel
                    & np.isfinite(raw)
                    & (raw > 0)
                )

                db_values = np.full(raw.shape, np.nan, dtype=np.float32)

                db_values[valid] = (
                    10.0 * np.log10(raw[valid])
                )

                values[date] = {
                    "db": db_values,
                    "valid": valid
                }

            # Calculate change only where both dates are valid.
            common = (
                values["30_Oct_2026"]["valid"]
                & values["11_Nov_2026"]["valid"]
            )

            change = np.full(
                common.shape,
                np.nan,
                dtype=np.float32
            )

            change[common] = (
                values["11_Nov_2026"]["db"][common]
                - values["30_Oct_2026"]["db"][common]
            )

            values["change"] = {
                "db": change,
                "valid": common
            }

            # Update statistics and output map accumulators.
            for date in list(PRODUCTS) + ["change"]:

                db = values[date]["db"]
                valid = values[date]["valid"]

                if not np.any(valid):
                    continue

                valid_values = db[valid]

                stat = statistics[(polarization, date)]

                stat["sum"] += float(np.sum(valid_values))
                stat["count"] += int(valid_values.size)
                stat["minimum"] = min(
                    stat["minimum"],
                    float(np.min(valid_values))
                )
                stat["maximum"] = max(
                    stat["maximum"],
                    float(np.max(valid_values))
                )

                # Pad the block so it can be aggregated.
                padded = np.full(
                    (BLOCK_SIZE, padded_width),
                    np.nan,
                    dtype=np.float32
                )

                padded[:actual_rows, :crop_width] = db

                valid_padded = np.zeros(
                    (BLOCK_SIZE, padded_width),
                    dtype=bool
                )

                valid_padded[:actual_rows, :crop_width] = valid

                block_values = padded.reshape(
                    1, BLOCK_SIZE, coarse_cols, BLOCK_SIZE
                )

                block_valid = valid_padded.reshape(
                    1, BLOCK_SIZE, coarse_cols, BLOCK_SIZE
                )

                block_sum = np.nansum(
                    block_values,
                    axis=(1, 3)
                )[0]

                block_count = np.sum(
                    block_valid,
                    axis=(1, 3)
                )[0]

                block_row = local_start // BLOCK_SIZE

                accumulators[(polarization, date)]["sum"][
                    block_row
                ] += block_sum

                accumulators[(polarization, date)]["count"][
                    block_row
                ] += block_count

        if (local_start // BLOCK_SIZE) % 50 == 0:
            print(
                "Processed",
                local_start,
                "of",
                crop_height,
                "rows"
            )

    print("\nRadar processing completed.")

finally:
    for hdf in handles.values():
        hdf.close()


# =========================================================
# 7. CALCULATE FINAL MAP ARRAYS
# =========================================================

print("\nCreating output datasets...")

maps = {}

for key, values in accumulators.items():

    result = np.full(
        values["sum"].shape,
        np.nan,
        dtype=np.float32
    )

    np.divide(
        values["sum"],
        values["count"],
        out=result,
        where=values["count"] > 0
    )

    maps[key] = result


# =========================================================
# 8. SAVE COMPRESSED DATA FOR THE DASHBOARD
# =========================================================

np.savez_compressed(
    os.path.join(OUTPUT_PATH, "data", "agri_pulse_data.npz"),

    hh_30_oct=maps[("HH", "30_Oct_2026")],
    hh_11_nov=maps[("HH", "11_Nov_2026")],
    hh_change=maps[("HH", "change")],

    hv_30_oct=maps[("HV", "30_Oct_2026")],
    hv_11_nov=maps[("HV", "11_Nov_2026")],
    hv_change=maps[("HV", "change")],

    x_coordinates=x_padded[::BLOCK_SIZE][:coarse_cols],
    y_coordinates=y[row_start:row_end:BLOCK_SIZE][:coarse_rows],

    block_size=BLOCK_SIZE
)

print("Compressed dashboard data saved.")


# =========================================================
# 9. SAVE DISTRICT STATISTICS
# =========================================================

csv_path = os.path.join(
    OUTPUT_PATH,
    "district_statistics.csv"
)

with open(csv_path, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Polarization",
        "Observation",
        "Valid_Pixels",
        "Valid_Percent",
        "Mean_Backscatter_dB",
        "Minimum_dB",
        "Maximum_dB"
    ])

    for polarization in ["HH", "HV"]:

        for date in PRODUCTS:

            stat = statistics[(polarization, date)]

            percentage = (
                100 * stat["count"] / district_pixel_count
                if district_pixel_count else 0
            )

            mean = (
                stat["sum"] / stat["count"]
                if stat["count"] else np.nan
            )

            writer.writerow([
                polarization,
                date,
                stat["count"],
                round(percentage, 3),
                round(mean, 4) if np.isfinite(mean) else "",
                stat["minimum"] if stat["count"] else "",
                stat["maximum"] if stat["count"] else ""
            ])

        stat = statistics[(polarization, "change")]

        percentage = (
            100 * stat["count"] / district_pixel_count
            if district_pixel_count else 0
        )

        mean = (
            stat["sum"] / stat["count"]
            if stat["count"] else np.nan
        )

        writer.writerow([
            polarization,
            "11_Nov_minus_30_Oct",
            stat["count"],
            round(percentage, 3),
            round(mean, 4) if np.isfinite(mean) else "",
            stat["minimum"] if stat["count"] else "",
            stat["maximum"] if stat["count"] else ""
        ])

print("District statistics saved.")


# =========================================================
# 10. GENERATE MAPS
# =========================================================

map_folder = os.path.join(OUTPUT_PATH, "maps")

extent = (
    float(x_crop[0]),
    float(x_crop[-1]),
    float(y[row_end - 1]),
    float(y[row_start])
)

def save_map(data, title, filename, color_label, cmap, limits=None):

    plt.figure(figsize=(10, 8))

    image = plt.imshow(
        data,
        origin="upper",
        extent=extent,
        cmap=cmap,
        interpolation="nearest",
        vmin=limits[0] if limits else None,
        vmax=limits[1] if limits else None
    )

    plt.title(title)
    plt.xlabel("UTM Easting (m)")
    plt.ylabel("UTM Northing (m)")

    colorbar = plt.colorbar(image)
    colorbar.set_label(color_label)

    plt.tight_layout()

    plt.savefig(
        os.path.join(map_folder, filename),
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()


for polarization in ["HH", "HV"]:

    date1 = maps[(polarization, "30_Oct_2026")]
    date2 = maps[(polarization, "11_Nov_2026")]
    difference = maps[(polarization, "change")]

    combined = np.concatenate([
        date1[np.isfinite(date1)],
        date2[np.isfinite(date2)]
    ])

    if combined.size:

        lower = float(np.percentile(combined, 2))
        upper = float(np.percentile(combined, 98))

        save_map(
            date1,
            f"{polarization} Backscatter - 30 October 2026",
            f"{polarization}_30_Oct.png",
            "Gamma0 backscatter (dB)",
            "viridis",
            (lower, upper)
        )

        save_map(
            date2,
            f"{polarization} Backscatter - 11 November 2026",
            f"{polarization}_11_Nov.png",
            "Gamma0 backscatter (dB)",
            "viridis",
            (lower, upper)
        )

    valid_change = difference[np.isfinite(difference)]

    if valid_change.size:

        limit = float(
            np.percentile(np.abs(valid_change), 98)
        )

        limit = max(limit, 0.1)

        save_map(
            difference,
            f"{polarization} Backscatter Change - 12 Days",
            f"{polarization}_change.png",
            "Change in Gamma0 backscatter (dB)",
            "RdBu_r",
            (-limit, limit)
        )


# =========================================================
# 11. SAVE A PROCESSING SUMMARY
# =========================================================

summary_path = os.path.join(
    OUTPUT_PATH,
    "processing_summary.txt"
)

with open(summary_path, "w", encoding="utf-8") as file:

    file.write("AGRIPULSE - NISAR PROCESSING SUMMARY\n")
    file.write("=" * 45 + "\n\n")

    file.write("Study area: Faisalabad District, Pakistan\n")
    file.write("Radar band: L-band\n")
    file.write("Frequency: A\n")
    file.write("Polarizations: HH and HV\n")
    file.write("Observations: 30 October and 11 November 2026\n")
    file.write("Projection: EPSG:32643\n")
    file.write("Original pixel spacing: 10 metres\n")
    file.write("Output map aggregation: 100 metres\n\n")

    file.write(
        f"District pixels tested: {district_pixel_count}\n"
    )

    for polarization in ["HH", "HV"]:

        for date in list(PRODUCTS) + ["change"]:

            stat = statistics[(polarization, date)]

            file.write(
                f"\n{polarization} - {date}: "
                f"{stat['count']} valid pixels"
            )

    file.write("\n\nChange maps use common valid pixels only.\n")
    file.write(
        "Backscatter changes are not direct soil-moisture "
        "or crop-health measurements.\n"
    )

print("\n" + "=" * 55)
print("AGRIPULSE PROCESSING COMPLETED!")
print("=" * 55)

print("\nGenerated files:")

for root, folders, files in os.walk(OUTPUT_PATH):
    for filename in files:
        print(os.path.join(root, filename))