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
    Extracts named entities (symptoms/conditions) from patient input.
    """
    entities = nlp(text)
    extracted = [entity["word"].lower() for entity in entities]

    if not extracted:
        extracted = ["general symptom"]

    return extracted
