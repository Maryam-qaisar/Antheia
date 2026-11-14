document.addEventListener("DOMContentLoaded", function () {
    // Load statistics from the Flask backend
    fetch("/api/statistics")
        .then(response => {
            if (!response.ok) {
                throw new Error("Could not load statistics");
            }
            return response.json();
        })
        .then(records => {
            const table = document.getElementById("statistics-table");

            if (!table) return;

            table.innerHTML = "";

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
                    let value = record[column] ?? "—";

                    if (column === "Valid_Pixels") {
                        value = Number(value).toLocaleString();
                    }

                    if (column === "Valid_Percent") {
                        value = Number(value).toFixed(2) + "%";
                    }

                    if (
                        column === "Mean_Backscatter_dB" ||
                        column === "Minimum_dB" ||
                        column === "Maximum_dB"
                    ) {
                        value = Number(value).toFixed(2) + " dB";
                    }

                    cell.textContent = value;
                    row.appendChild(cell);
                });

                table.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Statistics loading error:", error);
        });

    // Change the radar map when a different option is selected
    const mapSelector = document.getElementById("radar-map");
    const radarImage = document.getElementById("radar-image");

    if (mapSelector && radarImage) {
        mapSelector.addEventListener("change", function () {
            const allowedMaps = [
                "HH_30_Oct.png",
                "HH_11_Nov.png",
                "HH_change.png",
                "HV_30_Oct.png",
                "HV_11_Nov.png",
                "HV_change.png"
            ];

            if (allowedMaps.includes(mapSelector.value)) {
                radarImage.src = "/maps/" + mapSelector.value;
            }
        });
    }
});