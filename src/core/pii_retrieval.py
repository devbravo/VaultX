import json
from src.core.encryption import EncryptionUtils, KeyManager
from typing import Dict

def retrieve_and_decrypt_pii(record_id: str, file_path: str, metadata_file: str) -> Dict[str, str]:
    """Retrieve and decrypt PII from a JSON file."""
    # Load the JSON file
    try:
        with open(file_path, "r") as f:
            storage_data = json.load(f)
    except FileNotFoundError:
        raise ValueError("Storage file not found.")
    
    # Find the record by ID
    record = storage_data.get(str(record_id))
    if not record:
        raise ValueError(f"No record found with ID {record_id}")

    # Load encrypted PII and text_with_hashes
    encrypted_pii = record.get("encrypted_pii")
    text_with_hashes = record.get("text_with_hashes")
    if not encrypted_pii or not text_with_hashes:
        raise ValueError(f"Record {record_id} does not contain valid data.")
      
    # encryption_key = KeyManager.get_key(key_version)

    # Decrypt the PII using correct keys
    decrypted_pii = {}
    for pii_type, items in encrypted_pii.items():
        decrypted_pii[pii_type] = []
        for item in items:
            key_version = item["key_version"]
            try: 
              encryption_key = KeyManager.load_key(key_version, metadata_file)
              print(f"Using key version {key_version}: {encryption_key}")
              decrypted_value = EncryptionUtils.decrypt_data(encryption_key, item["encrypted"])
              print('Encryption key', encryption_key)
            except Exception as e:
                print(f"Decryption failed for {pii_type}: {e}")
                raise ValueError(f"Decryption failed. Invalid token for {item['encrypted']}")
          
            decrypted_pii[pii_type].append(decrypted_value)
            
    KeyManager.increment_key_usage(key_version)

    # Reconstruct the original text
    original_text = text_with_hashes
    for pii_type, values in decrypted_pii.items():
        for value, hash_value in zip(values, [EncryptionUtils.hash_data(v) for v in values]):
            original_text = original_text.replace(hash_value, value)

    return {"original_text": original_text, "decrypted_pii": decrypted_pii}
  
uuid = "2e61d4f5-8187-4a46-959c-efc448b55fd9"
file_path = "src/db/pii_storage.json"
key_file_path = "src/db/keys_metadata.json"

print(retrieve_and_decrypt_pii(uuid, file_path, key_file_path ))




    

  
  