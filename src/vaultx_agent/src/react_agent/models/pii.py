from typing import Optional

from anthropic import BaseModel


class EncryptedPii(BaseModel):
    record_id: Optional[dict] | None
    processed_text: Optional[str] | None

class DecryptedPii(BaseModel):
    original_text: str
    decrypted_pii: dict