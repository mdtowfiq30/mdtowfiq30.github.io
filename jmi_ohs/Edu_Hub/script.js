document.getElementById("pdf-select").addEventListener("change", function() {
    let pdfFile = this.value;
    document.getElementById("pdf-viewer").src = pdfFile;
    document.getElementById("mobile-pdf-link").href = pdfFile;
});
