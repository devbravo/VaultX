import re
import logging
from typing import Tuple, Dict, List
from src.core.encryption import EncryptionUtils, KeyManager
from concurrent.futures import ThreadPoolExecutor
from src.core.pii_detection import detect_all_pii
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
      

def replace_pii_with_placeholder(text: str, pii_data: Dict[str, List[str]]) -> str:
    """Replace PII with placeholders in the given text."""
    placeholders = {
        "emails": "[email]",
        "phone_numbers": "[phone-number]",
        "ssns": "[ssn]",
        "credit_cards": "[credit-card]",
        "addresses": "[address]",
        "ips": "[ip]",
        "passport_numbers": "[passport]",
    }

    for pii_type, values in pii_data.items():
        placeholder = placeholders.get(pii_type, "[pii]")  # Default placeholder for unknown types
        for value in values:
            pattern = re.escape(value)
            text = re.sub(pattern, placeholder, text)

    return text
  

def encrypt_pii(text: str) -> Tuple[str, Dict]:
    """Detect PII in text and encrypt it."""
    # Detect PII
    pii_data = detect_all_pii(text)
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
    encrypted_pii = encryption(pii_data, encryption_key, latest_version)

    # Replace PII with hashes
    text_with_placeholder = replace_pii_with_placeholder(text, pii_data)

    return text_with_placeholder, encrypted_pii
  