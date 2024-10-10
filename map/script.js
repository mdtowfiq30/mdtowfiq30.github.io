// Initialize the map
const map = L.map('map', {
    center: [23.685, 90.3563], // Bangladesh coordinates
    zoom: 7
});

// Add default OpenStreetMap layer (added by default)
const openStreetMap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);  // OpenStreetMap added to map by default

// Add ESRI Imagery layer (not added by default)
const imageryMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// Add ESRI Terrain base layer (not added by default)
const esriTerrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 17,
    attribution: '&copy; Esri &mdash; Sources: Esri, USGS, NOAA'
});

// Add OpenStreetMap labels layer (not added by default)
const osmLabels = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
    opacity: 0.6
});

// Combine ESRI Terrain with OSM Labels into one 'combine' layer
const combine = L.layerGroup([esriTerrain, osmLabels]);

// Create GeoJSON layers for boundary and river
let boundaryLayer,divisionLayer, waterLayer;

// Fetch and display the boundary layer (added to map by default)
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/boundary.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        boundaryLayer = L.geoJSON(geojsonData, {
            style: { color: 'green', weight: 1 },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM0_EN || 'Unnamed Boundary');
            }
        }).addTo(map);  // Boundary layer added to map by default
        updateLayerControl();
    });

// Fetch and display the division layer (added to map by default)
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/division.json')
    .then(response => response.json())
    .then(geojsonData => {
        divisionLayer = L.geoJSON(geojsonData, {
            style: { color: 'OrangeRed', weight: 1 },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM1_EN || 'Unnamed Boundary');
            }
        });  // Boundary layer added to map by default
        updateLayerControl();
    });


// Fetch and display the district layer (added to map by default)
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/district.json')
    .then(response => response.json())
    .then(geojsonData => {
        districtLayer = L.geoJSON(geojsonData, {
            style: { color: 'OrangeRed', weight: 1 },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM2_EN || 'Unnamed Boundary');
            }
        });  // Boundary layer added to map by default
        updateLayerControl();
    });


// Fetch and display the river layer (not added to the map by default)
fetch('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/water_body.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        waterLayer = L.geoJSON(geojsonData, {
            style: { color: 'blue', weight: .2, opacity: .8 },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.ADM0_EN || 'Unnamed River');
            }
        });  // River layer not added to the map by default
        updateLayerControl();
    });

// Define the bounds for Bangladesh (adjust SW and NE corners if necessary)
const imageBounds = [[20.4110767, 84.4502653], [27.7924300, 95.8792157]];

// Add the PNG overlay (link from GitHub raw file)
const bivariateMap = L.imageOverlay('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/precipitation.png', imageBounds);

// Define the bounds for river (adjust SW and NE corners if necessary)
const rivershedBounds = [[20.1208200, 87.0715245], [26.7756004, 93.9161178]];

// Add the PNG overlay (link from GitHub raw file)
const rivershedMap = L.imageOverlay('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/river_shed.png', rivershedBounds);

// Define the bounds for soil (adjust SW and NE corners if necessary)
const soilBounds = [[20.2847726, 87.1386001], [27.4185750, 95.1812276]];

// Add the PNG overlay (link from GitHub raw file)
const soilMap = L.imageOverlay('https://raw.githubusercontent.com/mdtowfiq30/web_map/main/soil_texture_map_no_bg.png', soilBounds);

// Layer control function to add base and overlay layers
function updateLayerControl() {
    const baseMaps = {
        "OpenStreetMap": openStreetMap,  // OpenStreetMap is selected by default
        "Imagery": imageryMap,
        "Terrain": combine,
    };

    const overlayMaps = {
        "Boundary": boundaryLayer,
        "Division":divisionLayer,
        "District":districtLayer,  
        "Water": waterLayer,
        "Temp & precipitation": bivariateMap,
        "River Sheds": rivershedMap,
        "Soil Texture":soilMap,
        
    };

    L.control.layers(baseMaps, overlayMaps, { collapsed: false }).addTo(map);
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

        const boundaryOption = L.DomUtil.create('option', '', dropdown);
        boundaryOption.text = "Boundary";
        boundaryOption.value = "boundary";

        const divisionOption = L.DomUtil.create('option', '', dropdown);
        divisionOption.text = "Division";
        divisionOption.value = "division";

        const districtOption = L.DomUtil.create('option', '', dropdown);
        districtOption.text = "District";
        districtOption.value = "ddistrict";

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
            } else if (selectedLayer === "water") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(waterLayer.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "water_body.geojson");
                downloadAnchor.click();
            } else if (selectedLayer === "division") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(division.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "division.json");
                downloadAnchor.click();
            } else if (selectedLayer === "district") {
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(district.toGeoJSON()));
                downloadAnchor = document.createElement('a');
                downloadAnchor.setAttribute("href", dataStr);
                downloadAnchor.setAttribute("download", "district.json");
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

// Handle CSV file upload and plot markers
document.getElementById('csvFile').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const csvData = e.target.result;
            processCSV(csvData);  // Function to handle the CSV data
        };
        reader.readAsText(file);
    }
});

// Process CSV data and add markers to the map
function processCSV(csvData) {
    const lines = csvData.split('\n');
    const headers = lines[0].split(',');
    const latIndex = headers.indexOf('lat');
    const lonIndex = headers.indexOf('lon');

    for (let i = 1; i < lines.length; i++) {
        const row = lines[i].split(',');
        if (row[latIndex] && row[lonIndex]) {
            const lat = parseFloat(row[latIndex]);
            const lon = parseFloat(row[lonIndex]);
            if (!isNaN(lat) && !isNaN(lon)) {
                L.marker([lat, lon]).addTo(map)
                    .bindPopup(`Lat: ${lat}, Lon: ${lon}`).openPopup();
            }
        }
    }
}
// Call the download control function
addDownloadControl();
