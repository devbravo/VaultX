import logging
from src.core.encryption import KeyManager


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