# app/services/severity_scoring.py
"""
Severity Scoring Service
------------------------
Uses fuzzy logic to map symptoms to severity (1–5) and
also returns a descriptive label (Critical, High, Medium, Low, Minimal).
"""

from thefuzz import fuzz

def calculate_severity(symptoms: list[str]):
    if not symptoms:
        return {
            "priority": 1,
            "label": "Minimal",
            "reasoning": "No clear symptoms provided."
        }

    weights = {
        "chest pain": 5,
        "shortness of breath": 5,
        "bleeding": 5,
        "fainting": 4,
        "headache": 3,
        "fever": 3,
        "vomiting": 3,
        "cough": 2,
        "sore throat": 2,
        "fatigue": 1,
        "dizzy": 2,
    }

    labels = {
        5: "Critical",
        4: "High",
        3: "Medium",
        2: "Low",
        1: "Minimal",
    }

    best_match = None
    best_weight = 1
    best_similarity = 0

    for s in symptoms:
        for ref, weight in weights.items():
            similarity = (fuzz.partial_ratio(s, ref) + fuzz.token_sort_ratio(s, ref)) / 2
            combined_score = (weight * 20) + similarity

            if combined_score > (best_weight * 20 + best_similarity):
                best_weight = weight
                best_match = ref
                best_similarity = similarity

    label = labels.get(best_weight, "Unknown")
    reasoning = f"Detected symptom similar to '{best_match}' (similarity={int(best_similarity)}%) with severity level {best_weight} ({label})."

    return {
        "priority": best_weight,
        "label": label,
        "reasoning": reasoning
    }
