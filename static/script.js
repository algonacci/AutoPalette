var loadFile = function (event) {
  var output = document.getElementById("output");
  output.src = URL.createObjectURL(event.target.files[0]);

  var uploadedImageHeading = document.getElementById("uploaded-image-heading");
  uploadedImageHeading.style.display = "block";

  // Store the current image file for tritone processing
  window.currentImageFile = event.target.files[0];
  var tritoneButton = document.getElementById("tritoneButton");
  if (tritoneButton) {
    tritoneButton.style.display = "block";
  }
};

const dropZone = document.getElementById("drop-zone");

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("border-blue-500");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("border-blue-500");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("border-blue-500");

  const file = e.dataTransfer.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (event) {
      const output = document.getElementById("output");
      output.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }

  const fileInput = document.querySelector('input[name="image"]');
  fileInput.files = e.dataTransfer.files;
});

const colorCodeElements = document.querySelectorAll(".copy-color-code");

colorCodeElements.forEach((element) => {
  element.addEventListener("click", () => {
    const colorCode = element.getAttribute("data-color");
    copyToClipboard(colorCode);
    Swal.fire("Good job!", `You copied: ${colorCode}`, "success");
  });
});

// Function to copy text to clipboard
function copyToClipboard(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}

// Function to create tritone effect
function createTritoneEffect() {
  if (window.currentImageFile) {
    const tritoneForm = document.getElementById("tritoneForm");
    const tritoneInput = document.getElementById("tritoneImageInput");
    
    // Create a new FileList with the current image
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(window.currentImageFile);
    tritoneInput.files = dataTransfer.files;
    
    tritoneForm.submit();
  }
}
