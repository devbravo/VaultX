import re
import logging
from typing import Tuple, Dict, List
from src.core.encryption import EncryptionUtils, KeyManager
from concurrent.futures import ThreadPoolExecutor
from src.core.pii_detection import detect_all_pii

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load or generate encryption key
def load_generate_encryption_key() -> bytes:
    """
    Load the latest encryption key or generate a new one if none exists.
    Returns the encryption key as bytes.
    """
    try:
        metadata = KeyManager.load_keys_metadata()
        
        if not metadata:  # Check if metadata is empty
            logging.info("No metadata found. Generating a new key.")
            new_version = KeyManager.add_new_key()
            encryption_key = KeyManager.get_key(new_version)
            logging.info(f"Initialized with new key: {new_version}")
        else:
            latest_version = max(metadata.keys())  # Get the latest key version
            encryption_key = KeyManager.get_key(latest_version)
            logging.info(f"Using key version: {latest_version}")
    except FileNotFoundError:
        # No metadata file exists; create the first key
        logging.info("Metadata file not found. Generating the first key.")
        new_version = KeyManager.add_new_key()
        encryption_key = KeyManager.get_key(new_version)
        logging.info(f"Initialized with new key: {new_version}")

    return encryption_key
    
    
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
# record_id, processed_text = encrypt_data(text, "src/db/pii_storage.json")
# print("Record ID:", record_id)
# print("Processed Text:", processed_text)