// const serverURL = "http://localhost:5000";
const serverURL = "https://pe-o4br.onrender.com";

// select fields
const area = document.getElementById("area");
const locationElement = document.getElementById("location");
const feType = document.getElementById("feType");
const capacity = document.getElementById("capacity");
const pressure = document.getElementById("pressure");
const seal = document.getElementById("seal");
const obstruction = document.getElementById("obstruction");
const tags = document.getElementById("tags");
const damage = document.getElementById("damage");
const refillDate = document.getElementById("refillDate");
const nextRefillDate = document.getElementById("nextRefillDate");
const inspectionDate = document.getElementById("inspectionDate");
const remarks = document.getElementById("remarks");
const form = document.getElementById("updateForm");

// empty all field value
function emptyField() {
  area.textContent = "";
  locationElement.textContent = "";
  feType.textContent = "";
  capacity.textContent = "";
  pressure.value = "";
  seal.value = "";
  obstruction.value = "";
  tags.value = "";
  remarks.value = "";
  damage.value = "";
  refillDate.value = "";
  nextRefillDate.value = "";
  inspectionDate.value = "";
}

// Fetch all Fire Extinguisher numbers from the database and populate the dropdown
function fetchFENumbers() {
  fetch(`${serverURL}/api/v1/fe`)
    .then((response) => response.json())
    .then((data) => {
      emptyField();
      const feDropdown = document.getElementById("feNo");
      feDropdown.innerHTML =
        '<option value="">Select Fire Extinguisher</option>';
      data?.data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item["feNo"];
        option.textContent = item["feNo"];
        feDropdown.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching FE Nos:", error));
}

// Fetch Fire Extinguisher Details when a FE No. is selected
document.getElementById("feNo").addEventListener("change", function () {
  const feNo = this.value;

  if (feNo) {
    fetch(`${serverURL}/api/v1/fe/${feNo}`)
      .then((response) => response.json())
      .then(({ data }) => {
        // Populate the FE Details section
        area.textContent = data["area"] || "";
        locationElement.textContent = data["location"] || "";
        feType.textContent = data["feType"] || "";
        capacity.textContent = data["capacity"] || "";
        pressure.value = data["pressureCondition"] || "";
        seal.value = data["safetySeal"] || "";
        obstruction.value = data["maintainedFreeOfObstruction"] || "";
        tags.value = data["clearTags"] || "";
        remarks.value = data["remarks"] || "";
        damage.value = data["physicalDamage"] || "";
        refillDate.value = data["refillDate"] || "";
        nextRefillDate.value = data["nextRefillDate"] || "";
        inspectionDate.value = data["inspectionDate"] || "";
      })
      .catch((error) => {
        console.error("Error fetching FE details:", error);
      });
  } else {
    emptyField();
  }
});

// Update Fire Extinguisher data in the database
form.addEventListener("submit", function (event) {
  // prevent the form from submitting
  event.preventDefault();

  // get the selected Fire Extinguisher number
  const feNo = document.getElementById("feNo").value;

  if (!feNo) {
    return alert("Please select a Fire Extinguisher!");
  }

  // get the form data
  const formData = new FormData(event.target);

  const data = Object.fromEntries(formData.entries());

  // update  Fire Extinguisher data in the database
  fetch(`${serverURL}/api/v1/fe/${feNo}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...data,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Data updated successfully!");
      }
    })
    .catch((error) => console.error("Error updating data:", error));
});

// Clear specific columns in the database (reset values)
function clearData() {
  if (
    !confirm(
      "Are you sure you want to clear the inspection details? This action cannot be undone."
    )
  ) {
    return;
  }

  fetch(`${serverURL}/api/v1/fe/clear-data`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Data cleared successfully!");
        emptyField();
      }
    })
    .catch((error) => console.error("Error clearing data:", error));
}

// Export Fire Extinguisher database as a CSV file
function exportCSV() {
  window.open(`${serverURL}/api/v1/fe/export-csv`, "_blank");
  // window.location.href = `${serverURL}/api/v1/fe/export-csv`;
}

// Event listeners
document.addEventListener("DOMContentLoaded", function () {
  fetchFENumbers(); // Populate dropdown on page load
});
