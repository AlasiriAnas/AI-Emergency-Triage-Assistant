# app/services/ai_chat_service.py

"""
AI-assisted symptom analysis helper.
Used BEFORE final LLM triage to extract structured medical hints.
"""

from typing import Dict, Any
from app.services.nlp_processing import extract_symptoms
from app.services.severity_scoring import calculate_severity

def process_patient_input(user_input: str) -> Dict[str, Any]:
    """
    Extract symptoms from user text and estimate rough severity level.
    This is a helper for your triage flow — not the final medical decision.
    """
    if not user_input or not user_input.strip():
        return {
            "symptoms": [],
            "duration": "",
            "risk_factors": [],
            "severity_guess": "Low",
        }

    symptoms = extract_symptoms(user_input)
    severity_guess = calculate_severity(symptoms)

    return {
        "symptoms": symptoms,
        "duration": "",
        "risk_factors": [],
        "severity_guess": severity_guess,
    }
