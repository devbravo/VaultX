import json
import logging
from datetime import datetime
from src.core.encryption import KeyManager, EncryptionUtils
from src.core.key_rotation import KeyRotationManager

logging.basicConfig(level=logging.INFO)

def update_storage_with_reencryption(old_key: bytes, new_key: bytes, new_key_version: str, file_path: str):
    """Re-encrypt data in storage and update the key version."""
    try:
        # Load the current storage file
        with open(file_path, "r") as f:
            storage_data = json.load(f)
    except FileNotFoundError:
        logging.error("Storage file not found.")
        return

    # Iterate through records and re-encrypt PII
    for record_id, record in storage_data.items():
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

    # Write back the updated data
    try:
        with open(file_path, "w") as f:
            json.dump(storage_data, f, indent=4)
        logging.info("Storage file updated with new key version.")
    except Exception as e:
        logging.error(f"Failed to update storage file: {e}")


if __name__ == "__main__":
    def rotation_with_reencryption():
        old_key, new_key, new_version = KeyRotationManager.rotate_keys(days_threshold=30, usage_threshold=1)
        update_storage_with_reencryption(old_key, new_key, new_version, "src/db/pii_storage.json")

    rotation_with_reencryption()