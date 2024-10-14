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
let boundaryLayer, divisionLayer, districtLayer, waterLayer;

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
        });  // Division layer not added to the map by default
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
        });  // District layer added to map by default
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

// Add the NDVI overlay
const NDVIMap = L.tileLayer('https://earthengine.googleapis.com/v1/projects/ee-mdtowfiq300/maps/8d6b10965c8a23f7df2521fa2270a8f9-9dea3d0792a50105a7fa915d5f67bbf3/tiles/{z}/{x}/{y}' );


// Add the NDWI overlay (link from GitHub raw file)
const NDWIdMap = L.tileLayer("https://earthengine.googleapis.com/v1/projects/ee-mdtowfiq300/maps/3b8aee06324d0c9baad6554515d520d4-fe2dbae70e906fe72506c62b04aea346/tiles/{z}/{x}/{y}");

// Function to update layer control
function updateLayerControl() {
    const baseLayers = {
        "OpenStreetMap": openStreetMap,
        "Imagery": imageryMap,
        "Terrain": combine
    };

    const overlayLayers = {
        "Boundary": boundaryLayer,
        "Division": divisionLayer,
        "District": districtLayer,
        "Water Bodies": waterLayer,
        "NDVI": NDVIMap,
        "NDWI":NDWIdMap
    };

    L.control.layers(baseLayers, overlayLayers, { collapsed: false }).addTo(map);
}

// Function to add the download control
function addDownloadControl() {
    const downloadControl = L.control({ position: 'topleft' });

    downloadControl.onAdd = function () {
        const div = document.querySelector('.download-container') || L.DomUtil.create('div', 'download-container');
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
        districtOption.value = "district";

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
            } else {
                alert('Please select a layer to download.');
            }
        });

        div.appendChild(dropdown);
        div.appendChild(button);

        return div;
    };

    downloadControl.addTo(map);
}

// Layer control toggle for smaller screens
const layerIcon = document.getElementById('layer-icon');
let isLayerControlVisible = false;

layerIcon.addEventListener('click', function () {
    if (!isLayerControlVisible) {
        document.querySelector('.leaflet-control-layers').style.display = 'block';
        isLayerControlVisible = true;
    } else {
        document.querySelector('.leaflet-control-layers').style.display = 'none';
        isLayerControlVisible = false;
    }
});

// Initially hide layer control for smaller screens
if (window.innerWidth <= 768) {
    document.querySelector('.leaflet-control-layers').style.display = 'none';
}

// Call the download control function after the map is initialized
addDownloadControl();
