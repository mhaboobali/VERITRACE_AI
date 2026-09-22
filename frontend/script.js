// Passport upload hone ke baad preview dikhana
function previewImage() {
  const input = document.getElementById("passportInput");
  const file = input.files[0];

  if (file) {
    const preview = document.getElementById("preview");

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    // Error message hide
    document.getElementById("errorMessage").classList.add("hidden");
  }
}

// Analyze button
function analyzeDocument() {
  const input = document.getElementById("passportInput");
  const file = input.files[0];

  // Agar file upload nahi hui
  if (!file) {
    document.getElementById("errorMessage").classList.remove("hidden");
    return;
  }

  // Error hide
  document.getElementById("errorMessage").classList.add("hidden");

  // Loading show
  document.getElementById("loading").classList.remove("hidden");

  // Dummy analysis (backend baad me connect karenge)
  setTimeout(() => {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("resultCard").classList.remove("hidden");

    document.getElementById("ocrResult").textContent = "Extracted";
    document.getElementById("mrzResult").textContent = "Valid";
    document.getElementById("tamperResult").textContent = "Low";
    document.getElementById("faceResult").textContent = "Matched";
    document.getElementById("graphResult").textContent = "1 Related Case";

    const riskBadge = document.getElementById("riskBadge");
    riskBadge.textContent = "MEDIUM";
    riskBadge.className = "risk medium";
  }, 1500);
}
