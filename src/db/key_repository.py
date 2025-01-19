import datetime
import logging

from mongoengine import StringField, DateTimeField, IntField, Document

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

class KeyData(Document):
    """
    A document representing one top-level key item, for example:
    {
      "name": "key_1",
      "key_value": "RMwqqDZxKoV...",
      "created": <datetime object>,
      "usage": 61
    }
    """
    name = StringField(required=True, unique=True)   # e.g. "key_1"
    key_value = StringField(required=True)           # e.g. the "key" field
    created = DateTimeField(required=True)           # parsed from string
    usage = IntField(default=0)                      # usage counter

def create_key(name: str, key_str: str, created_str: str, usage: int = 0) -> KeyData:
    """
    Create a new KeyData document.
    :param name: Top-level key name (e.g. "key_1").
    :param key_str: The "key" field value.
    :param created_str: A string representing the creation date (e.g. "2025-01-18 12:12:49").
    :param usage: An integer usage count.
    :return: The newly saved KeyData document.
    """
    # Parse the created date from string
    created_dt = datetime.datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
    new_doc = KeyData(name=name, key_value=key_str, created=created_dt, usage=usage)
    new_doc.save()
    return new_doc

def get_key(name: str) -> KeyData:
    """
    Read (find) a KeyData document by its name.
    :param name: Top-level key name to look up (e.g. "key_1").
    :return: The KeyData document if found, else None.
    """
    return KeyData.objects(name=name).first()

def update_key(name: str, new_key_value: str = None, new_usage: int = None) -> KeyData:
    """
    Update an existing KeyData document. Only updates fields that are not None.
    :param name: Name (e.g. "key_1") of the KeyData document to update.
    :param new_key_value: New 'key_value' if you want to change the stored key.
    :param new_usage: New usage value (an integer).
    :return: The updated document, or None if not found.
    """
    doc = KeyData.objects(name=name).first()
    if doc:
        if new_key_value is not None:
            doc.key_value = new_key_value
        if new_usage is not None:
            doc.usage = new_usage
        doc.save()
        return doc
    return None

def delete_key(name: str) -> bool:
    """
    Delete a KeyData document by name.
    :param name: The top-level key name, e.g. "key_1".
    :return: True if a document was found and deleted, otherwise False.
    """
    doc = KeyData.objects(name=name).first()
    if doc:
        doc.delete()
        return True
    return False
