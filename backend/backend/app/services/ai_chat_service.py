from app.services.nlp_processing import extract_symptoms
from app.services.severity_scoring import calculate_severity

def analyze_patient_input(user_input: str):
    """
    Uses NLP to extract entities and calculate severity.
    """
    detected = extract_symptoms(user_input)
    severity = calculate_severity(detected)

    return {
        "detected_symptoms": detected,
        "severity": severity
    }
