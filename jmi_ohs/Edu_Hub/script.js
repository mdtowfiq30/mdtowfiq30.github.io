document.getElementById("pdf-select").addEventListener("change", function() {
    document.getElementById("pdf-viewer").src = this.value;
});
