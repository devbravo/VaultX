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
      

def compile_pii_pattern(pii_data: Dict[str, List[str]]) -> re.Pattern:
    pii_values = [value for values in pii_data.values() for value in values]
    return re.compile(r"|".join(re.escape(value) for value in pii_values))
  

def replace_pii_with_hash(text: str, pii_data: Dict[str, List[str]]) -> str:
    pattern = compile_pii_pattern(pii_data)

    def replacer(match):
        return EncryptionUtils.hash_data(match.group(0))

    return pattern.sub(replacer, text)
  

def encrypt_pii(text: str) -> Tuple[str, Dict]:
    """Detect PII in text and encrypt it."""
    # Detect PII
    pii_data = detect_all_pii(text)
    logging.info(f"Detected PII: {pii_data}")
    print("PII_detection")

    # Load or generate the latest encryption key
    encryption_key = load_generate_encryption_key()
    latest_metadata = KeyManager.load_keys_metadata()
    latest_version = max(latest_metadata.keys())  # Get the latest key version

    # Encrypt PII
    encrypted_pii = encryption(pii_data, encryption_key, latest_version)

    # Replace PII with hashes
    text_with_hashes = replace_pii_with_hash(text, pii_data)

    return text_with_hashes, encrypted_pii
  
  
# # Example usage
# text = "Contact me at john.doe@example.com or +1-123-456-7890. My SSN is 123-45-6789."
# record_id, processed_text = encrypt_pii(text)
# print("Record ID:", record_id)
# print("Processed Text:", processed_text)