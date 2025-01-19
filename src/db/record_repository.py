import json
import logging
import uuid
from typing import Dict, Any

from mongoengine import EmbeddedDocument, StringField, EmbeddedDocumentListField, Document, EmbeddedDocumentField

logging.basicConfig(level=logging.INFO)


def store_record_by_id(file_path: str, text_with_placeholders: str, encrypted_pii: Dict) -> str:
    """Store a new record in the storage file."""

    record_id = str(uuid.uuid4())

    new_record = {
        "text_with_placeholders": text_with_placeholders,
        "encrypted_pii": encrypted_pii  # Store with key versions
    }
    # Since we are using json as a storage format, we need to load the existing data first
    try:
        with open(file_path, "r") as f:
            storage_data = json.load(f)
    except FileNotFoundError:
        storage_data = {}
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {file_path}")

    # Add new record
    storage_data[record_id] = new_record

    # Save updated data
    try:
        with open(file_path, "w") as f:
            json.dump(storage_data, f, indent=4)
            logging.info(f"Stored record with ID: {record_id}")
    except Exception as e:
        logging.error(f"Failed to store record with ID: {record_id}")
        raise e

    logging.info(f"Processed text stored with Record ID: {record_id}")

    return record_id


def store_all_records(file_path: str, records: Dict) -> None:
    """Store all records in the storage file."""
    try:
        with open(file_path, "w") as f:
            json.dump(records, f, indent=4)
        logging.info("Storage file updated with new key version.")
    except Exception as e:
        raise ValueError(f"Failed to update storage file: {e}")


def get_record_by_id(record_id: str, file_path: str) -> Dict:
    """Retrieve a specific record by ID from the storage file."""
    try:
        with open(file_path, "r") as f:
            storage_data = json.load(f)
    except FileNotFoundError:
        raise ValueError("Storage file not found.")

    # Find the record by ID
    record = storage_data.get(str(record_id))
    if not record:
        raise ValueError(f"No record found with ID {record_id}")

    return record


def get_all_records(file_path: str) -> Dict:
    """Retrieve all records from the storage file."""
    try:
        with open(file_path, "r") as f:
            storage_data = json.load(f)
    except FileNotFoundError:
        raise ValueError("Storage file not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {file_path}")

    return storage_data


class PIIEntry(EmbeddedDocument):
    """
    Represents a single piece of encrypted PII, e.g.:
    {
      "encrypted": "gAAAAABni8TxmpZRRXiH...",
      "key_version": "key_1"
    }
    """
    encrypted = StringField(required=True)
    key_version = StringField(required=True)


class EncryptedPII(EmbeddedDocument):
    """
    Holds the arrays of PIIEntry objects:
    {
      "emails": [...],
      "phone_numbers": [...],
      "ssns": [...]
    }
    """
    emails = EmbeddedDocumentListField(PIIEntry, default=[])
    phone_numbers = EmbeddedDocumentListField(PIIEntry, default=[])
    ssns = EmbeddedDocumentListField(PIIEntry, default=[])


######################################
#   3. Define the Main DataRecord    #
######################################

class DataRecord(Document):
    """
    The main document:
    {
      "record_id": "002af585-03cc-4bf9-9f9d-d9543795242d",
      "text_with_hashes": "...",
      "encrypted_pii": {
         "emails": [...],
         "phone_numbers": [...],
         "ssns": [...]
      }
    }
    """
    # We store the UUID-like string as the primary key (or you can use ObjectId).
    record_id = StringField(primary_key=True)
    text_with_hashes = StringField()
    encrypted_pii = EmbeddedDocumentField(EncryptedPII)


########################
#   4. CRUD Functions  #
########################

def create_data_record(
        record_id: str,
        text_with_hashes: str,
        encrypted_pii_data: Dict[str, Any]
) -> DataRecord:
    """
    Create and save a new DataRecord to MongoDB.

    :param record_id: The UUID-like string (e.g. "002af585-03cc-4bf9-9f9d-d9543795242d").
    :param text_with_hashes: The content of "text_with_hashes".
    :param encrypted_pii_data: A dictionary matching the structure of "encrypted_pii".
    :return: The newly created DataRecord object.
    """
    if DataRecord.objects(record_id=record_id).first():
        raise ValueError(f"Record with record_id={record_id} already exists.")

    # Build the embedded EncryptedPII object
    # Each field is a list of {"encrypted": "...", "key_version": "..."}
    emails_list = [
        PIIEntry(encrypted=e["encrypted"], key_version=e["key_version"])
        for e in encrypted_pii_data.get("emails", [])
    ]
    phones_list = [
        PIIEntry(encrypted=p["encrypted"], key_version=p["key_version"])
        for p in encrypted_pii_data.get("phone_numbers", [])
    ]
    ssns_list = [
        PIIEntry(encrypted=s["encrypted"], key_version=s["key_version"])
        for s in encrypted_pii_data.get("ssns", [])
    ]

    encrypted_pii = EncryptedPII(
        emails=emails_list,
        phone_numbers=phones_list,
        ssns=ssns_list
    )

    # Create and save the record
    record = DataRecord(
        record_id=record_id,
        text_with_hashes=text_with_hashes,
        encrypted_pii=encrypted_pii
    )
    record.save()
    return record


def get_data_record(record_id: str) -> DataRecord:
    """
    Retrieve a DataRecord by its record_id.

    :param record_id: The UUID-like string identifying the record.
    :return: The matching DataRecord object or None if not found.
    """
    return DataRecord.objects(record_id=record_id).first()


def update_data_record(
        record_id: str,
        new_text_with_hashes: str = None,
        new_encrypted_pii_data: Dict[str, Any] = None
) -> DataRecord:
    """
    Update an existing DataRecord. Fields not provided remain unchanged.

    :param record_id: The record to update.
    :param new_text_with_hashes: Updated text_with_hashes (optional).
    :param new_encrypted_pii_data: Dictionary to replace or modify encrypted_pii (optional).
    :return: The updated DataRecord, or None if the record wasn't found.
    """
    record = DataRecord.objects(record_id=record_id).first()
    if not record:
        return None

    if new_text_with_hashes is not None:
        record.text_with_hashes = new_text_with_hashes

    if new_encrypted_pii_data is not None:
        # (Option A) Overwrite entire embedded document:
        emails_list = [
            PIIEntry(encrypted=e["encrypted"], key_version=e["key_version"])
            for e in new_encrypted_pii_data.get("emails", [])
        ]
        phones_list = [
            PIIEntry(encrypted=p["encrypted"], key_version=p["key_version"])
            for p in new_encrypted_pii_data.get("phone_numbers", [])
        ]
        ssns_list = [
            PIIEntry(encrypted=s["encrypted"], key_version=s["key_version"])
            for s in new_encrypted_pii_data.get("ssns", [])
        ]
        record.encrypted_pii = EncryptedPII(
            emails=emails_list,
            phone_numbers=phones_list,
            ssns=ssns_list
        )

        # (Option B) If you prefer partial updates, you'd manually update each field
        # instead of overwriting. That logic depends on your needs.

    record.save()
    return record


def delete_data_record(record_id: str) -> bool:
    """
    Delete a DataRecord from MongoDB by its record_id.

    :param record_id: The UUID-like string for the record.
    :return: True if a record was deleted, False otherwise.
    """
    record = DataRecord.objects(record_id=record_id).first()
    if record:
        record.delete()
        return True
    return False

# def update_all_records(record_id: str, updated_record: dict, file_path: str) -> str:
#   pass
