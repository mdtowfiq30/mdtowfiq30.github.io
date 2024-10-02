// Import PDF.js library
const pdfjsLib = window['pdfjs-dist/build/pdf'];

// Set the path to the PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

// Function to render a single page on its own canvas
function renderPage(pdfDoc, pageNum, scale) {
  pdfDoc.getPage(pageNum).then(function (page) {
    const viewport = page.getViewport({ scale: scale });
    
    // Create a canvas element dynamically for each page
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    
    // Render the page into the canvas
    const renderContext = {
      canvasContext: ctx,
      viewport: viewport
    };

    page.render(renderContext).promise.then(function () {
      console.log('Page ' + pageNum + ' rendered');
    });

    // Append the canvas to the container
    document.querySelector('.pdf-container').appendChild(canvas);
  });
}

// Function to render all pages of the PDF
function renderAllPages(pdfDoc, scale) {
  for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
    renderPage(pdfDoc, pageNum, scale);
  }
}

// Function to load the selected PDF and render all its pages
function loadPDF(pdfUrl) {
  console.log("Loading PDF: " + pdfUrl);
  
  // Clear the container before rendering a new PDF
  const container = document.querySelector('.pdf-container');
  container.innerHTML = '';

  pdfjsLib.getDocument(pdfUrl).promise.then(function (pdfDoc) {
    console.log("PDF Loaded, Total pages: " + pdfDoc.numPages);
    
    // Render all pages
    renderAllPages(pdfDoc, 1.5); // You can change the scale factor to adjust page size
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
