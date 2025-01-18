from typing import Dict
from src.core.encryption import KeyManager, EncryptionUtils


def decrypt_pii(record: Dict, metadata_file: str) -> Dict[str, str]:
    """Decrypt PII from a given record using the appropriate keys."""
    encrypted_pii = record.get("encrypted_pii")
    text_with_hashes = record.get("text_with_hashes")
    if not encrypted_pii or not text_with_hashes:
        raise ValueError("Record does not contain valid data.")

    decrypted_pii = {}
    for pii_type, items in encrypted_pii.items():
        decrypted_pii[pii_type] = []
        for item in items:
            key_version = item["key_version"]
            try:
                encryption_key = KeyManager.load_key(key_version, metadata_file)
                print(f"Using key version {key_version}: {encryption_key}")
                decrypted_value = EncryptionUtils.decrypt_data(encryption_key, item["encrypted"])
                decrypted_pii[pii_type].append(decrypted_value)
            except Exception as e:
                print(f"Decryption failed for {pii_type}: {e}")
                raise ValueError(f"Decryption failed. Invalid token for {item['encrypted']}")

    # Reconstruct the original text
    original_text = text_with_hashes
    for pii_type, values in decrypted_pii.items():
        for value, hash_value in zip(values, [EncryptionUtils.hash_data(v) for v in values]):
            original_text = original_text.replace(hash_value, value)

    # Increment key usage
    for item in encrypted_pii.values():
        for entry in item:
            KeyManager.increment_key_usage(entry["key_version"])

    return {"original_text": original_text, "decrypted_pii": decrypted_pii}


# if __name__ == "__main__":
#   record_id = ""

#   # Open the JSON file
#   with open("src/db/pii_storage.json", "r") as f:
#       data = json.load(f)

#   # Dynamically retrieve the first UUID key
#   if data:
#       record_id = next(iter(data))  # Get the first key from the dictionary
#       print(f"Retrieved UUID: {record_id}")
#       print("Record for UUID:", data[record_id])
#   else:
#       print("No data found in the JSON file.")
      
      
#   file_path = "src/db/pii_storage.json"
#   metadata_file = "src/db/keys_metadata.json"
#   record = get_record_by_id(record_id, file_path)
#   print(decrypt_pii(record, metadata_file))




    

  
  