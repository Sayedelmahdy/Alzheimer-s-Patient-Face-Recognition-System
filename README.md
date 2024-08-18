# Alzheimer's Patient Face Recognition System

This project is a specialized face recognition system designed to assist Alzheimer's patients in recognizing their loved ones and authenticating their identities using facial recognition technology. The system was developed by **Hazem Monsif** and **[Your Name]** to improve the quality of life for Alzheimer's patients and reduce the burden on caregivers by leveraging advanced AI and machine learning techniques.

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

## Overview

This system was developed with the primary goal of aiding Alzheimer's patients by allowing them to recognize family members and authenticate themselves through facial recognition. Built using FastAPI, this application provides an intuitive API interface for registering and recognizing faces, offering a secure and user-friendly experience.

## Features

- **Family Member Registration**: Register a family member’s face for easy recognition.
- **Patient Login**: Patients can authenticate themselves using facial recognition.
- **Face Recognition**: High-accuracy facial recognition system based on advanced machine learning models.
- **Secure Storage**: Face encodings are stored securely as `.npy` files.

## Project Structure

\`\`\`plaintext
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
\`\`\`

## Installation

### Prerequisites

- **Python 3.11**: Ensure Python 3.11 is installed.
- **pip**: Ensure `pip` is installed for managing Python packages.

### Step-by-Step Installation

1. **Clone the Repository**:
    \`\`\`bash
    git clone https://github.com/yourusername/AlzheimerFaceRecognition.git
    cd AlzheimerFaceRecognition
    \`\`\`

2. **Install Dependencies**:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

3. **Install dlib**:
    Install the precompiled `.whl` file for Windows:
    \`\`\`bash
    python -m pip install dlib-19.24.1-cp311-cp311-win_amd64.whl
    \`\`\`

4. **Create Directories**:
    Create necessary directories for storing face encodings:
    \`\`\`bash
    mkdir -p data/encodings
    \`\`\`

## Usage

### Running the Application

To start the FastAPI application:

\`\`\`bash
uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
\`\`\`

### Accessing the API

API documentation and interactive testing are available at:

\`\`\`
http://127.0.0.1:8010/docs
\`\`\`

## API Endpoints

### 1. Register Family Member

- **Endpoint**: \`/register_image\`
- **Method**: \`POST\`
- **Description**: Register a family member's face under a specific patient ID.
- **Request Body**:
    \`\`\`json
    {
      "patient_id": "string",
      "family_member_id": "string",
      "idx": "string",
      "image": "file"
    }
    \`\`\`
- **Response**:
    \`\`\`json
    {
      "status": "Encoding saved successfully",
      "path": "path/to/saved/encoding"
    }
    \`\`\`

### 2. Recognize Family Member

- **Endpoint**: \`/recognize_faces\`
- **Method**: \`POST\`
- **Description**: Recognize family members' faces from an uploaded image for a specific patient.
- **Request Body**:
    \`\`\`json
    {
      "patient_id": "string",
      "image": "file"
    }
    \`\`\`
- **Response**:
    \`\`\`json
    {
      "recognition_results": [
        {
          "identified_name": "string"
        }
      ]
    }
    \`\`\`

### 3. Register Patient

- **Endpoint**: \`/register_patient\`
- **Method**: \`POST\`
- **Description**: Register a new patient's face encoding.
- **Request Body**:
    \`\`\`json
    {
      "patient_id": "string",
      "image": "file"
    }
    \`\`\`
- **Response**:
    \`\`\`json
    {
      "status": "Encoding saved successfully",
      "path": "path/to/saved/encoding"
    }
    \`\`\`

### 4. Patient Login

- **Endpoint**: \`/login_patient\`
- **Method**: \`POST\`
- **Description**: Authenticate a patient based on their facial features.
- **Request Body**:
    \`\`\`json
    {
      "image": "file"
    }
    \`\`\`
- **Response**:
    \`\`\`json
    {
      "status": "Authenticated",
      "patient_id": "string"
    }
    \`\`\`

## Detailed Functionality

### Face Registration

- **Family Member Registration**:
    - The system encodes a family member's face using the HOG (Histogram of Oriented Gradients) model provided by the `face_recognition` library. HOG is preferred for this system due to its balance between speed and accuracy, especially on devices with limited computational power. Although CNN (Convolutional Neural Networks) offers higher accuracy, it requires more computational resources, making it less suitable for real-time applications on standard hardware.
    - The face encoding is then stored securely as a `.npy` file in the `data/encodings` directory, using the `save_encoding_to_file_np` function. This ensures that the encoding can be quickly retrieved and used for future recognition tasks.

- **Patient Registration**:
    - Patient registration follows a similar process. The patient’s face is encoded and stored, ensuring that each patient has a unique directory under `data/encodings` where their encoding is kept. This is crucial for accurate and efficient recognition.

### Face Recognition

- **Family Member Recognition**:
    - When recognizing a family member, the system compares the uploaded image's encoding with the stored encodings for that patient. The function `find_best_match_for_family` calculates the Euclidean distances between the uploaded encoding and the stored encodings.
    - A consensus threshold is applied to determine the best match. If the majority of encodings for a family member fall within a certain distance threshold, that family member is recognized as the best match.

- **Nearest Match Identification**:
    - During patient login, the `find_nearest_match` function is used. This function searches for the closest encoding in the stored data, allowing for accurate patient identification even if the patient’s appearance has slightly changed.

### Patient Login Functionality

- **Login with Facial Recognition**:
    - The login process is streamlined to ensure ease of use for Alzheimer's patients. The patient uploads an image, which the system compares against all stored encodings to find the closest match.
    - The system then returns whether the patient is authenticated based on the closest match found within the specified threshold. This approach balances security with usability, ensuring that patients can log in easily while maintaining a high level of accuracy.

### Encoding Services

- **Encoding Service**:
    - The `encoding_service.py` module is central to the system's operation, handling all tasks related to saving and loading face encodings. The module includes functions for saving face encodings as `.npy` files, which are lightweight and easy to manage.
    - The module also includes functions for loading encodings from the filesystem, making them available for recognition tasks. By abstracting these operations into a dedicated service, the system maintains a clean separation of concerns, improving maintainability and scalability.

- **Face Recognition Service**:
    - The `face_recognition_service.py` module encapsulates the core logic for face recognition. It provides functions to calculate the best match for a family member and to find the nearest match for a patient during login.
    - By isolating the recognition logic in a service module, the system ensures that recognition processes are efficient and can be easily tested and modified.

## Contributing

This project was developed in collaboration with [hazemmonsif](https://github.com/hazemmonsif). Contributions from the community are welcome. If you have suggestions, improvements, or find any issues, feel free to open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. For more details, refer to the [LICENSE](LICENSE) file.
