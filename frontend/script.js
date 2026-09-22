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

async function analyzeDocument() {
  const input = document.getElementById("passportInput");
  const file = input.files[0];

  if (!file) {
    document.getElementById("errorMessage").classList.remove("hidden");
    return;
  }

  document.getElementById("errorMessage").classList.add("hidden");
  document.getElementById("loading").classList.remove("hidden");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    document.getElementById("loading").classList.add("hidden");
    document.getElementById("resultCard").classList.remove("hidden");

    document.getElementById("ocrResult").textContent = "Uploaded";
    document.getElementById("mrzResult").textContent = "Pending";
    document.getElementById("tamperResult").textContent = "Pending";
    document.getElementById("faceResult").textContent = "Pending";
    document.getElementById("graphResult").textContent = "Pending";

    const riskBadge = document.getElementById("riskBadge");
    riskBadge.textContent = "UPLOADED";
    riskBadge.className = "risk medium";

    console.log(data);
  } catch (error) {
    document.getElementById("loading").classList.add("hidden");
    alert("Backend connection failed.");
  }
}
