# app/services/nlp_processing.py
"""
NLP Processing Service
----------------------
Extracts medical symptoms/entities from user input.
Uses a clinical NER model if available, otherwise falls back to general NER.
Lazy-loads the model to avoid slow startup.
"""

from typing import List
from transformers import pipeline

_ner_model = None  # Lazy-loaded model cache

def load_model():
    global _ner_model
    if _ner_model is not None:
        return _ner_model

    try:
        _ner_model = pipeline(
            "ner",
            model="samrawal/bert-base-uncased_clinical-ner",
            grouped_entities=True
        )
    except Exception:
        _ner_model = pipeline("ner", grouped_entities=True)

    return _ner_model

def extract_symptoms(text: str) -> List[str]:
    if not text or not text.strip():
        return ["unknown symptom"]

    nlp = load_model()
    entities = nlp(text)

    merged = []
    current = []

    for ent in entities:
        word = ent["word"].replace("##", "")
        if ent.get("entity_group") and current and ent["entity_group"] != current[0][1]:
            merged.append(" ".join(w for w, _ in current))
            current = []
        current.append((word, ent.get("entity_group")))

    if current:
        merged.append(" ".join(w for w, _ in current))

    cleaned = [
        m.strip().lower()
        for m in merged
        if m.strip() and len(m.strip()) > 2
    ]

    if not cleaned:
        cleaned = ["general symptom"]

    return cleaned
