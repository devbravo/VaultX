import logging
from datetime import datetime
from src.core.encryption import KeyManager, KeyRotationManager, EncryptionUtils

logging.basicConfig(level=logging.INFO)

def simulate_reencrypt_data(old_key: bytes, new_key: bytes):
    # Example data to simulate re-encryption
    test_data = [
        "john.doe@example.com",
        "+1-123-456-7890",
        "123-45-6789"
    ]

    # Encrypt with the old key
    encrypted_data = [
        EncryptionUtils.encrypt_data(old_key, item) for item in test_data
    ]

    # Decrypt with the old key and re-encrypt with the new key
    reencrypted_data = [
        EncryptionUtils.encrypt_data(new_key, EncryptionUtils.decrypt_data(old_key, item))
        for item in encrypted_data
    ]

    # Log the results
    for original, encrypted, reencrypted in zip(test_data, encrypted_data, reencrypted_data):
        logging.info(f"Original: {original}")
        logging.info(f"Encrypted with Old Key: {encrypted}")
        logging.info(f"Re-encrypted with New Key: {reencrypted}")

if __name__ == "__main__":
    # Call the KeyRotationManager to handle rotation and simulate re-encryption
    def rotation_with_reencryption():
        metadata = KeyManager.load_keys_metadata()
        for key_version, key_info in metadata.items():
            if KeyRotationManager.should_rotate_key(key_info, days_threshold=30, usage_threshold=100):
                old_key = KeyManager.get_key(key_version)
                new_version = KeyManager.add_new_key()
                new_key = KeyManager.get_key(new_version)
                logging.info(f"Rotating key: {key_version} -> {new_version}")
                simulate_reencrypt_data(old_key, new_key)

    rotation_with_reencryption()