console.log("Upload Resume JS Loaded");

const uploadBox = document.querySelector(".upload-box");
const resumeInput = document.getElementById("resume");
const fileName = document.getElementById("file-name");

const MAX_SIZE = 5 * 1024 * 1024;

// Open file picker when upload box is clicked
uploadBox.addEventListener("click", function (e) {

    if (e.target.tagName !== "BUTTON") {
        resumeInput.click();
    }

});

// File selected
resumeInput.addEventListener("change", function () {

    if (resumeInput.files.length === 0) {

        fileName.innerHTML = "No file selected";

        return;

    }

    const file = resumeInput.files[0];

    if (file.type !== "application/pdf") {

        alert("Only PDF files are allowed.");

        resumeInput.value = "";

        fileName.innerHTML = "No file selected";

        return;

    }

    if (file.size > MAX_SIZE) {

        alert("Maximum file size is 5 MB.");

        resumeInput.value = "";

        fileName.innerHTML = "No file selected";

        return;

    }

    fileName.innerHTML =
        `<i class="bi bi-file-earmark-pdf-fill text-danger"></i>
         ${file.name}`;

});

// Drag Over
uploadBox.addEventListener("dragover", function (e) {

    e.preventDefault();

    uploadBox.classList.add("drag-active");

});

// Drag Leave
uploadBox.addEventListener("dragleave", function () {

    uploadBox.classList.remove("drag-active");

});

// Drop
uploadBox.addEventListener("drop", function (e) {

    e.preventDefault();

    uploadBox.classList.remove("drag-active");

    resumeInput.files = e.dataTransfer.files;

    resumeInput.dispatchEvent(new Event("change"));

});