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


def detect_email(text: str) -> List[str]:
    return re.findall(EMAIL_REGEX, text)
  
def detect_phone_number(text: str) -> List[str]:
    return re.findall(PHONE_REGEX, text)
  
def detect_ssn(text: str) -> List[str]:
    return re.findall(SSN_REGEX, text)
  
def detect_credit_card(text: str) -> List[str]:
    return re.findall(CREDIT_CARD_REGEX, text)
  
def detect_date(text: str) -> List[str]:
    return re.findall(DATE_REGEX, text)
  
def detect_ip(text: str) -> List[str]:
    ipv4 = re.findall(IPV4_REGEX, text)
    ipv6 = re.findall(IPV6_REGEX, text)
    return ipv4 + ipv6
  
def detect_passport_number(text: str) -> List[str]:
    return re.findall(PASSPORT_REGEX, text)
  
def detect_pii_regex(text: str) -> dict:
    results = {
        "EMAIL": detect_email(text),
        "PHONE_NUMBER": detect_phone_number(text),
        "SOCIAL_SECURITY_NUMBER": detect_ssn(text),
        "CREDIT_CARD": detect_credit_card(text),
        "IP_ADDRESS": detect_ip(text),
        "PASSPORT_NUMBER": detect_passport_number(text),
    }
    return {key: value for key, value in results.items() if value}