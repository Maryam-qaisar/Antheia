AgriPulse

Satellite-Based Agricultural Radar Monitoring for Faisalabad District, Pakistan

NASA Space Apps Challenge 2026

AgriPulse is a satellite-based agricultural radar monitoring platform developed using NASA-ISRO Synthetic Aperture Radar (NISAR) Level-2 Geocoded Covariance Matrix (GCOV) data. The project analyses radar backscatter observations over Faisalabad District, Pakistan, to identify spatial patterns and changes between satellite acquisitions.

The platform combines satellite data processing, geospatial analysis, statistical summaries and an interactive web dashboard to make radar observations easier to explore and interpret.

⸻

1. Project Overview

Agriculture is an important part of Pakistan’s economy. Monitoring agricultural landscapes over large areas can be challenging, particularly when conventional optical satellite imagery is affected by cloud cover.

AgriPulse demonstrates how synthetic aperture radar (SAR) observations can help monitor changes in agricultural landscapes. Unlike optical sensors, radar can collect observations through cloud cover and during both daytime and nighttime.

The project uses two NISAR observations to compare radar backscatter over Faisalabad District and presents the results through spatial maps and district-level statistics.

Project Objectives

* Analyse NISAR L-band radar observations over Faisalabad District.
* Process HH and HV radar polarization data.
* Generate spatial backscatter maps for two acquisition dates.
* Identify temporal changes in radar backscatter.
* Calculate district-level statistical summaries.
* Present the results through an accessible web dashboard.
* Demonstrate the potential of satellite radar observations for agricultural monitoring.

2. Study Area

Location: Faisalabad District, Punjab, Pakistan.

The project uses a district boundary GeoJSON file to define the geographical study area. Satellite observations are cropped and analysed within this boundary.

The processing grid uses the WGS 84 / UTM Zone 43N projected coordinate reference system (EPSG:32643), with a source pixel spacing of approximately 10 metres.

3. Satellite Data

AgriPulse uses NASA-ISRO NISAR Level-2 GCOV observations.

NISAR is a joint mission of NASA and the Indian Space Research Organisation (ISRO). It uses synthetic aperture radar technology to observe changes in Earth’s surface.

Acquisition details

Parameter	Observation 1	Observation 2
Acquisition date	30 October 2026	11 November 2026
Scene identifier	034_084_A_017	035_084_A_017
Orbit direction	Ascending	Ascending
Track	84	84
Frame	17	17
Absolute orbit	6584	6757
Frequency	A	A
Radar band	L-band	L-band
Polarizations	HH, HV	HH, HV

Observation interval: 12 days.

Both observations cover the Faisalabad District study area and use compatible spatial grids, supporting pixel-based temporal comparison.

Radar Polarizations

The project processes two polarization channels:

* HH: Horizontal transmission and horizontal reception.
* HV: Horizontal transmission and vertical reception.

These channels provide different information about radar scattering characteristics.

4. Methodology

AgriPulse follows a satellite data processing and analysis workflow.

Step 1 — Data acquisition

The required NISAR Level-2 GCOV products are obtained from the NASA Alaska Satellite Facility Distributed Active Archive Center (ASF DAAC).

Step 2 — Data inspection

The HDF5 products are inspected to identify the required datasets, including HH and HV covariance terms, geolocation information, coordinate grids and quality masks.

Step 3 — Study area extraction

The Faisalabad District boundary is loaded from GeoJSON and transformed into the satellite products’ projected coordinate reference system.

The corresponding satellite data region is extracted using the district boundary.

Step 4 — Quality filtering

Satellite data are screened using the available quality masks, valid subswath information and numerical validity checks.

Invalid, missing and non-positive observations are excluded from the backscatter calculations.

Step 5 — Backscatter conversion

Valid linear radar backscatter values are converted into decibels using:

Backscatter (dB) = 10 × log10(linear backscatter)

Step 6 — Temporal comparison

The two acquisition dates are compared using the corresponding HH and HV observations.

Change is calculated as:

Change (dB) = Backscatter on 11 November − Backscatter on 30 October

Negative values indicate a decrease in radar backscatter, while positive values indicate an increase.

Step 7 — Statistical analysis

District-level statistics are calculated, including:

* Number of valid pixels.
* Valid pixel coverage percentage.
* Mean backscatter.
* Minimum backscatter.
* Maximum backscatter.

Step 8 — Visualization

The processed observations and temporal differences are converted into maps and displayed through the AgriPulse web dashboard.

5. Project Results

The two NISAR observations were successfully processed over Faisalabad District.

Observed backscatter statistics

Measurement	HH	HV
Mean — 30 October	-10.64 dB	-17.18 dB
Mean — 11 November	-11.09 dB	-17.55 dB
Mean temporal change	-0.43 dB	-0.35 dB
Median temporal change	-0.212 dB	-0.170 dB

The median temporal changes are based on the processed spatial comparison.

The results show spatial variation in radar backscatter between the two acquisition dates. The generated change maps allow users to explore where increases and decreases occurred across the district.

Data coverage

Observation	Valid pixel coverage
30 October 2026	Approximately 94.62%
11 November 2026	Approximately 96.76%

The temporal comparison uses common valid pixels from both acquisitions.

6. AgriPulse Dashboard

AgriPulse includes an interactive web dashboard developed using Flask, HTML, CSS and JavaScript.

The dashboard provides the following sections:

Overview

* Project introduction.
* Key radar change indicators.
* Study area information.
* Observation interval.

Radar Explorer

* HH backscatter map.
* HV backscatter map.
* Acquisition-date selection.

Temporal Comparison

* HH temporal change map.
* HV temporal change map.
* Explanation of positive and negative changes.

District Insights

* Valid pixel counts.
* Coverage percentages.
* Mean, minimum and maximum backscatter statistics.

Methodology

* Satellite data source.
* Radar processing information.
* Spatial and temporal analysis workflow.

7. Technologies Used

Technology	Application
Python	Main processing language
NumPy	Numerical calculations
h5py	Reading NISAR HDF5 products
Shapely	Geospatial boundary operations
PyProj	Coordinate transformations
Matplotlib	Radar map generation
Flask	Web application backend
HTML	Dashboard structure
CSS	Dashboard styling
JavaScript	Dashboard interactions
GeoJSON	Study area boundary representation

8. Repository Structure

AgriPulse/
│
├── acquisition/
│   ├── inspect_nisar.py
│   └── search_nisar.py
│
├── analysis/
│
├── config/
│
├── dashboard/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── dashboard.js
│
├── data/
│   ├── raw/
│   │   ├── product_2/
│   │   └── product_6/
│   └── reference/
│       └── faisalabad_district.geojson
│
├── outputs/
│   ├── data/
│   ├── maps/
│   ├── reports/
│   ├── district_statistics.csv
│   └── processing_summary.txt
│
├── processing/
│
├── requirements.txt
├── .gitignore
└── README.md

The repository may contain additional scripts and configuration files as the project evolves.

9. Installation and Setup

Prerequisites

* Python 3.11 recommended.
* Git.
* Visual Studio Code or another Python-compatible editor.
* Internet access for installing dependencies and obtaining satellite data.

Step 1 — Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

Step 2 — Enter the project directory

cd AgriPulse

Step 3 — Create a virtual environment

python -m venv venv

Step 4 — Activate the environment

Windows PowerShell:

venv\Scripts\activate

macOS / Linux:

source venv/bin/activate

Step 5 — Install dependencies

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

All required Python packages listed in requirements.txt will be installed.

10. Satellite Data Preparation

The original NISAR satellite products are not included in this GitHub repository because the HDF5 files are large.

Users must obtain the corresponding NISAR Level-2 GCOV products through the NASA Alaska Satellite Facility (ASF DAAC).

Data access resources:

* NASA NISAR: https://nisar.jpl.nasa.gov/
* ASF DAAC: https://asf.alaska.edu/
* NASA Earthdata: https://www.earthdata.nasa.gov/

Obtain the two acquisitions described in the Satellite Data section, ensuring that the correct scene identifiers, frequency and polarizations are selected.

Place the downloaded HDF5 products in the expected project directories:

data/
└── raw/
    ├── product_2/
    │   └── NISAR_HDF5_PRODUCT
    │
    └── product_6/
        └── NISAR_HDF5_PRODUCT

The Faisalabad District GeoJSON boundary should be placed in:

data/reference/faisalabad_district.geojson

Note: The original satellite files must be obtained separately. Access to NASA Earthdata services and any applicable data-access requirements may be necessary.

11. Running the Processing Workflow

After obtaining the satellite products and preparing the required directories:

1. Activate the Python virtual environment.
2. Place the two NISAR HDF5 products in their respective directories under `data/raw/`.
3. Ensure the Faisalabad District GeoJSON boundary is available in `data/reference/`.
4. Run the main processing script from the root AgriPulse directory:

```bash
python process_nisar.py
```

The script processes the satellite observations and generates the radar maps, district statistics and processing summary in the `outputs/` directory.

Expected outputs include:

- HH backscatter maps for both acquisition dates.
- HV backscatter maps for both acquisition dates.
- HH and HV temporal change maps.
- District-level statistics CSV.
- Processing summary report.
- Processed numerical data in NPZ format.

12. Launching the Dashboard

After the required processing outputs have been generated:

Run the Flask application from the main project directory:

python dashboard/app.py

Open the following address in a web browser:

http://127.0.0.1:5000

The dashboard reads the generated maps and district statistics from the project’s outputs directory.

13. Understanding the Results

Radar backscatter represents the portion of transmitted radar energy scattered back toward the satellite.

Changes in backscatter can be influenced by several factors, including:

* Surface moisture conditions.
* Vegetation structure.
* Surface roughness.
* Land management activities.
* Acquisition and measurement conditions.

Positive changes indicate an increase in measured backscatter, while negative changes indicate a decrease.

Scientific limitation: Changes in radar backscatter alone cannot establish crop health, identify a specific crop condition, directly measure soil moisture or confirm irrigation events. These interpretations require additional datasets and validation.

AgriPulse should therefore be understood as a radar-based monitoring and exploratory analysis platform rather than a standalone agricultural diagnostic system.

14. Future Development

Potential future improvements include:

* Integration of additional NISAR observations.
* Longer-term temporal analysis.
* Integration of optical satellite imagery.
* Comparison with rainfall and weather observations.
* Integration of field-based agricultural measurements.
* More detailed land-cover and crop-specific analysis.
* Automated monitoring and reporting.

15. Acknowledgements and Data Sources

AgriPulse uses satellite observations from the NASA-ISRO NISAR mission.

We acknowledge:

* NASA — National Aeronautics and Space Administration.
* ISRO — Indian Space Research Organisation.
* ASF DAAC — Alaska Satellite Facility Distributed Active Archive Center.
* NASA Earthdata — Satellite data access and distribution resources.

The project was developed as part of the NASA Space Apps Challenge 2026.

⸻

AgriPulse — Turning Satellite Radar Observations into Accessible Agricultural Insights.