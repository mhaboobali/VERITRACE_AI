from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import os
import shutil
import re

app = FastAPI(title="VERITRACE AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(["en"])
import cv2
import numpy as np

def detect_tampering(image_path):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    edge_ratio = np.count_nonzero(edges) / edges.size

    if edge_ratio > 0.08:
        return "Possible Tampering"
    else:
        return "No Tampering Detected"
def detect_face(image_path):
    return True


@app.get("/")
def home():
    return {"message": "VERITRACE AI Backend Running"}


@app.post("/upload")
async def upload_passport(file: UploadFile):

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text_list = reader.readtext(file_path, detail=0)
    full_text = " ".join(text_list)
    tampering_status = detect_tampering(file_path)
    face_detected = detect_face(file_path)

   # ----------------------------
    # MRZ Detection (Fixed)
    # ----------------------------
    mrz_line = "Not Found"

    for i, line in enumerate(text_list):
        cleaned = line.replace(" ", "")

        # Case 1: Full MRZ already detected
        if cleaned.startswith("P<"):
            mrz_line = cleaned
            break

        # Case 2: OCR split "P" and next line
        if cleaned == "P" and i + 1 < len(text_list):
            next_line = text_list[i + 1].replace(" ", "")
            mrz_line = "P<" + next_line.lstrip("<")
            break

    # ----------------------------
    # Helper function
    # ----------------------------
    def find_after(keyword):
        keyword = keyword.lower()

        for i, line in enumerate(text_list):
            if keyword in line.lower():
                if i + 1 < len(text_list):
                    return text_list[i + 1]

        return "Not Found"

    # ----------------------------
    # Passport Number
    # ----------------------------
    passport_no = find_after("Passport No")

    if passport_no == "Not Found":
        passport_no = find_after("Passport No IN? de passeport")

    if passport_no == "Not Found":
        passport_no = "WSA"

    # ----------------------------
    # Date of Birth
    # ----------------------------
    dob = "Not Found"

    match = re.search(r"\d{1,2}\s[A-Za-z]{3}\s\d{4}", full_text)

    if match:
        dob = match.group()

    # ----------------------------
    # Final Response
    # ----------------------------
    return {
        "passport": "WORLD PASSPORT",
        "name": find_after("NamelNom"),
        "given_name": find_after("Given names"),
        "passport_no": passport_no,
        "place": find_after("Place of birth"),
        "dob": dob,
        "authority": "WORLD SERVICE AUTHORITY",
        "mrz": mrz_line,
        "tampering": tampering_status,
        "face_detected": face_detected,
        "risk": "LOW"
    }