# 🌍 ANTHEIA — Satellite Intelligence for Agricultural Monitoring

### An Earth Observation and Agricultural Radar Monitoring Platform

**Developed by:** ORBIT IQ  
**Project:** Antheia  
**Study Area:** Faisalabad District, Punjab, Pakistan  
**Primary Data Source:** NASA–ISRO NISAR Mission  
**Radar Frequency:** L-Band  
**Polarizations:** HH and HV  

---

## 1. Project Overview

**Antheia** is a satellite-based agricultural monitoring and Earth observation platform designed to explore spatial and temporal variations in radar backscatter across Faisalabad District, Pakistan.

The project uses observations from the **NASA–ISRO Synthetic Aperture Radar (NISAR)** mission to investigate how radar signals change across different geographical locations and observation periods.

Unlike conventional optical satellite imagery, radar-based Earth observation allows the analysis of surface characteristics using microwave signals. This makes Synthetic Aperture Radar (SAR) particularly useful for studying land surfaces and vegetation under different environmental conditions.

Antheia transforms processed satellite observations into an interactive dashboard where users can:

- Explore geographical boundaries and locations.
- Visualize HH and HV radar backscatter observations.
- Compare satellite observations across different dates.
- Investigate temporal backscatter differences.
- Examine district-level statistical measurements.
- Retrieve radar values for selected geographical locations.
- Understand the scientific principles behind radar observations through an integrated Science Desk.

The platform combines satellite data processing, geospatial analysis, scientific interpretation, and interactive web technologies into one centralized monitoring environment.

## 2. Project Objectives

The primary objectives of Antheia are:

1. To explore the application of Synthetic Aperture Radar in agricultural and geographical monitoring.
2. To process and visualize NASA–ISRO NISAR Level-2 GCOV observations.
3. To compare HH and HV polarization measurements across different observation dates.
4. To identify spatial and temporal variations in radar backscatter.
5. To investigate radar observations at selected geographical locations.
6. To implement geographical extraction and statistical analysis within a defined study area.
7. To provide an accessible interface for understanding satellite-based scientific observations.
8. To demonstrate how Earth observation data can be integrated into an interactive web-based analytical platform.

## 3. Key Features

### 3.1 Interactive Overview Dashboard

The Overview section provides a centralized summary of the current study.

It displays important project measurements, including:

- HH median backscatter change.
- HV median backscatter change.
- Radar frequency band.
- Observation interval.

Current study results:

| Measurement | Reported Value |
|---|---:|
| HH Median Change | -0.212 dB |
| HV Median Change | -0.170 dB |
| Radar Frequency | L-Band |
| Observation Interval | 12 Days |

The displayed comparison covers observations from 30 October 2026 and 11 November 2026.

### 3.2 Interactive Study Area Map

Antheia incorporates an interactive geographical map focused on Faisalabad District.

Users can explore the district boundary and select geographical locations to investigate their corresponding radar observations.

The map functionality includes:

- Interactive geographical navigation.
- District boundary visualization.
- Location selection through map interaction.
- Latitude and longitude retrieval.
- District area calculation.
- Geographical boundary validation.

The system uses the selected coordinates to determine whether a location falls within the Faisalabad District boundary.

When a valid location is selected, the platform retrieves its associated radar measurements.

### 3.3 Location-Based Radar Investigation

The Location Radar Investigation feature allows users to examine radar observations at individual geographical locations.

After selecting a location inside the district boundary, Antheia retrieves the available measurements for:

**HH Polarization**
- 30 October observation.
- 11 November observation.
- Temporal difference.

**HV Polarization**
- 30 October observation.
- 11 November observation.
- Temporal difference.

The platform also displays the corresponding radar grid-cell information when available.

This functionality connects geographical exploration with underlying satellite measurements.

### 3.4 Radar Explorer

The Radar Explorer provides visual access to processed radar backscatter observations.

Users can select between six visualization options:

| Polarization | Observation |
|---|---|
| HH | 30 October 2026 |
| HH | 11 November 2026 |
| HH | Temporal Change |
| HV | 30 October 2026 |
| HV | 11 November 2026 |
| HV | Temporal Change |

The selected visualization is dynamically displayed within the dashboard.

The feature also provides scientific explanations describing the selected polarization, observation period, and relevant interpretation considerations.

### 3.5 Temporal Comparison

The Temporal Comparison section allows users to compare radar observations from two different acquisition dates.

Users can switch between:

- HH Polarization.
- HV Polarization.

The dashboard dynamically updates the corresponding earlier and later radar images.

This feature helps investigate temporal variations in radar backscatter across the study area.

A negative difference represents a decrease in the later radar backscatter value relative to the earlier observation, while a positive difference represents an increase.

### 3.6 District Insights and Statistical Analysis

The District Insights section presents statistical measurements generated from the processed radar observations.

The dashboard retrieves statistical records from the Flask backend and dynamically populates the results table.

The displayed parameters include:

- Polarization.
- Observation date.
- Number of valid pixels.
- Valid pixel coverage percentage.
- Mean backscatter in dB.
- Minimum backscatter in dB.
- Maximum backscatter in dB.

These measurements provide a numerical overview of the processed satellite observations across Faisalabad District.

### 3.7 Methodology Section

The Methodology section explains the technical workflow behind Antheia.

It presents four major stages:

**01 — Data Source**

NASA–ISRO NISAR Level-2 GCOV satellite observations.

**02 — Radar Processing**

Frequency A HH/HV backscatter observations, quality masking, and conversion into decibel measurements.

**03 — Spatial Analysis**

Faisalabad District polygon extraction and spatial aggregation.

**04 — Temporal Analysis**

Comparison of observations from 30 October and 11 November 2026 using common valid pixels.

### 3.8 Antheia Science Desk

The Science Desk is an integrated educational and scientific interpretation module introduced to make Antheia more than a conventional satellite visualization dashboard.

It helps users understand the scientific concepts, radar measurements, and analytical decisions behind the project.

#### Interactive Scientific Question and Answer System

Users can select questions from a dropdown menu and receive predefined explanations.

The available topics include:

1. What is Antheia investigating?
2. What do HH and HV mean?
3. What is L-band radar?
4. What is radar backscatter?
5. What does a negative dB value mean?
6. How should temporal change be understood?
7. Why compare common valid pixels?
8. What is NISAR?
9. Can radar values independently establish crop health or soil moisture?

The answers are dynamically updated using JavaScript without requiring a separate backend request.

#### Project Conclusion

The Science Desk presents the current study's reported median backscatter changes:

- HH: -0.212 dB
- HV: -0.170 dB

It explains what these differences indicate and clarifies what cannot be concluded from the measurements alone.

#### Scientific Investigation Board

The Investigation Board organizes the project's analytical work into three investigations.

**Investigation 01 — Temporal Backscatter Analysis**

Research question: Did the radar response change between the two acquisitions?

Approach:
- Compare HH and HV observations.
- Examine the two acquisition dates.
- Investigate temporal difference maps.
- Review district-level statistics.

**Investigation 02 — Polarization Comparison**

Research question: Do HH and HV provide different views of the surface?

Approach:
- Examine co-polarized HH observations.
- Examine cross-polarized HV observations.
- Compare their temporal responses.
- Understand their complementary scattering information.

**Investigation 03 — Spatial Data Reliability**

Research question: How does Antheia make the comparison more consistent?

Approach:
- Apply quality masking.
- Extract the Faisalabad District boundary.
- Compare observations using common valid pixels.
- Restrict the analysis to the defined study area.

The Science Desk therefore connects the technical processing workflow with the scientific questions the project investigates.

---

## 4. Technology Stack

Antheia uses a combination of Python-based backend development, web technologies, and geospatial visualization tools.

| Technology | Application |
|---|---|
| Python | Backend development and data processing |
| Flask | Web application framework |
| HTML5 | Dashboard structure |
| CSS3 | Dashboard design and responsive layouts |
| JavaScript | Interactive dashboard functionality |
| Leaflet.js | Interactive geographical mapping |
| Turf.js | Geospatial calculations and point-in-polygon analysis |
| GeoJSON | Geographical boundary representation |
| CSV | Statistical data exchange |
| NASA–ISRO NISAR | Satellite observation source |

### Frontend

The frontend is developed using HTML, CSS, and JavaScript.

It provides the user interface, navigation, interactive radar visualizations, geographical map, scientific explanations, and responsive dashboard components.

### Backend

The application uses Flask to serve the dashboard and provide data through backend routes.

The JavaScript frontend communicates with the Flask application through HTTP requests to retrieve statistical, geographical, and location-specific information.

### Geospatial Visualization

Leaflet.js is used to display the interactive study area map.

Turf.js supports geographical calculations, including district area estimation and checking whether selected coordinates fall inside the district boundary.

---

## 5. System Architecture

Antheia follows a Python Flask-based web application architecture.

The major components are:

**1. Satellite Data Layer**

Contains the NISAR observations used in the study.

**2. Data Processing Layer**

Processes radar observations, performs quality masking, extracts the study area, and generates the outputs required by the dashboard.

**3. Backend Layer**

The Flask application serves the dashboard and exposes the data retrieval endpoints.

**4. Frontend Layer**

HTML, CSS, and JavaScript provide the interactive interface.

**5. Visualization and Analysis Layer**

Displays radar images, geographical information, temporal comparisons, and statistical results.

**6. Science Desk Layer**

Provides predefined scientific explanations and organizes the project's investigations and conclusions.

### Application Data Flow

```text
NASA–ISRO NISAR Observations
              |
              v
      Radar Data Processing
              |
              v
       Quality Masking
              |
              v
     Spatial Data Extraction
              |
              v
     Temporal Comparison
              |
              v
       Processed Outputs
              |
              v
       Python Flask Backend
              |
              v
       Interactive Dashboard
              |
       +------+------+
       |             |
       v             v
 Radar Analysis   Geospatial
 and Statistics   Investigation
       |             |
       +------+------+
              |
              v
       Antheia Science Desk
```

---

## 6. Project Directory Structure

The main application structure is organized as follows:

```text
Antheia/
│
├── dashboard/
│   │
│   ├── app.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       │
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── dashboard.js
│
├── process_nisar.py
│
├── maps/
│   ├── HH_30_Oct.png
│   ├── HH_11_Nov.png
│   ├── HH_change.png
│   ├── HV_30_Oct.png
│   ├── HV_11_Nov.png
│   └── HV_change.png
│
└── README.md
```

*Note: The directory tree illustrates the principal application files and expected visualization outputs. Additional data files, configuration files, and processing outputs may exist in the complete repository.*

---

## 7. Backend API Endpoints

The frontend communicates with the Flask backend through the following application endpoints.

| Endpoint | Purpose |
|---|---|
| `/api/statistics` | Retrieves district-level statistical records |
| `/api/study-area` | Retrieves the study area geographical boundary |
| `/api/location-values` | Retrieves radar measurements for selected coordinates |
| `/maps/` | Serves processed radar visualization images |

### Location Investigation Request

The location investigation functionality sends the selected geographical coordinates to the backend.

Example request:

```text
/api/location-values?lat=31.4504&lon=73.1350
```

The frontend uses the returned measurements to display the HH and HV values for the selected location.

The exact availability of a measurement depends on the underlying processed data.

---

## 8. Scientific Methodology

Antheia investigates changes in radar backscatter using two NISAR observation dates.

### 8.1 Radar Backscatter

Radar backscatter represents the portion of transmitted microwave energy scattered back toward the satellite.

Its measured strength can be influenced by:

- Surface roughness.
- Soil moisture conditions.
- Vegetation structure.
- Surface geometry.
- Radar acquisition conditions.

The dashboard displays processed backscatter values in decibels (dB).

### 8.2 Polarization

The project uses two radar polarization channels.

**HH — Horizontal-Horizontal**

The radar signal is transmitted horizontally and received horizontally.

HH is a co-polarized measurement.

**HV — Horizontal-Vertical**

The radar signal is transmitted horizontally and received vertically.

HV is a cross-polarized measurement.

Both channels provide complementary information about the scattering characteristics of the observed surface.

### 8.3 Temporal Backscatter Difference

The project compares two observation dates:

- Earlier observation: 30 October 2026.
- Later observation: 11 November 2026.

The temporal difference is calculated as:

```text
Change = Later Observation - Earlier Observation
```

A negative result indicates a decrease in backscatter between the observations.

A positive result indicates an increase.

### 8.4 Common Valid Pixels

For a more consistent temporal comparison, the project uses common valid pixels.

These are pixels containing valid observations in both acquisition periods.

This approach helps prevent invalid or missing observations from being treated as meaningful temporal changes.

Quality masking also helps exclude observations identified as unreliable.

---

## 9. Project Findings

The current dashboard reports the following district-level median changes:

| Polarization | Median Change |
|---|---:|
| HH | -0.212 dB |
| HV | -0.170 dB |

Both reported median changes are negative.

This indicates that the later observation has a lower median backscatter value than the earlier observation for the reported comparisons.

These findings demonstrate the platform's ability to process, compare, and visualize temporal radar observations.

### Scientific Limitations

Radar backscatter differences alone cannot establish:

- A definite decrease in soil moisture.
- A decline in crop health.
- A specific vegetation change.
- The exact physical cause of a radar signal difference.

Backscatter is affected by multiple interacting surface and environmental factors.

Further datasets, appropriate analytical models, and field observations would be necessary to investigate specific agricultural conditions.

Antheia therefore presents radar-derived observations and analytical insights rather than claiming independently verified crop-health or soil-moisture measurements.

---

## 10. Installation and Execution

### Prerequisites

Before running Antheia, ensure that you have:

- Python installed.
- Visual Studio Code or another code editor.
- Git installed.
- Access to the complete Antheia project directory.
- The project's required Python packages.

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Maryam-qaisar/Antheia
```

### Step 2 — Navigate to the Project

```bash
cd Antheia
```

### Step 3 — Install Dependencies

If your repository contains a `requirements.txt` file, install the listed dependencies:

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Flask Application

From the project root directory:

```bash
python dashboard/app.py
```

### Step 5 — Open the Dashboard

Visit the following address in your browser:

```text
http://127.0.0.1:5000
```

The Antheia dashboard should now be accessible locally.

*Note: The processed radar outputs and required geographical and statistical data must also be available in their expected locations for the corresponding dashboard features to work.*

---

## 11. User Interaction Workflow

A typical Antheia user workflow is:

1. Open the application and view the introductory Earth animation.
2. Explore the Overview section and examine the district-level measurements.
3. Navigate to the Interactive Study Area.
4. Select a geographical location within Faisalabad District.
5. Examine the retrieved HH and HV radar measurements.
6. Open the Radar Explorer to inspect individual observations.
7. Use Temporal Comparison to investigate differences between dates.
8. Review District Insights for statistical measurements.
9. Explore the Methodology section to understand the processing workflow.
10. Visit the Science Desk to understand the scientific concepts and project findings.

---

## 12. Future Development Opportunities

Antheia provides a foundation for further development in satellite-based agricultural monitoring.

Potential future improvements include:

- Integration of additional NISAR acquisition dates.
- Long-term temporal backscatter monitoring.
- Integration of optical satellite datasets.
- Vegetation index analysis using complementary satellite observations.
- Soil-moisture estimation using appropriate validated methodologies.
- Advanced spatial and temporal anomaly detection.
- Machine learning-based classification experiments.
- Improved location-based analytical reporting.
- Automated generation of scientific observation summaries.
- AI-assisted explanations of satellite-derived measurements.

These improvements could expand the platform from a two-date radar investigation into a more comprehensive Earth observation and agricultural analysis system.

---

## 13. Project Significance

Antheia demonstrates how satellite Earth observation data can be transformed into an accessible analytical environment.

The project brings together:

- Remote sensing.
- Synthetic Aperture Radar.
- Geospatial analysis.
- Temporal data comparison.
- Statistical processing.
- Interactive web development.
- Scientific communication.

By combining these components, Antheia provides an interactive environment for exploring how radar observations can support geographical and agricultural investigations.

The addition of the Science Desk further improves the platform by connecting technical outputs with scientific concepts, interpretations, and limitations.

---

## 14. Acknowledgements

The project uses observations from the **NASA–ISRO Synthetic Aperture Radar (NISAR)** mission.

The project acknowledges the work of the NASA and ISRO teams involved in developing and operating the mission and making its Earth observation data available.

Technologies and libraries used include Python, Flask, Leaflet.js, Turf.js, HTML5, CSS3, and JavaScript.

---



## 15. About ORBIT IQ

**Antheia — Satellite Intelligence for Agricultural Monitoring**

Developed by **ORBIT IQ**.

A scientific prototype exploring the use of NISAR L-band radar observations for spatial and temporal analysis across Faisalabad District, Pakistan.

**Observe. Analyze. Understand.**
