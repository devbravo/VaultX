"""
SpaCy-based PII Detection Module

This module provides functionality to detect Personally Identifiable Information (PII) 
using SpaCy's Named Entity Recognition (NER) capabilities. It specifically includes 
mechanisms to exclude placeholders that may interfere with PII detection.
"""

import spacy
from typing import Dict, List
import re


class SpaCyPIIDetector:
  def __init__(self):
    self.nlp = spacy.load("en_core_web_sm")
    self.exclude_pattern = r"__PLACEHOLDER_\d+__"  # Regex to match placeholders

  def detect_pii(self, text: str) -> Dict[str, List[str]]:
    doc = self.nlp(text)
    entities = {}
    for ent in doc.ents:
      # Skip placeholders
      if not re.match(self.exclude_pattern, ent.text):
        label = "NAME" if ent.label_ == "PERSON" else ent.label_
        entities.setdefault(label, []).append(ent.text)
    return entities
