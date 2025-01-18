from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from src.core.pii_decryption import decrypt_pii
from src.db.record_repository import get_record_by_id, store_record_by_id
from src.core.pii_encryption import encrypt_pii
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
async def encrypt_data_endpoint(request: EncryptRequest):
  """Encrypt PII data and store it with metadata."""
  try:
    # record_id, processed_text = encrypt_data(request.text)
    text_with_hashes, encrypted_pii = encrypt_pii(request.text)
    record_id = store_record_by_id(PII_STORAGE_FILE, text_with_hashes, encrypted_pii )
    return {"record_id": record_id, "processed_text": text_with_hashes}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Error processing PII: {e}')
  
  
@app.post('/decrypt/')
async def decrypt_data_endpoint(request: DecryptRequest):
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
  