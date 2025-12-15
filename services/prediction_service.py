import json
import os
from utils.file_ops import append_prediction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_PATH = os.path.join(BASE_DIR, "exported_db_files", "disease_symptom_mapping.json")

with open(MAP_PATH, "r") as f:
    DISEASE_MAP = json.load(f)


def predict_disease_from_symptoms(symptom_list, username=None, top_n=3):
    clean_list = [s.strip().lower() for s in symptom_list]
    results = []

    for disease, symptoms in DISEASE_MAP.items():
        matched = set(clean_list) & set(symptoms)

        if matched:
            confidence = int((len(matched) / len(symptoms)) * 100)
            results.append({
                "disease": disease,
                "confidence": f"{confidence}%",
                "matched_symptoms": list(matched)
            })

    if not results:
        results.append({
            "disease": "No matching disease found",
            "confidence": "0%",
            "matched_symptoms": []
        })

    results = sorted(results, key=lambda x: int(x["confidence"][:-1]), reverse=True)

    if username:
        append_prediction(username, clean_list, results[0]["disease"])

    return results[:top_n]
