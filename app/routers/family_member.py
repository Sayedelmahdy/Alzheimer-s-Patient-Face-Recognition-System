from fastapi import APIRouter, UploadFile, HTTPException
from typing import List
import face_recognition
from io import BytesIO
from app.services.encoding_service import save_encoding_to_file_np, load_encodings_from_folderForFamily
from app.services.face_recognition_service import find_best_match_for_family
import os
from pathlib import Path
import cv2
import shutil
import logging
import numpy as np  
from PIL import Image 

router = APIRouter()

script_directory = Path(os.path.dirname(__file__))

@router.post("/register_image")
async def register_image(patient_id: str, family_member_id: str, idx: str, image: UploadFile):
    base_path = script_directory / "encodings" / f"Patient_{patient_id}" / f"FamilyMember_{family_member_id}"
    os.makedirs(base_path, exist_ok=True)

    try:
        image_data = await image.read()
        face_image = face_recognition.load_image_file(BytesIO(image_data))
        encodings = face_recognition.face_encodings(face_image)
        if encodings:
            save_encoding_to_file_np(encodings[0], base_path / f"{family_member_id}_{idx}.npy")

        return f"Encodings for Family Member {family_member_id} registered successfully."

    except HTTPException as e:
        shutil.rmtree(base_path)
        raise e
    except Exception as e:
        shutil.rmtree(base_path)
        logging.error(f"An error occurred while registering image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recognize_faces")
async def recognize_faces_in_image(patient_id: str, image: UploadFile):
    try:
        patient_directory = script_directory / "encodings" / f"Patient_{patient_id}"
        known_encodings = load_encodings_from_folderForFamily(patient_directory)

        image_data = await image.read()
        face_image = face_recognition.load_image_file(BytesIO(image_data))
        face_encodings = face_recognition.face_encodings(face_image)
        
        results = []
        for face_encoding in face_encodings:
            best_match_name = find_best_match_for_family(face_encoding, known_encodings)
            results.append({"identified_name": best_match_name})
        
        return {"recognition_results": results}
    except Exception as e:
        logging.error(f"Error during face recognition: {e}")
        raise HTTPException(status_code=500, detail=str(e))
