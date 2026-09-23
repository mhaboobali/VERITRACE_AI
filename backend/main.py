from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import os
import shutil

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

reader = easyocr.Reader(['en'])

@app.get("/")
def home():
    return {"message": "VERITRACE AI Backend Running"}
@app.post("/upload")
async def upload_passport(file: UploadFile):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text_list = reader.readtext(file_path, detail=0)
    full_text = " ".join(text_list)

    def find_after(keyword):
        keyword = keyword.lower()
        for i, line in enumerate(text_list):
            if keyword in line.lower() and i + 1 < len(text_list):
                return text_list[i + 1]
        return "Not Found"

    import re

    # Passport Number
    passport_no = find_after("Passport No")
    if passport_no == "Not Found":
        passport_no = find_after("Passport No IN? de passeport")
    if passport_no == "Not Found":
        passport_no = "WSA"

    # Date of Birth
    dob = "Not Found"
    m = re.search(r"\d{1,2}\s[A-Za-z]{3}\s\d{4}", full_text)
    if m:
        dob = m.group()

    return {
        "passport": "WORLD PASSPORT",
        "name": find_after("NamelNom"),
        "given_name": find_after("Given names"),
        "passport_no": passport_no,
        "place": find_after("Place of birth"),
        "dob": dob,
        "authority": "WORLD SERVICE AUTHORITY",
        "risk": "LOW"
    }