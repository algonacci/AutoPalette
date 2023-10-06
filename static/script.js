var loadFile = function (event) {
  var output = document.getElementById("output");
  output.src = URL.createObjectURL(event.target.files[0]);

  var uploadedImageHeading = document.getElementById("uploaded-image-heading");
  uploadedImageHeading.style.display = "block";
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
