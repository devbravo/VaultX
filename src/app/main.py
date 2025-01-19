from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.core.key_rotation import KeyRotationManager
from src.core.pii_decryption import decrypt_pii
from src.core.pii_encryption import encrypt_pii
from src.core.pii_update_on_key_rotate import update_pii_with_reencryption
from src.db.record_repository import get_all_records, get_record_by_id
from src.db.record_repository import store_all_records, store_record_by_id

app = FastAPI()

PII_STORAGE_FILE = "src/db/pii_storage.json"
KEY_METADATA_FILE = "src/db/keys_metadata.json"


class EncryptRequest(BaseModel):
    text: str


class DecryptRequest(BaseModel):
    record_id: str
    text: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Welcome to VaultX Technologies"}


@app.post('/encrypt/')
async def encrypt_data_endpoint(request: EncryptRequest):
    """Encrypt PII data and store it with metadata."""
    try:
        text_with_hashes, encrypted_pii = encrypt_pii(request.text)
        if not text_with_hashes or not encrypted_pii:
            return {"message": "No PII detected. Nothing was stored."}

        record_id = store_record_by_id(PII_STORAGE_FILE, text_with_hashes, encrypted_pii)
        return {"record_id": record_id, "processed_text": text_with_hashes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error processing PII: {e}')


@app.post('/decrypt/')
async def decrypt_data_endpoint(request: DecryptRequest):
    """Decrypt PII data."""
    try:
        record = get_record_by_id(request.record_id, PII_STORAGE_FILE)
        result = decrypt_pii(record, KEY_METADATA_FILE, request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Error decrypting PII: {e}')


@app.post('/rotate-keys/')
async def rotate_keys():
    """Rotate encryption keys and re-encrypt data"""
    records = get_all_records(PII_STORAGE_FILE)
    old_key, new_key, new_version = KeyRotationManager.rotate_keys(days_threshold=30, usage_threshold=1)
    updated_records = update_pii_with_reencryption(old_key, new_key, new_version, records)
    store_all_records(PII_STORAGE_FILE, updated_records)
