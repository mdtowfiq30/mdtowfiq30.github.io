document.addEventListener("DOMContentLoaded", function () {
    // Accident data for each month
    const monthData = {
        january: [
            { x: 800, y: 100, type: "foot", name: "Shakil", id: "12345", accident: "👣" },
            { x: 400, y: 150, type: "hand", name: "Michael Smith", id: "54321", accident: "Hand Injury ✋" }
        ],
        february: [
            { x: 750, y: 310, type: "foot", name: "Shakil Ahammod", id: "26086005", accident: "👣"},
            { x: 300, y: 200, type: "hand", name: "Jane Smith", id: "67890", accident: "Hand Injury ✋" },
            { x: 590, y: 310, type: "foot", name: "Md. Ibrahim", id: "26086006", accident: "👣" }
        ],
        march: [
            { x: 700, y: 250, type: "eye", name: "Sarah Lee", id: "33567", accident: "Eye Injury 👁️" },
            { x: 600, y: 400, type: "hand", name: "David Clark", id: "78901", accident: "Hand Injury ✋" }
        ],
    };

    // Track selected month
    let selectedMonth = "january"; // default selection
    let heatmapVisible = false;
    let allAccidentData = []; // Store all data points for the heatmap

    // Event listener for selecting a month
    document.getElementById("month").addEventListener("change", function () {
        selectedMonth = document.getElementById("month").value;
        const accidentData = monthData[selectedMonth];

        if (!accidentData || accidentData.length === 0) {
            alert("No data available for " + selectedMonth);
            return;
        }

        // Clear previous markers and tooltips
        clearMarkersAndTooltips();

        // Display markers for the selected month
        displayMarkers(accidentData);
    });

    // Event listener for toggling the heatmap
    document.getElementById("toggleHeatmap").addEventListener("click", function () {
        const accidentData = monthData[selectedMonth];

        if (!accidentData || accidentData.length === 0) {
            alert("No data available for " + selectedMonth);
            return;
        }

        // Clear previous markers and tooltips before showing the heatmap
        clearMarkersAndTooltips();

        // Toggle heatmap visibility and update data
        if (!heatmapVisible) {
            heatmapVisible = true;

            // Aggregate all data points across all months for the heatmap
            allAccidentData = [];
            for (let month in monthData) {
                allAccidentData = [...allAccidentData, ...monthData[month]];
            }

            // Generate the heatmap with the aggregated data
            generateHeatmap(allAccidentData);
        } else {
            heatmapVisible = false;

            // Remove heatmap canvas
            const heatmapCanvas = document.querySelector(".heatmap-canvas");
            if (heatmapCanvas) {
                heatmapCanvas.remove();
            }

            // After turning off the heatmap, display only the markers for the selected month
            const currentMonthData = monthData[selectedMonth];
            displayMarkers(currentMonthData);
        }
    });

    // Function to clear markers and tooltips
    function clearMarkersAndTooltips() {
        const imageContainer = document.querySelector(".image-container");
        const existingMarkers = imageContainer.querySelectorAll(".marker");
        const existingTooltips = imageContainer.querySelectorAll(".tooltip");

        // Remove all markers and tooltips
        existingMarkers.forEach(marker => marker.remove());
        existingTooltips.forEach(tooltip => tooltip.remove());
    }

    // Function to generate the heatmap
    function generateHeatmap(accidentData) {
        const imageContainer = document.querySelector(".image-container");
        const containerWidth = imageContainer.clientWidth;
        const containerHeight = imageContainer.clientHeight;

        const canvas = document.createElement("canvas");
        canvas.width = containerWidth;
        canvas.height = containerHeight;
        canvas.classList.add("heatmap-canvas");
        imageContainer.appendChild(canvas);

        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        accidentData.forEach(accident => {
            drawHeatSpot(ctx, accident.x, accident.y);
        });
    }

    // Function to draw a heat spot (radial gradient) at the given coordinates
    function drawHeatSpot(ctx, x, y) {
        const innerRadius = 10;
        const outerRadius = 30;
        const gradient = ctx.createRadialGradient(x, y, innerRadius, x, y, outerRadius);
        gradient.addColorStop(0, "rgba(255, 0, 0, 0.8)");
        gradient.addColorStop(0.7, "rgba(255, 0, 0, 0.4)");
        gradient.addColorStop(1, "rgba(255, 0, 0, 0.1)");
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, outerRadius, 0, Math.PI * 2);
        ctx.fill();
    }

    // Function to display markers for each accident in the selected month
    function displayMarkers(accidentData) {
        const imageContainer = document.querySelector(".image-container");

        accidentData.forEach(accident => {
            const marker = document.createElement("div");
            marker.classList.add("marker");
            marker.style.top = `${accident.y}px`;
            marker.style.left = `${accident.x}px`;

            // Set the marker image based on the injury type
            const markerImage = document.createElement("img");
            markerImage.src = `images/${accident.type}.png`; // Assuming images are in the 'images' folder
            markerImage.alt = accident.accident;
            marker.appendChild(markerImage);

            imageContainer.appendChild(marker);

            // Create tooltip
            const tooltip = document.createElement("div");
            tooltip.classList.add("tooltip");
            tooltip.style.top = `${accident.y + 30}px`;
            tooltip.style.left = `${accident.x}px`;
            tooltip.innerHTML = `<b>Name:</b> ${accident.name} <br>
                                 <b>ID:</b> ${accident.id} <br>
                                 <b>Accident:</b> ${accident.accident}`;
            imageContainer.appendChild(tooltip);

            // Show tooltip on hover
            marker.addEventListener("mouseenter", function () {
                tooltip.style.display = "block";
            });

            marker.addEventListener("mouseleave", function () {
                tooltip.style.display = "none";
            });
        });
    }
});
