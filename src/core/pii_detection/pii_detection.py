"""
PII Detection Pipeline Module

This module integrates regex-based PII detection and SpaCy-based Named Entity Recognition (NER)
for comprehensive identification and masking of Personally Identifiable Information (PII). It also
provides support for integrating a Language Model (LLM) for advanced PII detection.
"""

from typing import Tuple, Dict, List
from src.core.pii_detection.pii_regex import detect_pii_regex
from src.core.pii_detection.pii_spacy import SpaCyPIIDetector

class PiiDetectionPipeline:
    def __init__(self):
      self.spacy_pii = SpaCyPIIDetector()

    def detect_with_regex(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """Use regex-based PII detection."""
        detected_pii = detect_pii_regex(text)
        for label, matches in detected_pii.items():
            for match in matches:
                text = text.replace(match, f"[{label}]")  # Mask detected PII
        return text, detected_pii

    def preprocess_for_spacy(self, text: str, placeholders: List[str]) -> Tuple[str, Dict[str, str]]:
      """Temporarily replace placeholders with empty strings to avoid interference."""
      placeholder_map = {}
      for i, placeholder in enumerate(placeholders):
          marker = f"__PLACEHOLDER_{i}__"
          placeholder_map[placeholder] = marker
          text = text.replace(placeholder, "")  # Remove placeholders
      return text, placeholder_map
  
      
    def postprocess_from_spacy(self, spacy_results: Dict[str, List[str]], placeholder_map: Dict[str, str]) -> Dict[str, List[str]]:
      """Revert markers back to original placeholders in spacy_results."""
      reverted_results = {}
      for label, entities in spacy_results.items():
          reverted_entities = []
          for entity in entities:
              replaced = False
              for placeholder, marker in placeholder_map.items():
                  if marker in entity:
                      # Replace the marker with the placeholder
                      entity = entity.replace(marker, placeholder)
                      replaced = True
              # Add the entity (reverted or original) to the list
              reverted_entities.append(entity if replaced else entity)

          reverted_results[label] = reverted_entities
      return reverted_results
    

    def detect_with_spacy(self, text: str, exclude_labels: List[str]) -> Dict[str, List[str]]:
        """Detect PII using spaCy while skipping placeholders."""
        text, placeholder_map = self.preprocess_for_spacy(text, exclude_labels)
        spacy_results = self.spacy_pii.detect_pii(text)
        spacy_results = self.postprocess_from_spacy(spacy_results, placeholder_map)
  
        return spacy_results

    def detect_all_pii(self, text: str) -> Dict[str, Dict]:
        """Run the full detection pipeline: regex first, then SpaCy."""
        masked_text, regex_results = self.detect_with_regex(text)

        placeholders = [f"[{label}]" for label in regex_results.keys()]
        spacy_results = self.detect_with_spacy(masked_text, placeholders)

        for label, entities in spacy_results.items():
            for entity in entities:
                if entity not in placeholders:  # Ensure placeholders are not re-masked
                    masked_text = masked_text.replace(entity, f"[{label}]")

        # Combine results
        return {
            "regex_results": regex_results,
            "spacy_results": spacy_results,
            "masked_text": masked_text,
        }
        
    def merge_pii_data(self, regex_results: Dict[str, List[str]], spacy_results: Dict[str, List[str]]) -> Dict[str, List[str]]:
      """Merge regex and spaCy PII detection results."""
      merged_data = regex_results.copy()
      for key, values in spacy_results.items():
        if key in merged_data:
            merged_data[key].extend(values)  # Combine lists if key exists
        else:
          merged_data[key] = values
      return merged_data

test_list = [
            "HI John Doe, Call me at +5978144939 or send an email to alice@company.co.uk. Also, my social security number is 987-65-4321."
            "John Doe's social security number is 123-45-6789, his email is john.doe@example.com, and his phone is +5978100000.",
             f"Jane’s social security number is 123-45-6789, her credit card is 4111-1111-1111-1111, and she lives in California.", 
             f"Robert Johnson sent a payment of $10,000 yesterday.", 
             f"Contact Priya at priya.123@example.co.in or call her on +91 9876543210",
             f"My internet protocol address is 192.168.0.1, and my passport number is A12345678",
             f"Call me at +44 20 7946 0958 or send an email to alice@company.co.uk. Also, my social security number is 987-65-4321.",
             f"John’s account number is 12345678, not 87654321, and his phone is 555-5555.",
             f"My bank details are top secret and not for sharing.",
             f"Reach out to +5978000000 for assistance or visit the website www.example.com",
             f"Hi, I’m Sara. Call me at 9876543210 or email me at sara@gmail.com. Let’s meet tomorrow.",
             f"123-45-6789"
             ]

      
### LMM PII DETECTION
# async def detect_pii_llm(text: str):
#     llm = ChatOpenAI(model="gpt-4o-mini")
#
#     class PII(BaseModel):
#         telephone_number: Optional[str]
#         email_address: Optional[str]
#         ssn: Optional[str]
#         credit_card_number: Optional[str]
#         date: Optional[str]
#         ip_address: Optional[str]
#         passport_number: Optional[str]
#         national_id: Optional[str]
#
#     structured_llm = llm.with_structured_output(PII)
#
#     system_prompt = """
#         Given the following text, identify any personally identifiable information (PII)
#         such as email addresses, phone numbers, social security numbers, credit card numbers,
#         dates, IP addresses, passport numbers, and national IDs.
#     """
#
#     pii_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system_prompt),
#             ("user", text),
#         ]
#     )
#
#     pii_setter = pii_prompt | structured_llm
#     pii = await pii_setter.ainvoke(text)

