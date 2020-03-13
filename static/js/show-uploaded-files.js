// Get the necessary references from the DOM by id...
let fileList = document.getElementById("choosen-image-files")
let fileUpload = document.getElementById("gallery-images");

// Register for change events on the file upload control...
fileUpload.addEventListener("change", (event) => {
  const files = event.target.files;
  populateFileList(files);
});

const populateFileList = (files) => {
  // Remove all children
  fileList.innerHTML = "";

  // Populate new children depending on the file names the user has uploaded...
  for (var i = 0; i < files.length; i++) {
    const listElement = document.createElement("li")
    listElement.innerHTML = files[i].name;
    fileList.append(listElement);
  }
};
