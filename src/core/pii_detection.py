import re
from typing import List

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\+?\d{1,4}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3}[\s-]?\d{4}"
SSN_REGEX = r"\b\d{3}-\d{2}-\d{4}\b"
CREDIT_CARD_REGEX = r"\b(?:\d[ -]*?){13,16}\b"
DATE_REGEX = r"\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])[/-](\d{4})\b"
IPV4_REGEX = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
IPV6_REGEX = r"\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
PASSPORT_REGEX = r"\b[A-PR-WY][1-9]\d\s?\d{4}[1-9]\b"
NATIONAL_ID_REGEX = r"\b\d{2}-\d{4}-\d{4}\b"
POSTAL_CODE_REGEX = r"\b\d{5}(-\d{4})?\b"

def detect_emails(text: str) -> List[str]:
    return re.findall(EMAIL_REGEX, text)

def detect_emails(text: str) -> List[str]:
    return re.findall(EMAIL_REGEX, text)
  
def detect_phone_numbers(text: str) -> List[str]:
    return re.findall(PHONE_REGEX, text)
  
def detect_ssns(text: str) -> List[str]:
    return re.findall(SSN_REGEX, text)
  
def detect_credit_cards(text: str) -> List[str]:
    return re.findall(CREDIT_CARD_REGEX, text)
  
def detect_dates(text: str) -> List[str]:
    return re.findall(DATE_REGEX, text)
  
def detect_ips(text: str) -> List[str]:
    ipv4 = re.findall(IPV4_REGEX, text)
    ipv6 = re.findall(IPV6_REGEX, text)
    return ipv4 + ipv6
  
def detect_passport_numbers(text: str) -> List[str]:
    return re.findall(PASSPORT_REGEX, text)
  
def detect_all_pii(text: str) -> dict:
    results = {
        "emails": detect_emails(text),
        "phone_numbers": detect_phone_numbers(text),
        "ssns": detect_ssns(text),
        "credit_cards": detect_credit_cards(text),
        "ips": detect_ips(text),
        "passport_numbers": detect_passport_numbers(text),
    }
    return {key: value for key, value in results.items() if value}
  
text = "Contact me at john.doe@example.com or +1-123-456-7890. My SSN is 123-45-6789."
print(detect_all_pii(text))