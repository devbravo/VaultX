import logging
from src.core.encryption import EncryptionUtils

logging.basicConfig(level=logging.INFO)

def update_pii_with_reencryption(old_key: bytes, new_key: bytes, new_key_version: str, records: dict):
    """Re-encrypt data in storage and update the key version."""

    # Iterate through records and re-encrypt PII
    for record_id, record in records.items():
        encrypted_pii = record.get("encrypted_pii")
        if not encrypted_pii:
            continue
        
        for pii_type, items in encrypted_pii.items():
            for item in items:
                try:
                    # Decrypt with old key and re-encrypt with the new key
                    decrypted_value = EncryptionUtils.decrypt_data(old_key, item["encrypted"])
                    item["encrypted"] = EncryptionUtils.encrypt_data(new_key, decrypted_value).decode()
                    item["key_version"] = new_key_version  # Update key version
                except Exception as e:
                    logging.error(f"Failed to re-encrypt PII for record {record_id}: {e}")
    return records


# if __name__ == "__main__":
#     old_key, new_key, new_version = KeyRotationManager.rotate_keys(days_threshold=30, usage_threshold=1)
#     update_storage_with_reencryption(old_key, new_key, new_version, "src/db/pii_storage.json")