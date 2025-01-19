import re
import logging
from typing import Tuple, Dict, List
from src.core.encryption import EncryptionUtils, KeyManager
from concurrent.futures import ThreadPoolExecutor
from src.core.pii_detection.pii_detection import PiiDetectionPipeline
from src.db.key_repository import load_generate_encryption_key

# Configure logging
logging.basicConfig(level=logging.INFO)

    
def encryption(pii_data: Dict[str, List[str]], 
                key: bytes, key_version: str) -> Dict[str, List[Dict[str, str]]]:
    encrypted_pii = {}
    with ThreadPoolExecutor() as executor:
        for pii_type, values in pii_data.items():
            encrypted_pii[pii_type] = [
                {"encrypted": encrypted.decode(), "key_version": key_version}
                for encrypted in executor.map(lambda value: EncryptionUtils.encrypt_data(key, value), values)
            ]
    return encrypted_pii
  

def encrypt_pii(text: str) -> Tuple[str, Dict]:
    """Detect PII in text and encrypt it."""
    # Detect PII
    pii_detection_pipeline = PiiDetectionPipeline()
    pii_data = pii_detection_pipeline.detect_all_pii(text)
    merged_pii = pii_detection_pipeline.merge_pii_data(pii_data["regex_results"], pii_data["spacy_results"])
    
    print('PII', pii_data)
    logging.info(f"Detected PII: {pii_data}")
    print("PII_detection", pii_data)
    
    if not pii_data:
      logging.info("No PII detected. Skipping encryption.")
      return None, None
      

    # Load or generate the latest encryption key
    encryption_key = load_generate_encryption_key()
    latest_metadata = KeyManager.load_keys_metadata()
    latest_version = max(latest_metadata.keys())  # Get the latest key version

    # Encrypt PII
    encrypted_pii = encryption(merged_pii, encryption_key, latest_version)
    
    masked_text = pii_data['masked_text']

    return masked_text, encrypted_pii
  