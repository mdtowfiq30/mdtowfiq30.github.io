// Import PDF.js library
const pdfjsLib = window['pdfjs-dist/build/pdf'];

// Set the path to the PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

// Initial PDF document and canvas setup
let pdfDoc = null,
  pageNum = 1,
  scale = 1.5,
  canvas = document.getElementById('pdfCanvas'),
  ctx = canvas.getContext('2d');

// Function to render the page
function renderPage(num) {
  pdfDoc.getPage(num).then(function (page) {
    const viewport = page.getViewport({ scale: scale });
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };

    page.render(renderContext);
    console.log("Rendering page: " + num);
  });
}

// Load the selected PDF
function loadPDF(pdfUrl) {
  console.log("Loading PDF: " + pdfUrl);
  pdfjsLib.getDocument(pdfUrl).promise.then(function (pdfDoc_) {
    pdfDoc = pdfDoc_;
    console.log("PDF Loaded");
    renderPage(pageNum); // Render the first page
  }).catch(function(error) {
    console.error("Error loading PDF: ", error);
  });
}

// Event listener for PDF selection
document.getElementById('pdfSelect').addEventListener('change', function (e) {
  const selectedPDF = e.target.value;
  loadPDF(selectedPDF); // Load the selected PDF

  // Update the download button href attribute
  document.getElementById('downloadBtn').href = selectedPDF;
});

// Load the default PDF on page load
window.onload = function () {
  const defaultPDF = document.getElementById('pdfSelect').value;
  loadPDF(defaultPDF);
};
