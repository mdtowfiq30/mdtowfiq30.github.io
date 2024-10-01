// Get references to the PDF embed and dropdown select element
const pdfEmbed = document.getElementById('pdfEmbed');
const pdfSelect = document.getElementById('pdfSelect');

// Add an event listener to the dropdown to detect changes
pdfSelect.addEventListener('change', function() {
  // Update the embed src attribute to the new PDF file selected
  const selectedPDF = pdfSelect.value;
  pdfEmbed.src = selectedPDF;
});
