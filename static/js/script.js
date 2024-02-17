const logoUploadInput = document.getElementById("logo");
const uploadLogoButton = document.getElementById("btn-upload-logo");
const logoHelperText = document.getElementById("logo-helper-text");
const logoLabel = document.getElementById("logo-label");
const confirmDetailsBtn = document.getElementById("confirm-details-btn");
const incorrectDetailsText = document.getElementById("incorrect-details-text");

const phNoRegex = /^[6-9]\d{9}$/;
const gstinRegex = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;

function sendLogo() {
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
          alert("An Error Occured. Please Refresh the page & Try again.");
        }
      })
      .then((data) => {
        const message = data.message;
        logoHelperText.textContent = message;
        logoHelperText.classList.remove("invisible");
      });
  }
}

function handleConfirm() {
  const shopName = document.getElementById("shop-name").value;
  const address = document.getElementById("address").value;
  const phNo = document.getElementById("phone-num").value;
  const gstin = document.getElementById("gst-num").value;
  if (!shopName || !address || !phNo || !gstin) {
    incorrectDetailsText.classList.remove("invisible");
  } else if (!gstinRegex.test(gstin)) {
    incorrectDetailsText.textContent = "Please Enter a Valid GSTIN";
    incorrectDetailsText.classList.remove("invisible");
  } else if (!phNoRegex.test(phNo)) {
    incorrectDetailsText.textContent = "Please Enter a Valid Phone Number";
    incorrectDetailsText.classList.remove("invisible");
  } else {
    fetch("/default", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        shopName: shopName,
        address: address,
        phNo: phNo,
        gstin: gstin,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          alert("An Error Occured. Please Refresh the page and try again.");
        }
      })
      .then((data) => {
        const anchorDefault = document.createElement("a");
        anchorDefault.href = "/default-page";
        anchorDefault.style.display = "none";
        document.body.appendChild(anchorDefault);
        anchorDefault.click();
      });
  }
}

uploadLogoButton.addEventListener("click", sendLogo);
logoLabel.addEventListener("click", (e) => {
  e.preventDefault();
});
confirmDetailsBtn.addEventListener("click", handleConfirm);
