import json 
from typing import Dict

def store_record(record: dict) -> str:
  pass


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