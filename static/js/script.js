const logoUploadInput = document.getElementById("logo");
const uploadLogoButton = document.getElementById("btn-upload-logo");
const logoHelperText = document.getElementById("logo-helper-text");
const logoLabel = document.getElementById("logo-label");

function sendLogo() {}

uploadLogoButton.addEventListener("click", () => {
  const extension = logoUploadInput.value.substring(
    logoUploadInput.value.lastIndexOf(".") + 1,
    logoUploadInput.value.length
  );
  if (!logoUploadInput.value) {
    logoHelperText.classList.remove("invisible");
  } else if (extension != "png" && extension != "jpg" && extension != "jpeg") {
    logoHelperText.textContent =
      "Please select images in the format JPG, JPEG or PNG";
    logoHelperText.classList.remove("invisible");
  } else {
    logoHelperText.classList.add("invisible");
    const formData = new FormData();
    formData.append("file", logoUploadInput.files[0]);
    fetch("/upload-file", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          // Handle Error
        }
      })
      .then((data) => {
        console.log(data);
      });
  }
});

logoLabel.addEventListener("click", (e) => {
  e.preventDefault();
});
