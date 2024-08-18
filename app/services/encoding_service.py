import numpy as np
import os

def save_encoding_to_file_np(encoding, output_file_path):
    np.save(output_file_path, encoding)

def load_encodings_from_folder(folder_path):
    encodings = {}
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".npy"):
                file_path = os.path.join(root, file_name)
                encodings[file_name[:-4]] = np.load(file_path)
    return encodings

def load_encodings_from_folderForFamily(folder_path):
    encodings = {}
    for root, dirs, files in os.walk(folder_path):
        encodings[os.path.basename(root)] = [np.load(os.path.join(root, file)) for file in files if file.endswith(".npy")]
    return encodings

def extractid(name):
    parts = name.split('_')
    if len(parts) > 1:
        return parts[1]
    return None
