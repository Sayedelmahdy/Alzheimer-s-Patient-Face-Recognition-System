Alzheimer's Patient Face Recognition System

This project is a specialized face recognition system designed to assist Alzheimer's patients in recognizing their loved ones. The system allows for the registration of family members' faces and enables Alzheimer's patients to authenticate themselves using facial recognition.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Installation](#step-by-step-installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Accessing the API](#accessing-the-api)
- [API Endpoints](#api-endpoints)
  - [Register Family Member](#register-family-member)
  - [Recognize Family Member](#recognize-family-member)
  - [Register Patient](#register-patient)
  - [Patient Login](#patient-login)
- [Detailed Functionality](#detailed-functionality)
  - [Face Registration](#face-registration)
  - [Face Recognition](#face-recognition)
  - [Patient Login](#patient-login-functionality)
  - [Encoding Services](#encoding-services)
- [Contributing](#contributing)
- [License](#license)

## Overview

This system is built with the primary goal of aiding Alzheimer's patients by allowing them to recognize family members and authenticate themselves through facial recognition. The application leverages the FastAPI framework to provide an easy-to-use API interface for registering and recognizing faces.

## Features

- **Family Member Registration**: Easily register a family member’s face with the system.
- **Patient Login**: Patients can log in using facial recognition, providing a seamless and secure authentication process.
- **Face Recognition**: The system can recognize previously registered faces with high accuracy.
- **Secure Storage**: Face encodings are securely stored as `.npy` files.

## Project Structure

```plaintext
AlzheimerFaceRecognition/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # Entry point for the FastAPI application
│   ├── models.py              # Pydantic models for request data validation
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── family_member.py   # Routes for family member registration and face recognition
│   │   └── patient.py         # Routes for patient registration and login
│   └── services/
│       ├── __init__.py
│       ├── encoding_service.py    # Service for handling face encoding operations
│       └── face_recognition_service.py  # Service for performing face recognition
│
├── data/                      # Directory where face encodings are stored
│   ├── encodings/             # Subdirectory for storing encoded faces
│
├── dlib-19.24.1-cp311-cp311-win_amd64.whl  # Precompiled dlib library for Windows
└── requirements.txt           # Python dependencies
```

## Installation

### Prerequisites

- **Python 3.11**: Ensure you have Python 3.11 installed on your machine.
- **pip**: Ensure `pip` is installed for managing Python packages.

### Step-by-Step Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/AlzheimerFaceRecognition.git
    cd AlzheimerFaceRecognition
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install dlib**:
    Use the precompiled `.whl` file included in the project for Windows:
    ```bash
    python -m pip install dlib-19.24.1-cp311-cp311-win_amd64.whl
    ```

4. **Create Directories**:
    Make sure the required directories for storing encodings are created:
    ```bash
    mkdir -p data/encodings
    ```

## Usage

### Running the Application

To start the FastAPI application, run:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

### Accessing the API

You can access the API documentation and try out the endpoints at:

```
http://127.0.0.1:8010/docs
```

## API Endpoints

### 1. Register Family Member

- **Endpoint**: `/register_image`
- **Method**: `POST`
- **Description**: Register the face of a family member for a specific patient.
- **Request Body**:
    ```json
    {
      "patient_id": "string",
      "family_member_id": "string",
      "idx": "string",
      "image": "file"
    }
    ```
- **Response**:
    ```json
    {
      "status": "Encoding saved successfully",
      "path": "path/to/saved/encoding"
    }
    ```

### 2. Recognize Family Member

- **Endpoint**: `/recognize_faces`
- **Method**: `POST`
- **Description**: Recognize a family member's face from an uploaded image.
- **Request Body**:
    ```json
    {
      "patient_id": "string",
      "image": "file"
    }
    ```
- **Response**:
    ```json
    {
      "recognition_results": [
        {
          "identified_name": "string"
        }
      ]
    }
    ```

### 3. Register Patient

- **Endpoint**: `/register_patient`
- **Method**: `POST`
- **Description**: Register a new patient's face encoding.
- **Request Body**:
    ```json
    {
      "patient_id": "string",
      "image": "file"
    }
    ```
- **Response**:
    ```json
    {
      "status": "Encoding saved successfully",
      "path": "path/to/saved/encoding"
    }
    ```

### 4. Patient Login

- **Endpoint**: `/login_patient`
- **Method**: `POST`
- **Description**: Authenticate a patient based on their facial features.
- **Request Body**:
    ```json
    {
      "image": "file"
    }
    ```
- **Response**:
    ```json
    {
      "status": "Authenticated",
      "patient_id": "string"
    }
    ```

## Detailed Functionality

### Face Registration

- **Family Member Registration**:
    - When a family member's face is registered, the system encodes the face using dlib and stores the encoding in the `data/encodings` directory. 
    - The function `save_encoding_to_file_np` is used to save the encoding as a `.npy` file, ensuring secure and efficient storage.

- **Patient Registration**:
    - Similar to family member registration, the patient's face is encoded and stored in the same format.
    - The system ensures that each patient has a unique directory under `data/encodings`, where their face encoding is stored.

### Face Recognition

- **Family Member Recognition**:
    - The system attempts to match an uploaded image against the registered encodings for a particular patient.
    - The function `find_best_match_for_family` calculates the distances between the uploaded image's encoding and the stored encodings, identifying the best match based on a consensus threshold.

- **Nearest Match Identification**:
    - The function `find_nearest_match` is used during the patient login process. It finds the closest match to the uploaded face encoding, allowing the patient to authenticate securely.

### Patient Login Functionality

- **Login with Facial Recognition**:
    - The login process involves uploading an image, which the system compares against all stored encodings to identify the patient.
    - If a match is found within the threshold, the patient is authenticated successfully.

### Encoding Services

- **Encoding Service**:
    - The `encoding_service.py` module handles all operations related to saving and loading face encodings. This includes functions for saving encodings to `.npy` files and retrieving them for recognition.

- **Face Recognition Service**:
    - The `face_recognition_service.py` module contains the logic for comparing face encodings, including functions for identifying the best match and finding the nearest match.

## Contributing

This project was developed in collaboration with [hazemmonsif](https://github.com/hazemmonsif). Contributions from the community are welcome. If you have suggestions, improvements, or find any issues, feel free to open an issue or submit a pull request on GitHub.


