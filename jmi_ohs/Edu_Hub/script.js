document.getElementById("pdf-select").addEventListener("change", function() {
    document.getElementById("pdf-viewer").src = this.value;
    document.getElementById("mobile-pdf-viewer").data = this.value;
});
