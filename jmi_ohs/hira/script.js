const jsonFileURL = 'doc/hira_quality.json'; // Adjust the path if needed

let jsonData = [];

// Fetch the JSON data
fetch(jsonFileURL)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();  // Parse JSON response
    })
    .then(data => {
        jsonData = data.HIRA_Register;  // Access 'Sheet1' array from the JSON
        populateMachineDropdown();  // Populate dropdown dynamically
        updateData();  // Initialize page with default data
    })
    .catch(error => {
        console.error('Error fetching or parsing JSON data:', error);
    });

// Function to populate the machine dropdown with unique values from the JSON data
function populateMachineDropdown() {
    const machineSelect = document.getElementById('machineSelect');
    const uniqueMachines = [...new Set(jsonData.map(item => item.Machine))];  // Get unique machines

    // Clear existing options (if any)
    machineSelect.innerHTML = '';

    // Add a default placeholder option
    const defaultOption = document.createElement('option');
    defaultOption.text = 'Select a Machine';
    machineSelect.appendChild(defaultOption);

    // Add options dynamically for each unique machine
    uniqueMachines.forEach(machine => {
        const option = document.createElement('option');
        option.value = machine;
        option.text = machine;
        machineSelect.appendChild(option);
    });
}

// Update data based on selected machine
function updateData() {
    const selectedMachine = document.getElementById('machineSelect').value;
    const filteredData = jsonData.filter(item => item.Machine === selectedMachine);

    // Check if any data is available for the selected machine
    if (filteredData.length > 0) {
        // Update machine and risk matrix images
        document.getElementById('machineImage').innerHTML = `<img src="${selectedMachine}.jpg" alt="${selectedMachine}" width="300">`;
        document.getElementById('riskMatrixImage').innerHTML = `<img src="images/risk_matrix.jpg" alt="Risk Matrix" width="300">`;

        // Populate the HIRA table
        populateHiraTable(filteredData);

        // Populate the control measures table
        populateControlMeasuresTable(filteredData);
    } else {
        console.log('No data available for this machine!');
    }
}

// Function to populate the HIRA table
function populateHiraTable(filteredData) {
    const tableBody = document.querySelector('#hazardTable tbody');
    tableBody.innerHTML = '';  // Clear existing table rows

    filteredData.forEach(machineData => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${machineData.Machine}</td>
            <td>${machineData['Specific Hazard']}</td>
            <td>${machineData['Perceived Risk']}</td>
            <td>${machineData['Severity']}</td>
            <td>${machineData['Likelihood']}</td>
            <td>${machineData['Risk Rating']}</td>
            
        `;
        tableBody.appendChild(row);
    });
}

// Function to populate the Control Measures table
function populateControlMeasuresTable(filteredData) {
    const tableBody = document.querySelector('#controlMeasuresTable tbody');
    tableBody.innerHTML = '';  // Clear existing table rows

    filteredData.forEach(machineData => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${machineData['Machine']}</td>
            <td>${machineData['Perceived Risk']}</td>
            <td>${machineData['Required New Control']}</td>
            <td>${machineData['Responsibility']}</td>
            <td>${machineData['Time Frame']}</td>
            <td>${machineData['Severity (N)']}</td>
            <td>${machineData['Likelihood (N)']}</td>
            <td>${machineData['Risk']}</td>
            
        `;
        tableBody.appendChild(row);
    });
}

// Initialize the page with default machine
window.onload = function() {
    updateData();
};
