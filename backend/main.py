
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI(title="VERITRACE AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "VERITRACE AI Backend Running"}

@app.post("/upload")
async def upload_passport(file: UploadFile):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Passport uploaded successfully",
        "filename": file.filename
    }