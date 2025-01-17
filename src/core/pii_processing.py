import json
import uuid
from encryption import EncryptionManager
from pii_detection import detect_all_pii

# Generate a predefined encryption key for simplicity
ENCRYPTION_KEY = EncryptionManager.generate_key()
EncryptionManager.save_key(ENCRYPTION_KEY, "encryption_key.txt")


def process_text_and_store_in_file(text, file_path="pii_storage.json"):
    # Step 1: Detect PII
    pii_data = detect_all_pii(text)

    # Step 2: Encrypt PII
    encrypted_pii = {key: [EncryptionManager.encrypt_data(ENCRYPTION_KEY, value) for value in values]
                     for key, values in pii_data.items()}

    # Step 3: Replace PII with hashes
    text_with_hashes = text
    for key, values in pii_data.items():
        for value in values:
            hashed_value = EncryptionManager.hash_data(value)
            text_with_hashes = text_with_hashes.replace(value, hashed_value)

    # Step 4: Store in a JSON file
    record_id = str(uuid.uuid4())
    new_record = {
        "text_with_hashes": text_with_hashes,
        "encrypted_pii": {key: [encrypted.decode() for encrypted in values] for key, values in encrypted_pii.items()}
    }

    try:
        with open(file_path, "r") as f:
            storage_data = json.load(f)
    except FileNotFoundError:
        storage_data = {}  # Initialize if file doesn't exist

    # Step 6: Add the new record
    storage_data[record_id] = new_record

    # Step 7: Write back to the JSON file
    with open(file_path, "w") as f:
        json.dump(storage_data, f, indent=4)

    return record_id, text_with_hashes
  
text = "Contact me at john.doe@example.com or +1-123-456-7890. My SSN is 123-45-6789."
processed_text = process_text_and_store_in_file(text)

print("Processed Text:", processed_text)