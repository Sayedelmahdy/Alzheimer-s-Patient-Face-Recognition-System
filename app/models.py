from typing import List
from pydantic import BaseModel
from fastapi import UploadFile

class ImageData(BaseModel):
    patient_id: str
    family_member_id: str
    images: List[UploadFile]

class LoginData(BaseModel):
    patient_id: str
    image: UploadFile
