from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from src.core.pii_decryption import decrypt_pii
from src.db.pii_repository import get_record_by_id
from src.core.pii_encryption import process_text_and_store_in_file
from src.core.key_rotation import KeyRotationManager

app = FastAPI() 

PII_STORAGE_FILE = "src/db/pii_storage.json"
KEY_METADATA_FILE = "src/db/keys_metadata.json"

class EncryptRequest(BaseModel):
  text: str 
  
class DecryptRequest(BaseModel):
  record_id: str

@app.get("/")
async def root():
  return {"message": "Welcome to VaultX Technologies"}


@app.post('/encrypt/')
async def encrypt_data(request: EncryptRequest):
  """Encrypt PII data and store it with metadata."""
  try:
    record_id, processed_text = process_text_and_store_in_file(request.text, PII_STORAGE_FILE)
    return {"record_id": record_id, "processed_text": processed_text}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Error processing PII: {e}')
  
  
@app.post('/decrypt/')
async def decrypt_data(request: DecryptRequest):
  """Decrypt PII data."""
  try:
    record = get_record_by_id(request.record_id, PII_STORAGE_FILE)
    result = decrypt_pii(record, KEY_METADATA_FILE)
    return result
  except Exception as e:
    raise HTTPException(status_code=404, detail=f'Error decrypting PII: {e}')
  

@app.post('rotate-keys/')
async def rotate_keys():
  """Rotate encryption keys and re-encrypt data"""
  