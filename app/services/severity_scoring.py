# app/services/severity_scoring.py

"""
Severity Scoring Service
------------------------
Maps free-text symptom list to an ER triage severity label.
This is a heuristic pre-classifier — the LLM will finalize triage.
"""

from typing import List
from thefuzz import fuzz

WEIGHTS = {
    "chest pain": 5,
    "shortness of breath": 5,
    "difficulty breathing": 5,
    "unconscious": 5,
    "severe bleeding": 5,
    "stroke": 5,
    "weakness one side": 5,
    "seizure": 5,

    "fainting": 4,
    "severe headache": 4,
    "severe pain": 4,
    "abdominal pain": 4,
    "high fever": 4,
    "vomiting blood": 4,

    "moderate pain": 3,
    "fever": 3,
    "vomiting": 3,
    "dehydration": 3,

    "cough": 2,
    "sore throat": 2,
    "dizzy": 2,
    "fatigue": 1,
}

SEVERITY_LABELS = {
    5: "Critical",
    4: "High",
    3: "Medium",
    2: "Low",
    1: "Low",
}

def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = text.lower().strip()

    arabic_map = {
        "الم": "pain",
        "صداع": "headache",
        "دوخه": "dizzy",
        "دوار": "dizzy",
        "الام": "pain",
        "الم الصدر": "chest pain",
        "ضيق تنفس": "shortness of breath",
        "نزيف": "bleeding",
        "اغماء": "fainting",
        "ترجيع": "vomiting",
        "حمى": "fever",
    }
    for k, v in arabic_map.items():
        if k in t:
            t = v

    return t

def calculate_severity(symptoms: List[str]) -> str:
    if not symptoms:
        return "Low"

    best_score = 0
    best_weight = 1

    for symptom in symptoms:
        s_norm = normalize_text(symptom)

        for ref, weight in WEIGHTS.items():
            similarity = (fuzz.partial_ratio(s_norm, ref) + fuzz.token_sort_ratio(s_norm, ref)) / 2
            combined_score = (weight * 20) + similarity

            if combined_score > best_score:
                best_score = combined_score
                best_weight = weight

    return SEVERITY_LABELS.get(best_weight, "Low")
