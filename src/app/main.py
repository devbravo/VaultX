from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from src.core.pii_processing import encrypt_pii, process_text_and_store_in_file

app = FastAPI() 

PII_STORAGE_FILE = "src/db/pii_storage.json"
KEY_METADATA_FILE = "src/db/keys_metadata.json"

class PiiRequest(BaseModel):
  text: str 
  
class DecryptRequest(BaseModel):
  record_id: str

@app.get("/")
async def root():
  return {"message": "Welcome to VaultX Technologies"}

@app.post('/encrypt')
async def encrypt_pii(request: PiiRequest):
  """Encrypt PII data and store it with metadata."""
  try:
    record_id, processed_text = process_text_and_store_in_file(request.text, PII_STORAGE_FILE)
    return {"record_id": record_id, "processed_text": processed_text}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Error processing PII: {e}')