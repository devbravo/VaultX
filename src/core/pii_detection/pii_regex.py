"""
Regex-based PII Detection Module

This module provides predefined regular expressions and utility functions for detecting
various types of Personally Identifiable Information (PII) in text."""

import re 
from typing import List


EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
CREDIT_CARD_REGEX = r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$"
PHONE_REGEX = r"^(?:\+1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$"
SSN_REGEX = r"\b\d{3}-\d{2}-\d{4}\b"
DATE_REGEX = r"\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])[/-](\d{4})\b"
IPV4_REGEX = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
IPV6_REGEX = r"\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
PASSPORT_REGEX = r"\b([A-Z][0-9]{8}|[A-Z]{2}[0-9]{7}|[A-Z]{3}[0-9]{6}|[A-Z]{2}[A-Z0-9]{7})\b"
NATIONAL_ID_REGEX = r"\b\d{2}-\d{4}-\d{4}\b"
POSTAL_CODE_REGEX = r"\b\d{5}(-\d{4})?\b"
ADDRESS_REGEX = r"\d+\s[A-Za-z0-9\s.,#-]+(?:\bStreet\b|\bSt\b|\bAvenue\b|\bAve\b|\bRoad\b|\bRd\b|\bBoulevard\b|\bBlvd\b|\bLane\b|\bLn\b|\bDrive\b|\bDr\b|\bCourt\b|\bCt\b|\bParkway\b|\bPkwy\b|\bPlaza\b|\bPlz\b|\bCircle\b|\bCir\b)"


def detect_email(text: str) -> List[str]:
  return re.findall(EMAIL_REGEX, text)
  
def detect_credit_card(text: str) -> List[str]:
  return re.findall(CREDIT_CARD_REGEX, text)


def detect_phone_number(text: str) -> List[str]:
  return re.findall(PHONE_REGEX, text)
  
def detect_ssn(text: str) -> List[str]:
  return re.findall(SSN_REGEX, text)
  
  
def detect_date(text: str) -> List[str]:
  return re.findall(DATE_REGEX, text)
  
def detect_ip(text: str) -> List[str]:
  ipv4 = re.findall(IPV4_REGEX, text)
  ipv6 = re.findall(IPV6_REGEX, text)
  return ipv4 + ipv6
  
def detect_passport_number(text: str) -> List[str]:
  return re.findall(PASSPORT_REGEX, text)
  
def detect_address(text: str) -> List[str]:
  return re.findall(ADDRESS_REGEX, text)

  
def detect_pii_regex(text: str) -> dict:
  results = {
      "EMAIL": detect_email(text),
      "CREDIT_CARD": detect_credit_card(text),
      "PHONE_NUMBER": detect_phone_number(text),
      "SOCIAL_SECURITY_NUMBER": detect_ssn(text),
      "DATA": detect_date(text),
      "IP_ADDRESS": detect_ip(text),
      "PASSPORT_NUMBER": detect_passport_number(text),
      "ADDRESS": detect_address(text)
  }
  return {key: value for key, value in results.items() if value}