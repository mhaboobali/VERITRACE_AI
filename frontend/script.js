// =============================
// VERITRACE AI - Frontend Script
// =============================

// Elements
const fileInput = document.getElementById("passportInput");
const previewImage = document.getElementById("previewImage");
const errorMessage = document.getElementById("errorMessage");
const loading = document.getElementById("loading");
const resultCard = document.getElementById("resultCard");

// Image Preview
fileInput.addEventListener("change", function () {
  const file = this.files[0];

  if (!file) return;

  previewImage.src = URL.createObjectURL(file);
  previewImage.style.display = "block";
  errorMessage.classList.add("hidden");
});

// Analyze Passport
async function analyzeDocument() {
  const file = fileInput.files[0];

  if (!file) {
    errorMessage.classList.remove("hidden");
    return;
  }

  errorMessage.classList.add("hidden");
  resultCard.classList.add("hidden");
  loading.classList.remove("hidden");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    // Hide loading
    loading.classList.add("hidden");

    // Show result card
    resultCard.classList.remove("hidden");

    // OCR Result
    document.getElementById("ocrResult").innerHTML = `
<div><strong>Passport:</strong> ${data.passport}</div>
<div><strong>Name:</strong> ${data.name}</div>
<div><strong>Given Name:</strong> ${data.given_name}</div>
<div><strong>Passport No:</strong> ${data.passport_no}</div>
<div><strong>DOB:</strong> ${data.dob}</div>
<div><strong>Place:</strong> ${data.place}</div>
<div><strong>Authority:</strong> ${data.authority}</div>
`;

    // Temporary statuses
    const mrzResult = document.getElementById("mrzResult");

    if (data.mrz !== "Not Found") {
      mrzResult.innerHTML = "✅ Verified<br>";
      const code = document.createElement("code");
      code.textContent = data.mrz; // textContent < ko text hi rakhega
      mrzResult.appendChild(code);
    } else {
      mrzResult.textContent = "❌ Not Found";
    }
    document.getElementById("tamperResult").innerHTML =
      data.tampering === "No Tampering Detected"
        ? "✅ No Tampering Detected"
        : "⚠️ Possible Tampering";
    document.getElementById("faceResult").innerHTML = data.face_detected
      ? "✅ Face Detected"
      : "❌ No Face Detected";
    document.getElementById("graphResult").textContent = "Pending";

    // Risk Badge
    const riskBadge = document.getElementById("riskBadge");
    riskBadge.textContent = "LOW";
    riskBadge.className = "risk low";

    console.log(data);
  } catch (error) {
    loading.classList.add("hidden");
    alert("Backend connection failed.");
    console.error(error);
  }
}
