import face_recognition
import numpy as np
import logging
from app.services.encoding_service import extractid

def find_best_match_for_family(unknown_encoding, known_encodings, distance_threshold=0.6, consensus_threshold=0.8):
    logging.debug("Starting face match process.")
    candidates = {}

    for full_name, encodings_list in known_encodings.items():
        if not encodings_list:
            logging.debug(f"No encodings available for {full_name}")
            continue
        
        # Calculate the distance between known encodings and the unknown encoding
        distances = [np.linalg.norm(encoding - unknown_encoding) for encoding in encodings_list]
        matches = [distance <= distance_threshold for distance in distances]
        match_rate = sum(matches) / len(matches)
        logging.debug(f"{full_name} match rate: {match_rate * 100}% with distances: {distances}")

        # Consider the person if the match rate exceeds the consensus threshold
        if match_rate >= consensus_threshold:
            candidates[full_name] = match_rate

    if candidates:
        best_match = max(candidates, key=candidates.get)
        logging.debug(f"Best match based on consensus is {best_match} with match rate {candidates[best_match] * 100}%")
        return extractid(best_match)

    logging.debug("No matches found meeting the consensus threshold. Returning 'Unknown'.")
    return "Unknown"

def find_nearest_match(unknown_encoding, known_encodings, distance_threshold=0.6):
    best_match_name = "Unknown"
    best_distance = float('inf')

    for name, known_encoding in known_encodings.items():
        # Calculate the distance between the unknown encoding and the known encoding
        distance = np.linalg.norm(known_encoding - unknown_encoding)
        
        if distance < best_distance:
            best_distance = distance
            name_parts = name.split("_")
            if len(name_parts) > 1:
                best_match_name = "_".join(name_parts[1:])
            else:
                best_match_name = name

    if best_distance <= distance_threshold:
        return best_match_name
    else:
        return "Unknown"
