from fastapi import APIRouter, UploadFile, HTTPException
from app.services.encoding_service import save_encoding_to_file_np, load_encodings_from_folder
from app.services.face_recognition_service import find_nearest_match
import face_recognition
import os
from pathlib import Path
import io

router = APIRouter()

script_directory = Path(os.path.dirname(__file__))

# Define the base directory for patient encodings relative to the project root
base_directory = Path(script_directory).parent.parent / "data" / "encodings"
os.makedirs(base_directory, exist_ok=True)

@router.post("/register_patient")
async def register_patient(patient_id: str, image: UploadFile):
    try:
        # Construct the full path for the patient's encoding
        patient_directory = base_directory / f"Patient_{patient_id}"
        os.makedirs(patient_directory, exist_ok=True)

        # Process the uploaded image
        image_data = await image.read()
        unknown_image = face_recognition.load_image_file(io.BytesIO(image_data))
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if len(unknown_encodings) == 0:
            raise HTTPException(status_code=400, detail="No face detected in the uploaded image")

        # Save the face encoding
        unknown_encoding = unknown_encodings[0]
        encoding_file_path = patient_directory / f"{patient_id}.npy"
        save_encoding_to_file_np(unknown_encoding, encoding_file_path)

        # Return the correct path in the response
        return {"status": "Encoding saved successfully", "path": str(encoding_file_path.resolve())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login_patient")
async def login_patient(image: UploadFile):
    try:
        # Process the uploaded image for login
        image_data = await image.read()
        unknown_image = face_recognition.load_image_file(io.BytesIO(image_data))
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        if not unknown_encodings:
            return {"status": "No face detected"}

        unknown_encoding = unknown_encodings[0]
        matched_patient = find_nearest_match(unknown_encoding, load_encodings_from_folder(base_directory))
        if matched_patient != "Unknown":
            return {"status": "Authenticated", "patient_id": matched_patient}
        else:
            return {"status": "Authentication Failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
