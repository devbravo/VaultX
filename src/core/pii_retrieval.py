import json
from src.core.encryption import EncryptionManager

def retrieve_and_decrypt_pii(record_id, file_path="pii_storage.json"):
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

    # Load encrypted PII
    encrypted_pii = record.get("encrypted_pii")
    text_with_hashes = record.get("text_with_hashes")
    if not encrypted_pii or not text_with_hashes:
        raise ValueError(f"Record {record_id} does not contain valid data.")

    # Decrypt the PII
    decrypted_pii = {key: [EncryptionManager.decrypt_data(EncryptionManager.load_key("encryption_key.txt"), value) for value in values]
                     for key, values in encrypted_pii.items()}
    
    original_text = text_with_hashes
    for key, values in decrypted_pii.items():
        for value, hash_value in zip(values, [EncryptionManager.hash_data(v) for v in values]):
            original_text = original_text.replace(hash_value, value)

    return {"original_text": original_text, "decrypted_pii": decrypted_pii}
  
print(retrieve_and_decrypt_pii("9f15a36c-b3b5-470b-970f-cab506e5ab50"))
  
  