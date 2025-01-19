import spacy

class SpaCyPIIDetector:
    def __init__(self, model: str = "en_core_web_sm"):
        self.nlp = spacy.load(model)

    def detect_pii(self, text: str):
        """Detect PII using SpaCy NER."""
        doc = self.nlp(text)
        pii_entities = {}

        for ent in doc.ents:
            if ent.label_ in {"PERSON", "DATE", "TIME", "MONEY"}:
                pii_entities.setdefault(ent.label_, []).append(ent.text)

        return pii_entities
      
spacy_detector = SpaCyPIIDetector()
pii_data = spacy_detector.detect_pii("John Doe's SSN is 123-45-6789 and his email is doe@gmail.com, the amount to be paid is $10000")
print(pii_data)