document.addEventListener("DOMContentLoaded", function () {
    // Accident data for each month
    const monthData = {
        january: [
            { x: 800, y: 100, type: "foot", name: "Shakil", id: "12345", accident: "👣" },
            { x: 400, y: 150, type: "hand", name: "Michael Smith", id: "54321", accident: "Hand Injury ✋" }
        ],
        february: [
            { x: 650, y: 310, type: "foot", name: "Shakil Ahammod", id: "26086005", accident: "👣" },
            { x: 300, y: 200, type: "hand", name: "Jane Smith", id: "67890", accident: "Hand Injury ✋" },
            { x: 500, y: 310, type: "foot", name: "Md. Ibrahim", id: "26086006", accident: "👣" }
        ],
        march: [
            { x: 700, y: 250, type: "eye", name: "Sarah Lee", id: "33567", accident: "Eye Injury 👁️" },
            { x: 600, y: 400, type: "hand", name: "David Clark", id: "78901", accident: "Hand Injury ✋" }
        ],
    };

    // Retrieve selected month from localStorage or default to January
    let selectedMonth = localStorage.getItem("selectedMonth") || "january";
    let heatmapVisible = false;
    let allAccidentData = []; // Store all data points for the heatmap

    // Set the dropdown to the saved value
    document.getElementById("month").value = selectedMonth;

    // Function to update displayed markers
    function updateMarkers() {
        const accidentData = monthData[selectedMonth];

        if (!accidentData || accidentData.length === 0) {
            alert("No data available for " + selectedMonth);
            return;
        }

        clearMarkersAndTooltips();
        displayMarkers(accidentData);
    }

    // Display markers for the initially selected month
    updateMarkers();

    // Event listener for selecting a month
    document.getElementById("month").addEventListener("change", function () {
        selectedMonth = document.getElementById("month").value;
        localStorage.setItem("selectedMonth", selectedMonth); // Save selected month
        updateMarkers();
    });

    // Event listener for toggling the heatmap
    document.getElementById("toggleHeatmap").addEventListener("click", function () {
        const accidentData = monthData[selectedMonth];

        if (!accidentData || accidentData.length === 0) {
            alert("No data available for " + selectedMonth);
            return;
        }

        clearMarkersAndTooltips();

        if (!heatmapVisible) {
            heatmapVisible = true;
            allAccidentData = Object.values(monthData).flat(); // Aggregate all months' data
            generateHeatmap(allAccidentData);
        } else {
            heatmapVisible = false;
            const heatmapCanvas = document.querySelector(".heatmap-canvas");
            if (heatmapCanvas) heatmapCanvas.remove();
            updateMarkers(); // Restore markers for selected month
        }
    });

    function clearMarkersAndTooltips() {
        document.querySelectorAll(".marker, .tooltip").forEach(el => el.remove());
    }

    function generateHeatmap(accidentData) {
        const imageContainer = document.querySelector(".image-container");
        const canvas = document.createElement("canvas");
        canvas.width = imageContainer.clientWidth;
        canvas.height = imageContainer.clientHeight;
        canvas.classList.add("heatmap-canvas");
        imageContainer.appendChild(canvas);
        const ctx = canvas.getContext("2d");

        accidentData.forEach(accident => drawHeatSpot(ctx, accident.x, accident.y));
    }

    function drawHeatSpot(ctx, x, y) {
        const innerRadius = 10, outerRadius = 30;
        const gradient = ctx.createRadialGradient(x, y, innerRadius, x, y, outerRadius);
        gradient.addColorStop(0, "rgba(255, 0, 0, 0.8)");
        gradient.addColorStop(0.7, "rgba(255, 0, 0, 0.4)");
        gradient.addColorStop(1, "rgba(255, 0, 0, 0.1)");
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, outerRadius, 0, Math.PI * 2);
        ctx.fill();
    }

    function displayMarkers(accidentData) {
        const imageContainer = document.querySelector(".image-container");

        accidentData.forEach(accident => {
            const marker = document.createElement("div");
            marker.classList.add("marker");
            marker.style.top = `${accident.y}px`;
            marker.style.left = `${accident.x}px`;

            const markerImage = document.createElement("img");
            markerImage.src = `images/${accident.type}.png`;
            markerImage.alt = accident.accident;
            marker.appendChild(markerImage);
            imageContainer.appendChild(marker);

            const tooltip = document.createElement("div");
            tooltip.classList.add("tooltip");
            tooltip.style.top = `${accident.y + 30}px`;
            tooltip.style.left = `${accident.x}px`;
            tooltip.innerHTML = `<b>Name:</b> ${accident.name} <br><b>ID:</b> ${accident.id} <br><b>Accident:</b> ${accident.accident}`;
            imageContainer.appendChild(tooltip);

            marker.addEventListener("mouseenter", () => tooltip.style.display = "block");
            marker.addEventListener("mouseleave", () => tooltip.style.display = "none");
        });
    }
});
