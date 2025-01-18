import json 
from typing import Dict
import uuid
import logging


logging.basicConfig(level=logging.INFO)


def store_record_by_id(file_path:str, text_with_hashes: str, encrypted_pii: Dict) -> str:
  """Store a new record in the storage file."""
  
  record_id = str(uuid.uuid4())
  
  new_record = {
        "text_with_hashes": text_with_hashes,
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
  
def updte_record(record_id: str, updated_record: dict, file_path: str) -> str:
  pass