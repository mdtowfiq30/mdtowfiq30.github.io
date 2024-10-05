// Initialize the map
const map = L.map('map').setView([23.685, 90.3563], 7);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Create variables for the GeoJSON layers
let divisionLayer, boundaryLayer, districtLayer,upazilaLayer, railwayLayer, waterLayer;

// Fetch and display the boundary layer
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/boundary.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        boundaryLayer = L.geoJSON(geojsonData, {
            style: function (feature) {
                return { color: 'blue' }; // Assign blue color to the boundary layer
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM0_EN || 'Unnamed Boundary');
            }
        }).addTo(map);
        updateLayerControl();
    })
    .catch(error => console.error('Error fetching boundary GeoJSON:', error));

// Fetch and display the division layer
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/division.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        divisionLayer = L.geoJSON(geojsonData, {
            style: function (feature) {
                return { color: 'OrangeRed' }; // Assign blue color to the boundary layer
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM1_EN || 'Unnamed Boundary');
            }
        }).addTo(map);
        updateLayerControl();
    })
    .catch(error => console.error('Error fetching boundary GeoJSON:', error));

// Fetch and display the district layer
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/district.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        districtLayer = L.geoJSON(geojsonData, {
            style: function (feature) {
                return { color: 'BlueViolet' }; // Assign blue color to the boundary layer
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM2_EN || 'Unnamed Boundary');
            }
        }).addTo(map);
        updateLayerControl();
    })
    .catch(error => console.error('Error fetching boundary GeoJSON:', error));


// Fetch and display the upazila layer
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/upazila.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        upazilaLayer = L.geoJSON(geojsonData, {
            style: function (feature) {
                return { color: 'red' }; // Assign blue color to the boundary layer
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM3_EN || 'Unnamed Boundary');
            }
        }).addTo(map);
        updateLayerControl();
    })
    .catch(error => console.error('Error fetching boundary GeoJSON:', error));


// Fetch and display the railway layer
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/railway.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        railwayLayer = L.geoJSON(geojsonData, {
            style: function (feature) {
                return { color: 'Gray' }; // Assign blue color to the boundary layer
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM0_EN || 'Unnamed Boundary');
            }
        }).addTo(map);
        updateLayerControl();
    })
    .catch(error => console.error('Error fetching boundary GeoJSON:', error));

// Fetch and display the railway layer

// Fetch and display the boundary layer
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/waterbody.json')
    .then(response => response.json())
    .then(geojsonData => {
        waterLayer = L.geoJSON(geojsonData, {
            style: function (feature) {
                return { color: 'DarkTurquoise' }; // Assign blue color to the boundary layer
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM0_EN || 'Unnamed Boundary');
            }
        }).addTo(map);
        updateLayerControl();
    })
    .catch(error => console.error('Error fetching boundary GeoJSON:', error));


// Update the layer control to include new layers
function updateLayerControl() {
    const overlays = {
        "Boundary": boundaryLayer,
        "Division": divisionLayer,
        "District": districtLayer,
        "Upazila":upazilaLayer,
        "Railway": railwayLayer,
        "Water":waterLayer
        
        
    };

    L.control.layers(null, overlays, { collapsed: true }).addTo(map);
}

// Function to add the download control
function addDownloadControl() {
    const downloadControl = L.control({ position: 'topleft' });

    downloadControl.onAdd = function () {
        const div = L.DomUtil.create('div', 'download-control');
        div.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
        div.style.padding = "10px";
        div.style.borderRadius = "5px";

        // Create a dropdown for layer selection
        const dropdown = L.DomUtil.create('select', 'layer-dropdown', div);
        const option = L.DomUtil.create('option', '', dropdown);
        option.text = "Select Layer";
        option.value = "";

        // Add options for each layer
        const boundaryOption = L.DomUtil.create('option', '', dropdown);
        boundaryOption.text = "Boundary";
        boundaryOption.value = "boundary";

        const divisionOption = L.DomUtil.create('option', '', dropdown);
        divisionOption.text = "Division";
        divisionOption.value = "division";

        const districtOption = L.DomUtil.create('option', '', dropdown);
        districtOption.text = "District";
        districtOption.value = "district";

        const upazilaOption = L.DomUtil.create('option', '', dropdown);
        upazilaOption.text = "Upazila";
        upazilaOption.value = "upazila";

        const railwayOption = L.DomUtil.create('option', '', dropdown);
        railwayOption.text = "Railway";
        railwayOption.value = "railway";

        const waterOption = L.DomUtil.create('option', '', dropdown);
        waterOption.text = "Water";
        waterOption.value = "water";

        

        // Download button
        const button = L.DomUtil.create('button', 'download-button', div);
        button.innerText = 'Download Layer';

        // Download action
        button.addEventListener('click', function () {
            const selectedLayer = dropdown.value;
            let dataStr, downloadAnchor;

            if (selectedLayer === "boundary") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(boundaryLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "boundary.geojson");
                downloadAnchor.click();
            } else if (selectedLayer === "division") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(divisionLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "division.geojson");
                downloadAnchor.click();
            } else if (selectedLayer === "district") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(districtLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "district.geojson");
                downloadAnchor.click();
            } else if (selectedLayer === "railway") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(railwayLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "railway.geojson");
                downloadAnchor.click();
            } else if (selectedLayer === "water") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(waterLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "waterbody.json");
                downloadAnchor.click();
            } else if (selectedLayer === "upazila") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(upazilaLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "upazla.geojson");
                downloadAnchor.click();
            }
            
            else {
                alert('Please select a layer to download.');
            }
        });

        div.appendChild(dropdown);
        div.appendChild(button);

        return div;
    };

    downloadControl.addTo(map);
}

// Call the download control function
addDownloadControl();
