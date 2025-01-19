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
    PHONE_NUMBER = '[phone-number]'
    EMAIL = '[email]'
    ADDRESS = '[address]'
    NAME = '[name]'
    DATE = '[date]'
    LOCATION = '[location]'
    ORGANIZATION = '[organization]'
    IDENTIFIER = '[identifier]'
    URL = '[url]'
    IP_ADDRESS = '[ip-address]'
    CREDIT_CARD = '[credit-card]'
    SSN = '[ssn]'
