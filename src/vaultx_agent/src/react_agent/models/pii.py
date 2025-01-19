from typing import Optional, List

from pydantic.v1 import BaseModel


class DecryptedPii(BaseModel):
    phone_numbers: Optional[List[str]] = None


class EncryptedPii(BaseModel):
    phone_numbers: Optional[List[dict]] = None


class Encrypted(BaseModel):
    message: Optional[str] = None
    record_id: Optional[str] = None
    processed_text: Optional[str] = None
    encrypted_pii: Optional[EncryptedPii] = None


class Decrypted(BaseModel):
    message: Optional[str] = None
    reconstructed_text: Optional[str] = None
    decrypted_pii: Optional[DecryptedPii] = None


class PlaceHolder:
    PHONE_NUMBER = '[PHONE_NUMBER]'
    EMAIL = '[EMAIL]'
    ADDRESS = '[ADDRESS]'
    NAME = '[NAME]'
    DATE = '[DATE]'
    LOCATION = '[LOCATION]'
    ORGANIZATION = '[ORGANIZATION]'
    IP_ADDRESS = '[IP_ADDRESS]'
    CREDIT_CARD = '[CREDIT_CARD]'
    PASSWORD = '[PASSWORD]'
    MONEY = '[MONEY]'
