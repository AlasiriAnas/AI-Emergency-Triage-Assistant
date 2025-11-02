# app/services/nlp_processing.py
"""
NLP Processing Service
----------------------
Uses a Hugging Face model to extract medical entities (symptoms/conditions)
from patient text input.
"""

from transformers import pipeline

# Load a named entity recognition (NER) model
# You can later replace with a medical model like "d4data/biomedical-ner-all"
nlp = pipeline("ner", model="samrawal/bert-base-uncased_clinical-ner", grouped_entities=True)



def extract_symptoms(text: str):
    """
    Extracts medical-related entities (symptoms/conditions) from patient input.
    Cleans up sub-tokens like 'short' + '##ness of breath' → 'shortness of breath'.
    """
    entities = nlp(text)

    merged = []
    current = ""
    for e in entities:
        word = e["word"].replace("##", "")
        if current and not e["word"].startswith("##"):
            merged.append(current.strip())
            current = word
        else:
            current += word if not e["word"].startswith("##") else word
    if current:
        merged.append(current.strip())

    if not merged:
        merged = ["general symptom"]

    return merged

