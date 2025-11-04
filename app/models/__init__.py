# backend/app/models/__init__.py
"""
Do NOT import User or TriageRecord here.

This file only exists to make the models package visible.
Models will be imported in main.py to avoid circular imports.
"""
from app.core.database import Base
