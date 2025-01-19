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
      
# spacy_detector = SpaCyPIIDetector()
# pii_data = spacy_detector.detect_pii("John Doe's SSN is 123-45-6789 and his email is doe@gmail.com, the amount to be paid is $10000")
# print(pii_data)