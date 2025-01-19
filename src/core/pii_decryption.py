from typing import Dict
from src.core.encryption import KeyManager, EncryptionUtils
import logging


def decrypt_pii(record: Dict, metadata_file: str) -> Dict[str, str]:
    """Decrypt PII from a given record using the appropriate keys."""
    encrypted_pii = record.get("encrypted_pii")
    text_with_placeholders = record.get("text_with_placeholders")
    if not encrypted_pii or not text_with_placeholders:
        raise ValueError("Record does not contain valid data.")

    decrypted_pii = {}
    for pii_type, items in encrypted_pii.items():
        decrypted_pii[pii_type] = []
        for item in items:
            key_version = item["key_version"]
            try:
                encryption_key = KeyManager.load_key(key_version, metadata_file)
                logging.info(f"Using key version {key_version}: {encryption_key}")
                decrypted_value = EncryptionUtils.decrypt_data(encryption_key, item["encrypted"])
                decrypted_pii[pii_type].append(decrypted_value)
            except Exception as e:
                logging.error(f"Decryption failed for {pii_type}: {e}")
                raise ValueError(f"Decryption failed. Invalid token for {item['encrypted']}")

    # Reconstruct the original text
    reconstructed_text = text_with_placeholders
    placeholders = {
        "EMAIL": "[EMAIL]",
        "PHONE_NUMBER": "[PHONE_NUMBER]",
        "SOCIAL_SECURITY_NUMBER": "[SOCIAL_SECURITY_NUMBER]",
        "CREDIT_CARD": "[CREDIT_CARD]",
        "ADDRESS": "[ADDRESS]",
        "IP_ADDRESS": "[IP_ADDRESS]",
        "PASSPORT_NUMBER": "[PASSPORT_NUMBER]",
        "NATIONAL_ID": "[NATIONAL_ID]",
    }

    for pii_type, values in decrypted_pii.items():
        placeholder = placeholders.get(pii_type, "[pii]")
        for value in values:
            # Replace the first occurrence of the placeholder with the decrypted value
            reconstructed_text = reconstructed_text.replace(placeholder, value, 1)
            
    # original_text = text_with_hashes
    # for pii_type, values in decrypted_pii.items():
    #     for value, hash_value in zip(values, [EncryptionUtils.hash_data(v) for v in values]):
    #         original_text = original_text.replace(hash_value, value)

    # Increment key usage
    for item in encrypted_pii.values():
        for entry in item:
            KeyManager.increment_key_usage(entry["key_version"])

    return {"reconstructed_text": reconstructed_text, "decrypted_pii": decrypted_pii}




    

  
  