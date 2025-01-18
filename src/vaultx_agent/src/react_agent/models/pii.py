from typing import Optional, List

from anthropic import BaseModel


class Encrypted(BaseModel):
    record_id: Optional[str] = None
    processed_text: Optional[str] = None


class Pii(BaseModel):
    phone_numbers: Optional[List[str]] = None


class Decrypted(BaseModel):
    original_text: Optional[str] = None
    decrypted_pii: Optional[Pii] = None
