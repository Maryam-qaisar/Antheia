document.addEventListener("DOMContentLoaded", function () {

    /* =====================================
       1. DISTRICT STATISTICS
    ===================================== */

    const statisticsTable = document.getElementById("statistics-table");

    fetch("/api/statistics")
        .then(response => {
            if (!response.ok) {
                throw new Error("Could not load statistics.");
            }
            return response.json();
        })
        .then(records => {

            if (!statisticsTable) return;

            statisticsTable.innerHTML = "";

            records.forEach(record => {

                const row = document.createElement("tr");

                const columns = [
                    "Polarization",
                    "Observation",
                    "Valid_Pixels",
                    "Valid_Percent",
                    "Mean_Backscatter_dB",
                    "Minimum_dB",
                    "Maximum_dB"
                ];

                columns.forEach(column => {

                    const cell = document.createElement("td");
                    let value = record[column];

                    if (value === null || value === undefined || value === "") {
                        value = "—";
                    }

                    if (column === "Valid_Pixels" && value !== "—") {
                        value = Number(value).toLocaleString();
                    }

                    if (column === "Valid_Percent" && value !== "—") {
                        value = Number(value).toFixed(2) + "%";
                    }

                    if (
                        [
                            "Mean_Backscatter_dB",
                            "Minimum_dB",
                            "Maximum_dB"
                        ].includes(column) &&
                        value !== "—"
                    ) {
                        value = Number(value).toFixed(2) + " dB";
                    }

                    cell.textContent = value;
                    row.appendChild(cell);

                });

                statisticsTable.appendChild(row);

            });

        })
        .catch(error => {

            console.error("Statistics loading error:", error);

            if (statisticsTable) {
                statisticsTable.innerHTML =
                    '<tr><td colspan="7">Unable to load statistics.</td></tr>';
            }

        });


    /* =====================================
       2. RADAR EXPLORER
    ===================================== */

    const radarSelector = document.getElementById("radar-map");
    const radarImage = document.getElementById("radar-image");

    const interpretationTitle =
        document.getElementById("interpretation-title");

    const interpretationDescription =
        document.getElementById("interpretation-description");

    const interpretationNote =
        document.getElementById("interpretation-note");


    const radarInterpretations = {

        "HH_30_Oct.png": {
            title: "HH Backscatter — 30 October 2026",

            description:
                "This map displays the HH radar backscatter observed on 30 October 2026. HH represents horizontally transmitted and horizontally received radar signals. Its response can be influenced by surface roughness, moisture conditions and vegetation structure.",

            note:
                "This is an observation from a single acquisition. Backscatter values should not be interpreted as direct soil-moisture or crop-health measurements."
        },

        "HH_11_Nov.png": {
            title: "HH Backscatter — 11 November 2026",

            description:
                "This map displays the HH radar backscatter observed on 11 November 2026. Comparing it with the earlier acquisition helps identify spatial differences in the radar response across Faisalabad District.",

            note:
                "Differences may reflect several surface and environmental factors. Additional observations and supporting datasets are required to identify their physical causes."
        },

        "HH_change.png": {
            title: "HH Temporal Change — 12 Days",

            description:
                "This map represents the difference between the 11 November and 30 October HH backscatter observations. Positive values represent an increase in backscatter, while negative values represent a decrease.",

            note:
                "A change in HH backscatter does not independently identify changes in soil moisture, crop condition or land management."
        },

        "HV_30_Oct.png": {
            title: "HV Backscatter — 30 October 2026",

            description:
                "This map displays HV radar backscatter observed on 30 October 2026. HV represents horizontally transmitted and vertically received radar signals. Cross-polarized returns can provide information about volume scattering and vegetation structure.",

            note:
                "HV backscatter is influenced by multiple scattering mechanisms and should not be treated as a direct vegetation-health measurement."
        },

        "HV_11_Nov.png": {
            title: "HV Backscatter — 11 November 2026",

            description:
                "This map displays HV radar backscatter observed on 11 November 2026. It provides a later observation for comparison with the 30 October acquisition.",

            note:
                "Differences between observations may result from vegetation, surface conditions, moisture and other factors. Further evidence is needed for causal interpretation."
        },

        "HV_change.png": {
            title: "HV Temporal Change — 12 Days",

            description:
                "This map shows the difference between HV backscatter observations from 30 October and 11 November 2026. It helps reveal where the cross-polarized radar response increased or decreased across the study area.",

            note:
                "Temporal differences indicate changes in the radar signal. They do not independently establish vegetation growth, crop health or soil moisture."
        }

    };


    function updateRadarExplorer() {

        if (!radarSelector || !radarImage) return;

        const selectedMap = radarSelector.value;

        radarImage.src = "/maps/" + selectedMap;

        const interpretation = radarInterpretations[selectedMap];

        if (!interpretation) return;

        if (interpretationTitle) {
            interpretationTitle.textContent = interpretation.title;
        }

        if (interpretationDescription) {
            interpretationDescription.textContent =
                interpretation.description;
        }

        if (interpretationNote) {
            interpretationNote.textContent = interpretation.note;
        }

    }


    if (radarSelector) {
        radarSelector.addEventListener("change", updateRadarExplorer);
        updateRadarExplorer();
    }


    if (radarImage) {

        radarImage.addEventListener("error", function () {
            console.error("Unable to load radar image:", radarImage.src);
        });

    }


    /* =====================================
       3. TEMPORAL COMPARISON
    ===================================== */

    const comparisonSelector =
        document.getElementById("comparison-polarization");

    const beforeImage =
        document.getElementById("comparison-before");

    const afterImage =
        document.getElementById("comparison-after");


    function updateComparison() {

        if (!comparisonSelector || !beforeImage || !afterImage) return;

        const polarization = comparisonSelector.value;

        beforeImage.src =
            "/maps/" + polarization + "_30_Oct.png";

        afterImage.src =
            "/maps/" + polarization + "_11_Nov.png";

    }


    if (comparisonSelector) {
        comparisonSelector.addEventListener("change", updateComparison);
        updateComparison();
    }


    /* =====================================
       4. INTERACTIVE STUDY AREA MAP
    ===================================== */

    const mapElement = document.getElementById("study-area-map");

    let map = null;

    if (mapElement) {

        if (typeof L === "undefined") {

            console.error("Leaflet library is not loaded.");

        } else if (typeof turf === "undefined") {

            console.error("Turf.js library is not loaded.");

        } else {

            map = L.map("study-area-map");

            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {

                attribution: "&copy; OpenStreetMap contributors",
                maxZoom: 19

            }).addTo(map);


            let studyAreaData = null;


            /* =====================================
               5. LOAD DISTRICT BOUNDARY
            ===================================== */

            fetch("/api/study-area")

                .then(response => {

                    if (!response.ok) {
                        throw new Error("Unable to load district boundary.");
                    }

                    return response.json();

                })

                .then(geojson => {

                    studyAreaData = geojson;

                    const boundaryLayer = L.geoJSON(studyAreaData, {

                        style: {

                            color: "#8b5cf6",
                            weight: 3,
                            fillColor: "#8b5cf6",
                            fillOpacity: 0.15

                        }

                    }).addTo(map);


                    map.fitBounds(boundaryLayer.getBounds());


                    /* DISTRICT AREA */

                    const districtArea = turf.area(studyAreaData) / 1000000;

                    const areaElement =
                        document.getElementById("district-area");

                    if (areaElement) {
                        areaElement.textContent =
                            districtArea.toFixed(2) + " km²";
                    }


                    /* MAP CLICK EVENT */

                    map.on("click", function (event) {

                        if (!studyAreaData) return;

                        const latitude = event.latlng.lat;
                        const longitude = event.latlng.lng;


                        const clickedPoint = turf.point([
                            longitude,
                            latitude
                        ]);


                        const features =
                            studyAreaData.type === "FeatureCollection"
                                ? studyAreaData.features
                                : [studyAreaData];


                        const insideDistrict = features.some(feature => {

                            return turf.booleanPointInPolygon(
                                clickedPoint,
                                feature
                            );

                        });


                        /* DISPLAY SELECTED COORDINATES */

                        const selectedLocation =
                            document.getElementById("selected-location");

                        const latitudeElement =
                            document.getElementById("latitude");

                        const longitudeElement =
                            document.getElementById("longitude");


                        if (latitudeElement) {
                            latitudeElement.textContent = latitude.toFixed(5);
                        }

                        if (longitudeElement) {
                            longitudeElement.textContent = longitude.toFixed(5);
                        }


                        if (selectedLocation) {

                            selectedLocation.textContent = insideDistrict
                                ? "Inside Faisalabad District"
                                : "Outside District Boundary";

                        }


                        const investigationPanel =
                            document.getElementById("location-investigation");


                        if (!insideDistrict) {

                            if (investigationPanel) {
                                investigationPanel.style.display = "none";
                            }

                            return;

                        }


                        /* SHOW RADAR INVESTIGATION */

                        if (investigationPanel) {
                            investigationPanel.style.display = "block";
                        }


                        const statusElement =
                            document.getElementById("location-status");

                        if (statusElement) {
                            statusElement.textContent =
                                "Loading radar observations...";
                        }


                        const gridElement =
                            document.getElementById("grid-location");

                        if (gridElement) {
                            gridElement.textContent =
                                "Retrieving grid information...";
                        }


                        /* RETRIEVE RADAR VALUES */

                        fetch(
                            `/api/location-values?lat=${latitude}&lon=${longitude}`
                        )

                            .then(response => {

                                if (!response.ok) {
                                    throw new Error(
                                        "Unable to retrieve location data."
                                    );
                                }

                                return response.json();

                            })

                            .then(result => {

                                if (result.error) {

                                    if (statusElement) {
                                        statusElement.textContent = result.error;
                                    }

                                    return;

                                }


                                const measurements = result.measurements;


                                function displayValue(value) {

                                    if (
                                        value === null ||
                                        value === undefined ||
                                        !Number.isFinite(Number(value))
                                    ) {
                                        return "Unavailable";
                                    }

                                    return Number(value).toFixed(4) + " dB";

                                }


                                /* HH VALUES */

                                document.getElementById("hh-oct").textContent =
                                    displayValue(measurements.hh_30_oct);

                                document.getElementById("hh-nov").textContent =
                                    displayValue(measurements.hh_11_nov);

                                document.getElementById("hh-change").textContent =
                                    displayValue(measurements.hh_change);


                                /* HV VALUES */

                                document.getElementById("hv-oct").textContent =
                                    displayValue(measurements.hv_30_oct);

                                document.getElementById("hv-nov").textContent =
                                    displayValue(measurements.hv_11_nov);

                                document.getElementById("hv-change").textContent =
                                    displayValue(measurements.hv_change);


                                /* STATUS */

                                if (statusElement) {

                                    statusElement.textContent =
                                        result.status ||
                                        "Radar observations retrieved.";

                                }


                                /* GRID INFORMATION */

                                if (gridElement && result.grid_cell) {

                                    gridElement.textContent =
                                        "Grid cell: Row " +
                                        result.grid_cell.row +
                                        ", Column " +
                                        result.grid_cell.column +
                                        " | Resolution: " +
                                        result.grid_cell.resolution;

                                }

                            })

                            .catch(error => {

                                console.error("Location radar error:", error);

                                if (statusElement) {

                                    statusElement.textContent =
                                        "Unable to retrieve radar observations.";

                                }

                            });

                    });

                })

                .catch(error => {

                    console.error("Study area map error:", error);

                    const selectedLocation =
                        document.getElementById("selected-location");

                    if (selectedLocation) {

                        selectedLocation.textContent =
                            "Unable to load district boundary";

                    }

                });

        }

    }


    /* =====================================
       6. SIDEBAR ACTIVE NAVIGATION
    ===================================== */

    const navigationLinks = document.querySelectorAll(".nav-link");


    navigationLinks.forEach(link => {

        link.addEventListener("click", function () {

            navigationLinks.forEach(item => {
                item.classList.remove("active");
            });

            link.classList.add("active");

        });

    });


    /* =====================================
       7. CINEMATIC EARTH INTRO
    ===================================== */

    const introScreen = document.getElementById("intro-screen");
    const skipButton = document.getElementById("intro-skip");

    let introFinished = false;
    let introTimer = null;


    function finishIntro() {

        if (introFinished) return;

        introFinished = true;

        if (introTimer) {
            clearTimeout(introTimer);
        }

        if (!introScreen) {
            document.body.classList.remove("intro-active");
            document.body.classList.add("intro-finished");
            return;
        }


        introScreen.classList.add("launching");


        setTimeout(function () {

            introScreen.classList.add("is-hidden");

            document.body.classList.remove("intro-active");
            document.body.classList.add("intro-finished");


            /*
             * Leaflet needs a resize event after the
             * dashboard becomes visible.
             */

            setTimeout(function () {

                window.dispatchEvent(new Event("resize"));

            }, 250);


            window.dispatchEvent(
                new Event("antheia-dashboard-revealed")
            );

        }, 1350);

    }


    if (introScreen) {

        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {

            finishIntro();

        } else {

            introTimer = setTimeout(function () {

                finishIntro();

            }, 3900);

        }

    } else {

        document.body.classList.remove("intro-active");

    }


    if (skipButton) {

        skipButton.addEventListener("click", function () {

            finishIntro();

        });

    }
    /* =====================================
       8. ANTHEIA SCIENCE DESK
    ===================================== */

    const scienceQuestion =
        document.getElementById("science-question");

    const scienceAnswerTitle =
        document.getElementById("science-answer-title");

    const scienceAnswerText =
        document.getElementById("science-answer-text");


    // Predefined scientific questions and answers

    const scienceAnswers = {

        "project": {

            title: "What is Antheia investigating?",

            answer:
                "Antheia explores spatial and temporal variations in NASA-ISRO NISAR L-band HH and HV radar backscatter across Faisalabad District. It compares observations from 30 October and 11 November 2026, a 12-day interval."

        },


        "hh-hv": {

            title: "What do HH and HV mean?",

            answer:
                "HH means the radar signal is transmitted horizontally and received horizontally. It is co-polarized. HV means the signal is transmitted horizontally and received vertically. It is cross-polarized. The two channels provide complementary information about how the surface scatters radar energy."

        },


        "lband": {

            title: "What is L-band radar?",

            answer:
                "L-band is a microwave radar frequency band with a relatively long wavelength. It can interact with vegetation and the ground surface, but the measured response depends on several factors, including surface structure, moisture, geometry and vegetation."

        },


        "backscatter": {

            title: "What is radar backscatter?",

            answer:
                "Backscatter is the portion of the transmitted radar energy that is scattered back toward the satellite. Its strength is influenced by the properties and arrangement of the surface. Antheia displays the processed backscatter values in decibels (dB)."

        },


        "decibels": {

            title: "What does a negative dB value mean?",

            answer:
                "A negative backscatter value is common when radar power is expressed on a logarithmic decibel scale. It does not mean negative soil moisture or a negative amount of vegetation. Interpret it as a radar signal measurement, and compare values using the same processing and units."

        },


        "change": {

            title: "How should I understand temporal change?",

            answer:
                "Temporal change is the later backscatter value minus the earlier value. A positive result means the radar backscatter increased; a negative result means it decreased. This identifies a change in the radar response, not the exact physical reason for that change."

        },


        "valid-pixels": {

            title: "Why compare common valid pixels?",

            answer:
                "A temporal comparison is more consistent when it uses pixels that contain valid observations in both dates. Common-valid-pixel comparison avoids treating a pixel as a change when one of its observations is missing or invalid. Quality masking also helps exclude pixels marked as unreliable."

        },


        "nisar": {

            title: "What is NISAR?",

            answer:
                "NISAR is the NASA-ISRO Synthetic Aperture Radar mission. It uses radar observations to study changes and characteristics of Earth's land and ice surfaces. Antheia uses the supplied NISAR Level-2 GCOV L-band observations for this Faisalabad study."

        },


        "limitations": {

            title: "Can these values tell us crop health or soil moisture?",

            answer:
                "Not by themselves. Radar backscatter can be affected by soil moisture, surface roughness, vegetation structure and other conditions. Antheia identifies radar-signal patterns and changes; confirming crop health or soil moisture requires supporting datasets, suitable models and/or field validation."

        }

    };


    // Update the displayed answer when a question is selected

    function updateScienceAnswer() {

        if (
            !scienceQuestion ||
            !scienceAnswerTitle ||
            !scienceAnswerText
        ) {
            return;
        }

        const selectedAnswer =
            scienceAnswers[scienceQuestion.value];

        if (!selectedAnswer) {
            return;
        }

        scienceAnswerTitle.textContent =
            selectedAnswer.title;

        scienceAnswerText.textContent =
            selectedAnswer.answer;

    }


    // Listen for question selection

    if (scienceQuestion) {

        scienceQuestion.addEventListener(
            "change",
            updateScienceAnswer
        );

        // Display the first answer when the page loads

        updateScienceAnswer();

    }

});